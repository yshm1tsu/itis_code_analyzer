import boto3


def send_message(message_body):
    # Create client
    client = boto3.client(
        service_name="sqs",
        endpoint_url="https://message-queue.api.cloud.yandex.net",
        region_name="ru-central1",
    )
    client.send_message(
        QueueUrl="https://message-queue.api.cloud.yandex.net/b1g34fan0njvd42a1q13/dj600000000gsel10636/default",
        MessageBody=message_body,
    )
