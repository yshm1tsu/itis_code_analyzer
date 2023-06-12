import os
from multiprocessing import Process

import click
import requests
from message_queue import run_messages
from watchdog_service import observer


@click.command()
def register():
    try:
        first_name = click.prompt("Пожалуйста, введите ваше имя", type=str)
        last_name = click.prompt("Пожалуйста, введите вашу фамилию", type=str)
        patronymic = click.prompt("Пожалуйста, введите ваше отчество", type=str)
        group = click.prompt("Пожалуйста, введите номер вашей группы", type=str)
        configuration_uuid = click.prompt(
            "Пожалуйста, введите идентификатор экзамена", type=str
        )
        response = requests.post(
            data={
                "first_name": first_name,
                "last_name": last_name,
                "patronymic": patronymic,
                "group": group,
                "configuration_uuid": configuration_uuid,
            },
            url=f"{os.getenv('APP_URL')}/teacher/add_student/",
        )
        response_data = response.json()
        if "errors" in response_data:
            click.echo(response_data["errors"])
        else:
            student_directory_name = response_data["directory_name"]
            student = response_data["student"]
            configuration_file_name = response_data["configuration_file_name"]
            response = requests.post(
                data={
                    "type": "start",
                    "configuration_uuid": configuration_uuid,
                    "student": student,
                },
                url=f"{os.getenv('APP_URL')}/teacher/statistics/",
            )
            response_data = response.json()
            configuration_statistics_id = response_data["configuration_statistics_id"]
            click.echo("Вы успешно зарегистрировались")
            p1 = Process(
                target=observer,
                args=(
                    student_directory_name,
                    configuration_file_name,
                    configuration_uuid,
                    student,
                    configuration_statistics_id,
                ),
            )
            p1.start()
            p2 = Process(target=run_messages, args=(student_directory_name,))
            p2.start()
            p1.join()
            p2.join()
    except KeyboardInterrupt:
        requests.post(
            data={
                "type": "end",
                "configuration_uuid": configuration_uuid,
                "student": student,
                "configuration_statistics": configuration_statistics_id,
            },
            url=f"{os.getenv('APP_URL')}/teacher/statistics/",
        )


@click.command()
@click.option(
    "--type",
    prompt="Добро пожаловать! Пожалуйста, введите свои данные:\n",
    help="The person to greet.",
)
def auth(type):
    if type == "1":
        register()
    if type == "2":
        pass


if __name__ == "__main__":
    auth()
