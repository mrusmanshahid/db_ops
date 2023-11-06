from migrate_data import MigrateData
from configs import Config
import argparse

def main(is_delete_from_source):
    Config().load_configs()
    MigrateData().migrate_to_destination()
    if is_delete_from_source:
        MigrateData().delete_from_source()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete_from_source", help="Set this flag to delete the data from source.")
    args = parser.parse_args()
    main(args.delete_from_source)
