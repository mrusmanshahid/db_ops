import boto3
import logging
import time
from env import patterns

class DMS:

    def __init__(self) -> None:
        pass

    def get_client(self):
        client = boto3.client('dms')
        return client
    
    def get_endpoint(self, identifier):
        try:
            client = self.get_client()
            result = client.describe_endpoints(
                        Filters=[
                            {
                                'Name': 'endpoint-id',
                                'Values': [identifier]
                            },
                        ]
                    )
            return result['Endpoints'][0]
        except:
            pass
    

    def get_dms_task(self, identifier):
        try:
            client = self.get_client()
            response = client.describe_replication_tasks(
                    Filters=[
                        {
                            'Name': 'replication-task-id',
                            'Values': [identifier]
                        },
                    ],
                    WithoutSettings=True
                )
            return response['ReplicationTasks'][0]
        except:
            pass

    def create_endpoint(self, identifier, host, username, password, port, endpoint_type="source"):
        res = self.get_endpoint(identifier)
        if res:
            return res['EndpointArn']
        
        logging.info(f"Creating new dms endpoint for instance -> {identifier} as {endpoint_type}")
        client = self.get_client()
        client.create_endpoint(
            ServerName=host,
            EndpointIdentifier=identifier,
            EndpointType=endpoint_type,
            EngineName='mysql',
            Username=username,
            Password=password,
            Port=port
        )
        time.sleep(3)
        res = self.get_endpoint(identifier)
        return res['EndpointArn']

    def create_dms_task(self, identifier, soruce_arn, target_arn, repl_instance_arn, binlog_position):
        res = self.get_dms_task(identifier)
        if res:
            logging.info("The task is already created, skipping this step.")
            # self.wait_for_availability(identifier)
            return res['ReplicationTaskIdentifier']
        
        logging.info("Creating new replication task for migration")
        client = self.get_client()
        response = client.create_replication_task(
            ReplicationTaskIdentifier=identifier,
            SourceEndpointArn=soruce_arn,
            TargetEndpointArn=target_arn,
            ReplicationInstanceArn=repl_instance_arn,
            MigrationType='cdc',
            TableMappings=self.get_table_mappings(),
            TaskData=self.get_task_settings(),
            ReplicationTaskSettings=self.get_replication_settings(),
            CdcStartPosition=binlog_position
        )
        # self.wait_for_availability(identifier)

    def get_replication_settings(sef):
        return  """ 
                {
                    "TargetMetadata": {
                        "BatchApplyEnabled": true
                    }
                }
                """

    def get_rules(self):
        rules = []
        template = """{
                        "rule-type": "selection",
                        "rule-id": "22113566{idx}",
                        "rule-name": "22113566{idx}",
                        "object-locator": {
                            "schema-name": "%",
                            "table-name": "%{pattern}"
                        },
                        "rule-action": "include",
                        "filters": []
                    }"""
        for i, pattern in enumerate(patterns.split(",")):
            rule = template.replace('{pattern}', pattern.strip()).replace('{idx}', str(i))
            rules.append(rule)
        return "\n,".join(rules)

    def get_table_mappings(self):
        rules = self.get_rules()
        mapping = """
            {
            "rules": [
                """+rules+"""
            ]
            }
            """
        return mapping

    def get_task_settings(self):
        return """
            {
                "FullLoadSettings":{
                    "TargetTablePrepMode":"DO_NOTHING"
                }
            }
        """

    def wait_for_availability(self, identifier):
        instance = self.get_dms_task(identifier)
        while instance['Status'] not in ["ready", "running"]:
            logging.info("Waiting for instance to become available for further actions")
            time.sleep(5)
            instance = self.get_dms_task(identifier)
