# Master-Slave Replication MySQL in Docker

## Background
The small POC focuses over delivering the concept of how to setup a master/slave replication using docker-compose and bash script.

## How To Bootstrap?
Follow the following instruction to build your own master-slave cluster using docker:

- Clone this repository,
- Edit `init.sh` and set value for password in `mysql_master_slave_password=<your_desired_password>`
- Run `init.sh` for cluster initialization.
- Access and Verify  by connecting to master at the port `3306` and slave at `3307`
    - Master: `mysql -u root -p<password_for_cluster> -P 3306`
    - Slave: `mysql -u root -p<password_for_cluster> -P 3307`