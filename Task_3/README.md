# Migrate Data From Source to Target Without Locking

## Background
The small shell script that migrates the data in user defined smaller chunks from source to master.
## How To Setup - Bash Script?
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

## How To Setup - Python Script?

The configuration file contains the configurations to migrate/split the data between source and target table.

The configuration file `yaml` should look like this:

```yaml
src_db_url: <source database endpoint>
src_db_username: <source database username>
src_db_password: <source database password>
src_schema: <source schema_name>

dest_db_url: <destination database endpoint>
dest_db_username: <destination database username>
dest_db_password: <destination database password>
dest_schema: <destination schema_name>

table_name: <table name to migrate between source and destination>

batch_start: <start id for migration>
batch_end: <end id for migration>
batch_size: <no of records in each transaction>
```

`python main.py`