
import os

# Connections Configurations 
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')

# Migration Related Configurations
parent_cluster_parameter_group_name = "replace-me-with-src-db-cluster-pg-name"
new_cluster_paremeter_group_name = "replace-me-with-new-db-cluster-pg-name"

parent_instance_parameter_group_name = "replace-me-with-src-db-instance-pg-name"
new_instance_paremeter_group_name = "replace-me-with-new-db-instance-pg-name"

parent_cluster_name = "replace-me-with-cluster-name"
new_cluster_name = "replace-me-with-new-cluster-name"
new_instance_name = "replace-me-with-new-instance-name"
snapshot_identifier = "snapshot-to-restore-new-cluster"

# DMS Related Configuration
dms_instance_arn = "arn:aws:dms:eu-central-1:942878658013:rep:JPRG72I6OOPDFCM5SSTMLXX3YEXBUHIF7RD4YOI"
instance_class = "db.r6g.xlarge"
use_dms = True

# Replication Pattern Table Suffixes, example table1_03, table_02 will only be replicated
patterns = 'table-ending-with-suffix-1,table-ending-with-suffix-2'
