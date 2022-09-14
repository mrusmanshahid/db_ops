# Migrate Data From Source to Target Without Locking

## Background
The small shell script that migrates the data in user defined smaller chunks from source to master.
## How To Bootstrap?
Follow the following instruction to build your own master-slave cluster using docker:

- Clone this repository,
- Edit `migrate_without_locking.sh` and set all the required variables as per the instructions.
- Run `migrate_without_locking.sh` for data migration.
- Verify data on target.
- You are done ;)