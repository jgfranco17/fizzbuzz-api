import time

from api.core.models import ServiceInfo


def get_service_info(start: float) -> ServiceInfo:
    info = {
        "project_name": "fizzbuzz-api",
        "description": "FastAPI-based microservice that solves the classic FizzBuzz problem via HTTP API",
        "repository_url": "https://github.com/jgfranco17/fizzbuzz-api",
        "license": "MIT",
        "version": "1.1.0",
        "languages": ["Python", "Gherkin"],
        "frameworks": ["FastAPI", "Behave"],
        "authors": [
            {
                "name": "Joaquin Franco",
                "github_username": "jgfranco17",
                "email": "chino.franco@gmail.com",
            }
        ],
        "seconds_since_start": time.time() - start,
    }
    return ServiceInfo(**info)
