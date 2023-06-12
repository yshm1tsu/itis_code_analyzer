import json
import time

import boto3

from live import TableProcessor


def get_message_from_queue(student_directory_name: str):
    queue_url = "https://message-queue.api.cloud.yandex.net/b1g34fan0njvd42a1q13/dj600000000gsel10636/default"
    client = boto3.client(
        service_name="sqs",
        endpoint_url="https://message-queue.api.cloud.yandex.net",
        region_name="ru-central1",
    )
    messages = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=60,
        WaitTimeSeconds=20,
    ).get("Messages")
    if messages:
        for msg in messages:
            if msg.get("Body") == student_directory_name:
                session = boto3.session.Session()
                s3 = session.client(
                    service_name="s3", endpoint_url="https://storage.yandexcloud.net"
                )
                try:
                    get_object_response = s3.get_object(
                        Bucket="diploma-itis-bucket",
                        Key=f"{student_directory_name}/results.json",
                    )
                    body = json.load(get_object_response["Body"])
                    client.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=msg.get("ReceiptHandle")
                    )
                    return body
                except Exception as e:
                    print(e)


def run_messages(student_directory_name):
    try:
        table_processor = TableProcessor()
        while True:
            body = get_message_from_queue(student_directory_name)
            if body:
                table_processor.initialize_table()
                table_processor.update_table(body)
                table_processor.print_table()
            time.sleep(20)
    except Exception:
        print("Exited")
