class SQL:
    
    def setup_replication_sql(self, src_endpoint, src_port, user, password, file, pos):
        return f"""
                CALL mysql.rds_set_external_master('{src_endpoint}', {src_port},
                '{user}', '{password}', '{file}', {pos}, 0);
                """
   
    def start_replication_sql(self):
        return f"""
                CALL mysql.rds_start_replication;
                """

    def show_slave_status_sql(self):
        return f"""
                SHOW SLAVE STATUS;
                """