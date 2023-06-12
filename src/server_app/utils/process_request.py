import json
import os
import subprocess
import time
from utils.configuration_parser import parse_configuration
from utils.template_render import render_template
from utils.put_to_bucket import put_result_to_bucket
import boto3

from utils.message_queue import send_message

from utils.linter import process_linter_results


def process_request(body):
    student_directory_name = body["student_directory_name"]
    configuration_file_name = body["configuration_file_name"]
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    configuration = parse_configuration(configuration_file_name)
    render_template(configuration, student_directory_name)
    keys = []
    for key in s3.list_objects(
        Bucket="diploma-itis-bucket", Prefix=f"{student_directory_name}/"
    )["Contents"]:
        filename = key["Key"]
        if filename.endswith(".py"):
            keys.append(filename)

    results = {}
    if not os.path.exists(student_directory_name):
        os.mkdir(student_directory_name)
    for key in keys:
        get_object_response = s3.get_object(Bucket="diploma-itis-bucket", Key=key)
        content = get_object_response["Body"].read().decode("utf-8")
        with open(key, "w") as py_file:
            py_file.write(content)
        from executable import process_file

        try:
            process_file(results, content, key)
        except Exception as e:
            print(e)
    print(results)
    try:
        linting_results = subprocess.run(
            ["flake8", "--config", "config.flake8", f"{student_directory_name}"],
            text=True,
            capture_output=True,
        )
        with open("results_linter.txt", "w") as results_file:
            results_file.write(linting_results.stdout)
        process_linter_results("results_linter.txt", results)
    except Exception as e:
        print(e)

    with open("results.json", "w") as results_file:
        json.dump(results, results_file)
    put_result_to_bucket("results.json", student_directory_name)
    time.sleep(5)
    message = student_directory_name
    send_message(message)
