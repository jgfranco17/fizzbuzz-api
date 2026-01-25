import logging
from http import HTTPStatus
from random import randint

from locust import HttpUser, between, task
from requests import Response

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class FizzbuzzUser(HttpUser):
    """Mock user class for the API tests."""

    wait_time = between(1, 5)

    @staticmethod
    def log_response(endpoint: str, status_code: int, response: Response):
        if response.status_code == status_code:
            logger.info(f"GET {endpoint} {status_code} [success]")
        else:
            logger.error(f"GET {endpoint} {status_code} [fail: got {response.status_code}]")

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
