import logging

import boto3
from boto3.dynamodb.conditions import Key

log = logging.getLogger(__name__)

RCU_COST = 0.00000125


class DdbTable:
    def __init__(self, table: str):
        self.session = boto3.Session(profile_name="fbs-int-userfull")
        self.ddb = self.session.resource("dynamodb")
        self.table_name = table
        self.table = self.ddb.Table(table)

    def create_table(self):
        # Table creation parameters
        table_params = {
            "TableName": self.table_name,
            "BillingMode": "PAY_PER_REQUEST",
            "KeySchema": [
                {"AttributeName": "PK", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "SK", "KeyType": "RANGE"},  # Sort key
            ],
            "AttributeDefinitions": [
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
        }

        # Create the table
        response = self.ddb.create_table(**table_params)
        log.info(f"Table {self.table_name} created successfully.")

        # Wait until the table exists and can be accessed
        self.ddb.meta.client.get_waiter("table_exists").wait(TableName=self.table_name)

        # Update the table to enable Point-In-Time Recovery
        pitr_response = self.session.client("dynamodb").update_continuous_backups(
            TableName=self.table_name,
            PointInTimeRecoverySpecification={"PointInTimeRecoveryEnabled": True},
        )
        log.info(f"Point-in-time recovery enabled for {self.table_name}.")

        return response

    def delete_table(self):
        response = self.table.delete()

        # Wait until the table is deleted
        self.ddb.meta.client.get_waiter("table_not_exists").wait(
            TableName=self.table_name
        )
        log.info(f"Table {self.table_name} deleted successfully.")
        return response

    def get_unique_pks(self):
        unique_pks = set()
        last_evaluated_key = None
        total_rcu = 0  # Total Read Capacity Units consumed

        while True:
            scan_kwargs = {"ReturnConsumedCapacity": "TOTAL"}
            if last_evaluated_key:
                scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

            response = self.table.scan(**scan_kwargs)

            # Extract PKs
            for item in response["Items"]:
                pk = item["PK"]  # Replace 'PK' with your actual PK attribute name
                unique_pks.add(pk)

            # Accumulate RCU
            total_rcu += response["ConsumedCapacity"]["CapacityUnits"]

            last_evaluated_key = response.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

        log.info(
            f"Total RCU Consumed: {total_rcu}, {round(total_rcu * RCU_COST, ndigits=4)} USD"
        )
        return unique_pks

    def clear_table(self):
        total_rcu = 0  # Total Read Capacity Units consumed
        total_wcu = 0  # Total Write Capacity Units consumed

        scan_kwargs = {"ReturnConsumedCapacity": "TOTAL"}

        scan = self.table.scan(**scan_kwargs)
        total_rcu += scan["ConsumedCapacity"]["CapacityUnits"]

        items = scan["Items"]

        for item in items:
            pk = item["PK"]
            sk = item["SK"]

            delete_response = self.table.delete_item(
                Key={"PK": pk, "SK": sk}, ReturnConsumedCapacity="TOTAL"
            )
            total_wcu += delete_response["ConsumedCapacity"]["CapacityUnits"]

        while "LastEvaluatedKey" in scan:
            scan_kwargs["ExclusiveStartKey"] = scan["LastEvaluatedKey"]
            scan = self.table.scan(**scan_kwargs)
            total_rcu += scan["ConsumedCapacity"]["CapacityUnits"]

            items = scan["Items"]

            for item in items:
                pk = item["PK"]
                sk = item["SK"]
                delete_response = self.table.delete_item(
                    Key={"PK": pk, "SK": sk}, ReturnConsumedCapacity="TOTAL"
                )
                total_wcu += delete_response["ConsumedCapacity"]["CapacityUnits"]

        log.info(f"Total RCU Consumed: {total_rcu}")
        log.info(f"Total WCU Consumed: {total_wcu}")

    def count(self) -> int:
        total_count = 0
        total_rcu = 0
        scan_kwargs = {"Select": "COUNT", "ReturnConsumedCapacity": "TOTAL"}

        while True:
            response = self.table.scan(**scan_kwargs)
            total_count += response["Count"]
            total_rcu += response["ConsumedCapacity"]["CapacityUnits"]

            # Check if there are more items to scan
            if "LastEvaluatedKey" in response:
                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            else:
                break

        log.info(f"Total RCU Consumed: {total_rcu}")
        return total_count

    def list_tables(self):
        ddb = self.session.client("dynamodb")
        table_names = []

        # Initial call to list_tables
        response = ddb.list_tables()

        while True:
            table_names.extend(response["TableNames"])

            # Check if more tables are available to list
            if "LastEvaluatedTableName" in response:
                response = ddb.list_tables(
                    ExclusiveStartTableName=response["LastEvaluatedTableName"]
                )
            else:
                break

        return table_names

    def count_pk(self, pk: str) -> int:
        # Partition key value
        # pk = "AGG_DELETES#2023-11-17"

        # Initialize the total count
        total_count = 0

        # Query parameters
        query_params = {"KeyConditionExpression": Key("PK").eq(pk), "Select": "COUNT"}

        # Paginate through results and sum counts
        while True:
            response = self.table.query(**query_params)
            total_count += response["Count"]
            if "LastEvaluatedKey" not in response:
                break
            query_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]

        return total_count


if __name__ == "__main__":
    log_fmt = (
        r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
    )
    logging.basicConfig(
        format=log_fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    ddb = DdbTable("fbs-hub-test-cl-delta-processing")

    ddb.delete_table()
    ddb.create_table()
    print(ddb.list_tables())

    # ddb.clear_table()
    # print(ddb.count())
    # print(ddb.get_unique_pks())
    # print(ddb.count_pk('AGG_DELETES#2023-11-17'))
