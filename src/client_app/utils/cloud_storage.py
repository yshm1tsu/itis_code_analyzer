import boto3


def put_file_to_bucket(file: str, directory: str):
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    filename = file.split("/")[-1]
    s3.upload_file(file, "diploma-itis-bucket", f"{directory}/{filename}")
