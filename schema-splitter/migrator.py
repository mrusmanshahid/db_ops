import logging
from rds import RDS
from dms import DMS
from database import Database
from env import dms_instance_arn, snapshot_identifier, parent_cluster_name, instance_class
from env import parent_instance_parameter_group_name, new_instance_paremeter_group_name
from env import parent_cluster_parameter_group_name, new_cluster_paremeter_group_name
from env import new_instance_name, new_cluster_name
from env import mysql_password, mysql_user, use_dms
from sql import SQL

class Migrator:

    def __init__(self) -> None:
        self.parent_instance = None
        self.db_ops = Database()
        self.rds = RDS()
        self.sql = SQL()
        self.dms = DMS()

    def restore_country_db(self):
        logging.info(f"Restoring a new cluster from snapshot")
        self.parent_instance = self.rds.get_db_instance(parent_cluster_name)
        pg_cluster = self.rds.copy_cluster_parameter_group(parent_cluster_parameter_group_name, new_cluster_paremeter_group_name)
        pg_instance = self.rds.copy_instance_parameter_group(parent_instance_parameter_group_name, new_instance_paremeter_group_name)
        
        ins = self.rds.restore_db_snapshot(snapshot_identifier, 
                                      new_cluster_name, new_instance_name,  
                                      new_cluster_paremeter_group_name, new_instance_paremeter_group_name, 
                                      instance_class, self.parent_instance)
        
        self.new_instance = self.rds.get_db_instance(new_cluster_name)

    def get_binlog_file_and_position(self, instance_name):
        events = self.rds.get_binlog_events(instance_name)
        if len(events) == 0:
            logging.error("No binlog event found, please check snapshot is restored from the backedup instance")
            return {}
        message = events[0]['Message'].split(' ')
        binlog_file = message[-2]
        binlog_position = message[-1]
        logging.info("Binlog position found, moving to setting up target")
        return {'binlog_file': binlog_file, 'binlog_position': binlog_position}

    def establish_replication_with_source(self):
        writer_name = list(filter(lambda x: x['IsClusterWriter'] == True, self.new_instance['DBClusterMembers']))[0]['DBInstanceIdentifier']
        binlog = self.get_binlog_file_and_position(writer_name)

        if binlog:
            conn_new_db = self.db_ops.get_connection(self.new_instance['Endpoint'], 
                                                mysql_user, mysql_password, self.new_instance['Port'])
            
            sql_setup = self.sql.setup_replication_sql(self.parent_instance['Endpoint'], 
                                                 self.parent_instance['Port'], mysql_user, mysql_password, 
                                                 binlog['binlog_file'], binlog['binlog_position'])
            
            self.db_ops.execute(conn_new_db, sql_setup)
            logging.info(f"Successfully setup target for {binlog['binlog_file']} at {binlog['binlog_position']}")
            self.db_ops.execute(conn_new_db, self.sql.start_replication_sql())

    def check_replication_status(self):
        conn_new_db = self.db_ops.get_connection(self.new_instance['Endpoint'], 
                                                mysql_user, mysql_password, self.new_instance['Port'])
        sql = self.sql.show_slave_status_sql()
        res = self.db_ops.execute_and_fetch(conn_new_db,sql)
        if len(res) > 0:
            status = res[0]['Slave_IO_State']
            logging.info(f"Slave I/O Status is {status}")
            logging.info(f"Replication is active and current at status {status}")
            return True
        return False
    
    def setup_dms_task(self):   
        writer_name = list(filter(lambda x: x['IsClusterWriter'] == True, self.new_instance['DBClusterMembers']))[0]['DBInstanceIdentifier']
        binlog = self.get_binlog_file_and_position(writer_name)
        cdc_start = f"{binlog['binlog_file']}:{binlog['binlog_position']}"
        source_endpoint_name = f"migration-{parent_cluster_name}-source"
        src_host = self.parent_instance['Endpoint']
        src_port = self.parent_instance['Port']
        target_endpoint_name = f"migration-{new_cluster_name}-target"
        tgt_host = self.new_instance['Endpoint']
        tgt_port = self.new_instance['Port']
        task_name = f"task-migration-{parent_cluster_name}-{new_cluster_name}"
        arn_src= self.dms.create_endpoint(source_endpoint_name, src_host, mysql_user, mysql_password, src_port, "source")
        arn_dest = self.dms.create_endpoint(target_endpoint_name, tgt_host, mysql_user, mysql_password, tgt_port, "target")
        self.dms.create_dms_task(task_name,arn_src, arn_dest, dms_instance_arn, cdc_start)

    def setup_replication(self):
        if use_dms:
            logging.info("You have selected to use DMS")
            self.setup_dms_task()
            return

        if not self.check_replication_status():
            logging.info("You have selected to use Native Replication")
            self.establish_replication_with_source()

    def run_migration(self):
        logging.info("Starting migration process")
        self.restore_country_db()
        self.setup_replication()
        logging.info("Migration has been completed.")
