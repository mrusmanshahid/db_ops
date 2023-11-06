#!/bin/bash

file=$(mysql -h master -u root -pbolt123 -e "show master status \G" | grep "File"| cut -d ":" -f2;)

file=$(sed "s/ //g" <<< $file)

position=$(mysql -h master -u root -pbolt123 -e "show master status \G" | grep "Position"| cut -d ":" -f2;)

position=$(sed "s/ //g" <<< $position)

slave_stmt="CHANGE MASTER TO MASTER_HOST='master',MASTER_USER='root',MASTER_PASSWORD='bolt123',MASTER_LOG_FILE='$file',MASTER_LOG_POS=$position; START SLAVE;"

echo $slave_stmt

mysql -u root -pbolt123 -e "$slave_stmt"
