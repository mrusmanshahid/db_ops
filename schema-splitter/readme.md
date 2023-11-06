# Schema Split Migration Script

The script can be used to establish to split any database with replication from source to destination using DMS and Native MySQL Replication.


## Environment Variables

To run this project, you will need to set the following environment variables

`MYSQL_USER`

`MYSQL_PASSWORD`

## Script Parameters

You are required to modify `env.py` file 

- `parent_cluster_parameter_group_name` = the name of the cluster parameter group at source

- `new_cluster_paremeter_group_name` = the name of the cluster parameter group that needs to attach, if used same then it will attach what we have on the source, if changed then it will create a copy of source with new name and attach, if the parameter group is already created then it will skip creation and attach directly.

- `parent_instance_parameter_group_name` = the name of the instance parameter group at source


- `new_instance_paremeter_group_name` = the name of the parameter group that needs to attach, if used same then it will attach what we have on the source, if changed then it will create a copy of source with new name and attach, if the parameter group is already created then it will skip creation and attach directly.

- `parent_cluster_name` = name of the source cluster

- `new_cluster_name` = name of the new/target cluster

- `new_instance_name` = name of the writer node under new cluster

- `snapshot_identifier` = snapshot to use for replication

- `dms_instance_arn` = arn of the dms-instance

- `instance_class` = the class of the new/target cluster

- `use_dms` = set True if we need to use dms else native replication
## How to Run
After setting the environment, run `main` to start the process
`python3 main.py`


`TIP`
The cluster create can take time so the process can be stopped once we will reach `Waiting for instance to become available for further actions...` don't worry once the instance is available we can re-run the script and it will continue from where it left.
