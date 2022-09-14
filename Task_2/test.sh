export mysql_master_slave_password=bolt123

FAIL='\033[0;31m'
PASS='\033[0;32m'
NC='\033[0m'


function replication_test()
{
    if docker exec master sh -c "export MYSQL_PWD=$mysql_master_slave_password; mysql -u root -e 'CREATE DATABASE replication_test;' > /tmp/out "
    then 
    printf "${PASS}Creating testing schema on master \xE2\x9C\x94\n${NC}"
    fi

    if $(docker exec slave sh -c "export MYSQL_PWD=$mysql_master_slave_password; mysql -u root -e 'USE replication_test;'")
    then
    printf "${PASS}Reading schema from slave, test passed \xE2\x9C\x94\n${NC}"
    else
    printf "${FAIL}Schema didnt replicate, test failed x \n${NC}"
    fi

    if $(docker exec master sh -c "export MYSQL_PWD=$mysql_master_slave_password; mysql -u root -e 'DROP DATABASE replication_test;'")
    then
    printf "${PASS}Droping schema from master \xE2\x9C\x94\n ${NC}"
    fi
}

replication_test