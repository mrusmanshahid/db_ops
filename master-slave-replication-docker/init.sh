#!/bin/bash

export mysql_master_slave_password=bolt123

docker-compose up -d

until docker exec slave sh -c "mysql -u root -p$mysql_master_slave_password -e ';'"
do
    echo "Waiting for slave..."
    sleep 3
done

until docker exec master sh -c "mysql -u root -p$mysql_master_slave_password -e ';'"
do
    echo "Waiting for master..."
    sleep 3
done

echo "Building replication between master and slave"

docker exec slave sh -c 'bash /etc/build_replication.sh'
