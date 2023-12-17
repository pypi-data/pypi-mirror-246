import json
import logging
import time

import boto3

log = logging.getLogger(__name__)

SQS_MAX_NUMBER = 10
# Create SQS client
session = boto3.Session(profile_name="fbs-prod-userfull")
sqs = boto3.client("sqs")

# URL of your SQS queue
queue_url = "fbs-hub-e2e-correction-layer-data-dlq"


def read_messages(consume: bool = False) -> list:
    counter = 0
    all_messages = []
    start_time = time.perf_counter()

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=SQS_MAX_NUMBER,  # Max number of messages to return in each call
            WaitTimeSeconds=5,  # Use long polling
            VisibilityTimeout=30,  # Visibility timeout to 30 seconds
        )
        counter += 1
        if counter % 100 == 0:
            log.info(f"Messages read: {counter * SQS_MAX_NUMBER}")

        # Check if any messages are returned
        if "Messages" in response and len(response["Messages"]) > 0:
            all_messages.extend(response["Messages"])

            # Optionally delete messages after processing
            if consume:
                for message in response["Messages"]:
                    sqs.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
                    )
        else:
            # Break out of the loop if no more messages are available
            log.info(f"duration: {time.perf_counter() - start_time}")
            break
    return all_messages


if __name__ == "__main__":
    log_fmt = (
        r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
    )
    datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=log_fmt, level=logging.INFO, datefmt=datefmt)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)

    file_path = (
        ROOT_DIR
        / "output"
        / f"messages.{queue_url}.{time.strftime('%Y%m%d_%H%M%S')}.json"
    )

    messages = read_messages(consume=False)

    with open(file_path, "w") as f:
        json.dump(messages, f, indent=4)

    # Print the last 5 messages
    for message in messages[-1:]:
        print("Message Received: ", message["Body"])
