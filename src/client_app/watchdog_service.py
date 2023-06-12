import os
import sys
import time

import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from message_queue import get_message_from_queue
from utils.cloud_storage import put_file_to_bucket


class MyHandler(FileSystemEventHandler):
    student_directory_name = None
    configuration_file_name = None
    configuration_uuid = None

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            put_file_to_bucket(event.src_path, self.student_directory_name)
            requests.post(
                url=os.getenv("CONTAINER_URL"),
                json={
                    "student_directory_name": self.student_directory_name,
                    "configuration_file_name": self.configuration_file_name,
                },
            )
            time.sleep(5)
            get_message_from_queue(self.student_directory_name)


def observer(
    student_directory_name,
    configuration_file_name,
    configuration_uuid,
    student,
    configuration_statistics_id,
):
    try:
        event_handler = MyHandler()
        event_handler.student_directory_name = student_directory_name
        event_handler.configuration_file_name = configuration_file_name
        observer = Observer()
        observer.schedule(
            event_handler,
            path=sys.argv[1] if len(sys.argv) > 1 else ".",
            recursive=True,
        )
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            requests.post(
                data={
                    "type": "end",
                    "configuration_uuid": configuration_uuid,
                    "student": student,
                    "configuration_statistics": configuration_statistics_id,
                },
                url=f"{os.getenv('APP_URL')}/teacher/statistics/",
            )
        observer.join()
    except Exception as e:
        print(e)
