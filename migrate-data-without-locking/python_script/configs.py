from env_variables import config_file_name
import yaml
import logging


class Config:

    def load_configs(self):
        self.set_logging_config()
        logging.info("Fetching Configurations")

        configurations = yaml.load(open(config_file_name), Loader=yaml.FullLoader)
        Config.src_db_url = configurations.get("src_db_url")
        Config.src_db_username = configurations.get("src_db_username")
        Config.src_db_password = configurations.get("src_db_password")
        Config.src_schema = configurations.get("src_schema")

        Config.dest_db_url = configurations.get("dest_db_url")
        Config.dest_db_username = configurations.get("dest_db_username")
        Config.dest_db_password = configurations.get("dest_db_password")
        Config.dest_schema = configurations.get("dest_schema")
        
        Config.table_name = configurations.get("table_name")
        Config.batch_start = configurations.get("batch_start")
        Config.batch_end = configurations.get("batch_end")
        Config.batch_size = configurations.get("batch_size")

    @staticmethod
    def set_logging_config():
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
