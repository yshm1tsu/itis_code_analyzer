import json

from utils.process_request import process_request
import logging


def application(env, start_response):
    body = json.load(env["wsgi.input"])
    try:
        process_request(body)
        start_response("200 OK", [("Content-Type", "text/html")])
    except Exception as e:
        logging.log(1, e)
        start_response("400 Bad Request", [("Content-Type", "text/html")])
