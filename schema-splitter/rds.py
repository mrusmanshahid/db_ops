import boto3
import time
import logging
from rich import print

class RDS:

    def get_client(self):
        client = boto3.client('rds')
        return client
    
    def get_db_instance(self, instance_name):
        try:
            client = self.get_client()
            response = client.describe_db_clusters(
                DBClusterIdentifier=instance_name
            )
            return response['DBClusters'][0]
        except:
            pass

    def get_parameter_group(self, parameter_group_name):
        try:
            client = self.get_client()
            response = client.describe_db_parameter_groups(DBParameterGroupName=parameter_group_name)
            return response['DBParameterGroups'][0]
        except:
            pass

    def get_cluster_parameter_group(self, parameter_group_name):
        try:
            client = self.get_client()
            response = client.describe_db_cluster_parameter_groups(DBClusterParameterGroupName=parameter_group_name)
            return response['DBClusterParameterGroups'][0]
        except:
            pass  
    
    def copy_cluster_parameter_group(self, parent_parameter_group, new_parameter_group):
        res = self.get_cluster_parameter_group(new_parameter_group)
        if res:
            logging.info("The parameter group exists.. skipping this step.")
            return new_parameter_group

        logging.info(f"Creating new parameter group witn name {parent_parameter_group}")
        client = self.get_client()
        response = client.copy_db_cluster_parameter_group(
            SourceDBClusterParameterGroupIdentifier=parent_parameter_group,
            TargetDBClusterParameterGroupIdentifier=new_parameter_group,
            TargetDBClusterParameterGroupDescription=new_parameter_group
        )

    def copy_instance_parameter_group(self, parent_parameter_group, new_parameter_group):
        res = self.get_parameter_group(new_parameter_group)
        if res:
            logging.info("The parameter group exists.. skipping this step.")
            return new_parameter_group

        logging.info(f"Creating new parameter group witn name {parent_parameter_group}")
        client = self.get_client()
        response = client.copy_db_parameter_group(
            SourceDBClusterParameterGroupIdentifier=parent_parameter_group,
            TargetDBClusterParameterGroupIdentifier=new_parameter_group,
            TargetDBClusterParameterGroupDescription=new_parameter_group
        )
    
    def restore_db_snapshot(self, snapshot_identifier, 
                            new_cluster_name, new_instance_name,
                            new_cluster_paremeter_group_name, new_instance_paremeter_group_name, 
                            instance_class, parent_instance):
        
        res = self.get_db_instance(new_cluster_name)
        client = self.get_client() 
        
        if res:
            self.wait_for_availability(new_cluster_name)
            logging.info("The target instance already exists.. skipping this step.")
            
            waiter = client.get_waiter('db_instance_available')
            waiter.wait(DBInstanceIdentifier=new_instance_name)
            return new_cluster_name
        
        logging.info(f"Creating new instanace with name {new_cluster_name}")
        security_groups = list(map(lambda x: x['VpcSecurityGroupId'],parent_instance['VpcSecurityGroups']))

        client.restore_db_cluster_from_snapshot(
            DBClusterIdentifier=new_cluster_name,
            Engine=parent_instance['Engine'],
            EngineVersion=parent_instance['EngineVersion'],
            SnapshotIdentifier=snapshot_identifier,
            DBClusterInstanceClass=instance_class,
            Port=parent_instance['Port'],
            DBSubnetGroupName=parent_instance['DBSubnetGroup'],
            PubliclyAccessible=False,
            Tags=parent_instance['TagList'],
            VpcSecurityGroupIds=security_groups,
            CopyTagsToSnapshot=True,
            DBClusterParameterGroupName=new_cluster_paremeter_group_name,
            DeletionProtection=True,
            EnableCloudwatchLogsExports=['error','slowquery']
        )

        logging.info("Waiting 10 seconds before initiating a db instance under the cluster")
        time.sleep(10)

        client.create_db_instance(
            DBInstanceIdentifier=new_instance_name,
            DBClusterIdentifier=new_cluster_name,
            DBInstanceClass=instance_class,
            Engine=parent_instance['Engine'],
            Tags=parent_instance['TagList'],
            DBParameterGroupName=new_instance_paremeter_group_name,
            AutoMinorVersionUpgrade=False,
        )

        self.wait_for_availability(new_cluster_name)

        waiter = client.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=new_instance_name)

        client.modify_db_cluster(
            DBClusterIdentifier=new_cluster_name,
            ApplyImmediately=True,
            AutoMinorVersionUpgrade=False,
        )

        logging.info("Waiting 10 seconds before initiating a other db operations for the cluster")
        time.sleep(10)
        
        return new_cluster_name

    def wait_for_availability(self, instance_name):
        instance = self.get_db_instance(instance_name)
        status = instance['Status']
        while status != "available":
            logging.info(f"Waiting for instance to become available for further actions, current status is {status}")
            time.sleep(5)
            instance = self.get_db_instance(instance_name)
            status = instance['Status']

    def get_binlog_events(self, instance_name):
        client = self.get_client()
        response = client.describe_events(
            Duration=10080,
            SourceIdentifier=instance_name,
            SourceType='db-instance'
        )
        binglog_events = list(filter(lambda x: 'Binlog' in x['Message'], response['Events']))
        return binglog_events
