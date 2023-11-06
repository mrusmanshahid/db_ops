
from migrator import Migrator
import logging

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    Migrator().run_migration()
