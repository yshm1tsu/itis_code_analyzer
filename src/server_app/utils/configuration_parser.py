import json
from typing import List

import boto3


def parse_configuration(filename: str) -> List:
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    get_object_response = s3.get_object(Bucket="diploma-itis-bucket", Key=filename)
    data = get_object_response["Body"].read()
    json_data = data.decode("utf-8")
    configuration = json.loads(json_data)
    try:
        for check in configuration:
            if check["CheckName"].startswith("linter"):
                check_name = check["CheckName"]
                parameters = (
                    "".join(f"{param}," for param in check["CheckAttributes"]).rstrip(
                        ","
                    )
                    if check["CheckAttributes"] != ["*=*"]
                    else ""
                )
                exec(f"from utils.analyzer.linter_functions import {check_name}")
                eval(f"{check_name}({parameters})")

    except Exception as e:
        print(e)
    return list(
        filter(lambda check: not check["CheckName"].startswith("linter"), configuration)
    )
