import json
import os
from tempfile import NamedTemporaryFile
from typing import List

from django.core.files.storage import Storage, default_storage
from django.utils import timezone
import boto3
from teacher_app.models.limitation import (
    ConfigurationLimitationParameter,
    LimitationConfiguration,
    Limitation,
)


def process_configuration_file(dict: List[dict], filename: str) -> str:
    with open(filename, "w") as outfile:
        json.dump(dict, outfile)
    storage: Storage = default_storage
    with open(filename, "rb") as outfile:
        name = storage.save(filename, outfile)

    return name


def create_config_file(configuration_id: int) -> str:
    parameters_array = []
    limitation_configurations = LimitationConfiguration.objects.filter(
        configuration_id=configuration_id
    ).values_list("limitation", flat=True)
    limitations = Limitation.objects.filter(pk__in=limitation_configurations)
    for limitation in limitations:
        configuration_limitation_parameters = (
            ConfigurationLimitationParameter.objects.filter(
                limitation_parameter__limitation=limitation
            )
        )
        limitations_array = []
        for limitation_parameter in configuration_limitation_parameters:
            limitations_array.append(
                f"{limitation_parameter.limitation_parameter.parameter_in_code}={limitation_parameter.value}"
                if limitation_parameter.value.isnumeric()
                else f"{limitation_parameter.limitation_parameter.parameter_in_code}='{limitation_parameter.value}'"
            )
        parameters_array.append(
            {
                "CheckName": limitation.function_name,
                "CheckAttributes": limitations_array,
                "Action": 1,
            }
        )
    filename = f"{configuration_id}_{timezone.now()}.json"
    return process_configuration_file(parameters_array, filename)


def create_folder_for_student(group, name, surname):
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    bucket_name = "diploma-itis-bucket"
    directory_name = f"{group}_{name}_{surname}"
    s3.put_object(Bucket=bucket_name, Key=(directory_name + "/"))
    return directory_name


def add_configuration(directory_name, teacher_directory, filename):
    bucket_name = "diploma-itis-bucket"
    s3 = boto3.resource(
        "s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    bucket = s3.Bucket(bucket_name)
    copy_source = {"Bucket": bucket_name, "Key": filename}
    bucket.copy(CopySource=copy_source, Key=f"{directory_name}/config.json")


def get_results_file(directory_name):
    bucket_name = "diploma-itis-bucket"
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    get_object_response = s3.get_object(
        Bucket=bucket_name, Key=f"{directory_name}/results.json"
    )
    file = NamedTemporaryFile(suffix="json")
    file.write(get_object_response["Body"].read())
    return file
