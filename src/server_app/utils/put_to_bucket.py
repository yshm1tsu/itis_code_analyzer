import boto3

session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


def put_result_to_bucket(file, student_directory_name: str):
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    s3.upload_file(file, "diploma-itis-bucket", f"{student_directory_name}/{file}")
