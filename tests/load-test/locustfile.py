import logging
from random import randint

from locust import HttpUser, between, task

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class FizzbuzzUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_fizzbuz_sequence(self):
        number = randint(1, 100)
        endpoint = f"/v0/fizzbuzz?number={number}"
        response = self.client.get(endpoint)
        if response.status_code == 200:
            logger.info(f"GET {endpoint} - success")
        else:
            logger.warning(f"GET {endpoint} - fail")
