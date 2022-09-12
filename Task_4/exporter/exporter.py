import logging
import time
import random
from os import path
import yaml
from prometheus_client.core import GaugeMetricFamily, REGISTRY, Info
from prometheus_client import start_http_server
import pymysql
import socket

class CollectMysqlConnections(object):
    
    def __init__(self):
        self.hosts=[]

    def get_connection(self, database_url, username, password, port):
        try:
            conn = pymysql.connect(host=database_url, user=username, password=password, port=port, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
            return conn
        except Exception as e:
            logging.info("connection failed, will retry in 5 seconds")
            time.sleep(5)
            return self.get_connection(database_url, username, password, port)

    def collect_metrics(self, host):
        connection = self.get_connection(host, "root", "root", 3306)
        query_connection = "SHOW STATUS WHERE `variable_name` = 'Threads_connected';"
        query_hostname = "select @@hostname as `host`;"
        connections = 0
        hostname = ""
        with connection.cursor() as conn:
            conn.execute(query_connection)
            connections = conn.fetchone()["Value"]
            conn.execute(query_hostname)
            hostname = f"host_{conn.fetchone()['host']}"
        return connections, hostname

    def resolve_and_collect(self):
        ip = socket.gethostbyname("mysql")
        if ip not in self.hosts:
            logging.info(f"new host {ip} has been detected and being tracked now.")
            self.hosts.append(ip)
    
    def collect(self):
        self.resolve_and_collect()
        for host in self.hosts:
            connections, hostname = self.collect_metrics(host)
            gauge = GaugeMetricFamily("db_connections", "db connection of the container", labels=[hostname])
            gauge.add_metric(["db_connections"], connections)
            yield gauge

if __name__ == "__main__":
    port = 9000
    frequency = 1
    if path.exists('config.yml'):
        with open('config.yml', 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                port = int(config['port'])
                frequency = config['scrape_frequency']
            except yaml.YAMLError as error:
                print(error)

    start_http_server(port)
    REGISTRY.register(CollectMysqlConnections())
    while True: 
        time.sleep(frequency)
