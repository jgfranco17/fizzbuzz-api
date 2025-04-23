import logging
from http import HTTPStatus
from random import randint

import requests
from locust import HttpUser, between, task

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class FizzbuzzUser(HttpUser):
    wait_time = between(1, 5)

    @staticmethod
    def log_response(endpoint: str, status_code: int, response: requests.Response):
        if response.status_code == status_code:
            logger.info(f"GET {endpoint} - success")
        else:
            logger.warning(f"GET {endpoint} - fail")

    @task(10)
    def test_get_service_info(self):
        endpoint = f"/service-info"
        response = self.client.get(endpoint)
        self.log_response(endpoint, HTTPStatus.OK, response)

    @task(90)
    def test_get_fizzbuz_sequence(self):
        number = randint(10, 50)
        endpoint = f"/v0/fizzbuzz?number={number}"
        response = self.client.get(endpoint)
        self.log_response(endpoint, HTTPStatus.OK, response)
