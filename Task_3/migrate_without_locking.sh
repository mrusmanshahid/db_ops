#!/bin/bash

## Configurations for the source database from where the script is supposed to read the data.
src_url="qa-6.cgevunlz3bfz.eu-west-1.rds.amazonaws.com"
src_username="careemuser"
src_password="xFxGNTX34VGnmBaN"

## Configuration for the destination database where the script is supposed to write the data.
dest_url=$4
dest_username=$5
dest_password=$6

## The database configurations, the schema and table name.
database_name="qa_careem"
table_name="usman_test"

## Batch size and configurations to migrate in smaller chunks.
batch_start=0
batch_end=100
threshold=15
batch_end_current=$((batch_start+threshold-1))

## Migration script without locking the source and destination table, and migration in small batches
while test $batch_end -gt $batch_end_current
do  
        echo "Fetch records from the source for migration for batch $batch_start and $((batch_end_current))"
        mysqldump -h $src_url -u $src_username -p$src_password $database_name $table_name --where="id between $batch_start and $batch_end_current" --single-transaction --skip-add-locks --no-create-info > ./data/dump_$batch_start.sql

        echo "Writing batch records from $batch_start and $batch_end_current to destination for migration"
        mysql -h $dest_url -u $dest_username -p$dest_password $database < ./data/dump_$batch_start.sql

        batch_start=$((batch_end_current+1))
        batch_end_current=$((batch_start+threshold-1))
done

echo "Fetch records from the source for migration for batch $batch_start and $batch_end)"
mysqldump -h $src_url -u $src_username -p$src_password $database_name $table_name --where="id between $batch_start and $batch_end" --single-transaction --skip-add-locks --no-create-info > ./data/dump_$batch_start.sql

echo "Writing batch records from $batch_start and $batch_end to destination for migration"
mysql -h $dest_url -u $dest_username -p$dest_password $database < ./data/dump_$batch_start.sql

echo "Migration is successfully completed for the records, please verify the data on the target."
