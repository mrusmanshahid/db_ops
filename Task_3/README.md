# Migrate Data From Source to Target Without Locking

## Background
The small shell script that migrates the data in user defined smaller chunks from source to master.
## How To Bootstrap?
Follow the instructions migrate data from source database to destination database:

- Clone this repository,
- Edit `migrate_without_locking.sh` and set all the required variables as per the instructions.
  - `batch_start`: The start value for id column of the table.
  - `batch_end`: The end value for the id column of the table.
  - `threshold`: The the size of chunk which the data needs to be migrated.
  - `table_name`: The table name which needs to be migrated from source to destination.
  - `src-*`: Set these variables for the source database connection.
  - `dest-*`: Set these variables for the destination database connection.
- Run `migrate_without_locking.sh` for data migration.
- Verify data on target.
- You are done ;)