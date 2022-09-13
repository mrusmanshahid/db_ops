#!/bin/bash

## Configurations for the source database from where the script is supposed to read the data.
src_url="<source_db_url_or_endpoint>"
src_username="<source_db_username>"
src_password="<source_db_password>"

## Configuration for the destination database where the script is supposed to write the data.
dest_url="<destination_db_url_or_endpoint>"
dest_username="<destination_db_username>"
dest_password="<destination_db_password>"

## The database configurations, the schema and table name.
src_database="<source_schema_name>"
dest_database="<destination_schema_name>"
table_name="<table_to_migrate>"

## Batch size and configurations to migrate in smaller chunks.
batch_start=0
batch_end=100
threshold=15
batch_end_current=$((batch_start+threshold-1))

## Migration script without locking the source and destination table, and migration in small batches
while test $batch_end -gt $batch_end_current
do  
        echo "Fetch records from the source for migration for batch $batch_start and $((batch_end_current))"
        mysqldump -h $src_url -u $src_username -p$src_password $src_database $table_name --where="id between $batch_start and $batch_end_current" --single-transaction --skip-add-locks --no-create-info > ./data/dump_$batch_start.sql

        echo "Writing batch records from $batch_start and $batch_end_current to destination for migration"
        mysql -h $dest_url -u $dest_username -p$dest_password $dest_database < ./data/dump_$batch_start.sql

        batch_start=$((batch_end_current+1))
        batch_end_current=$((batch_start+threshold-1))
done

echo "Fetch records from the source for migration for batch $batch_start and $batch_end)"
mysqldump -h $src_url -u $src_username -p$src_password $src_database $table_name --where="id between $batch_start and $batch_end" --single-transaction --skip-add-locks --no-create-info > ./data/dump_$batch_start.sql

echo "Writing batch records from $batch_start and $batch_end to destination for migration"
mysql -h $dest_url -u $dest_username -p$dest_password $dest_database < ./data/dump_$batch_start.sql

echo "Migration is successfully completed for the records, please verify the data on the target."
