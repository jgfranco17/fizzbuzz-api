"""Main server creation setup."""

import logging
import os
from http import HTTPStatus
from typing import Tuple

from fastapi import APIRouter
from redis import Redis

from api.core.computation import generate_fizzbuzz_sequence
from api.core.constants import EnvironmentVariables, RedisConfigs
from api.core.models import FizzBuzzSequence
from api.errorhandling.errors import ErrorResponse

logger = logging.getLogger(__name__)
redis_client = Redis(
    host=os.getenv(EnvironmentVariables.REDIS_HOST, RedisConfigs.LOCAL),
    port=RedisConfigs.DEFAULT_PORT,
    decode_responses=True,
)


def __should_use_cache() -> bool:
    """Helper function to determine if cache should be used.

    Separated the logic in case the cache condition changes
    later down the line.
    """
    host_from_env = os.getenv(EnvironmentVariables.REDIS_HOST)
    return host_from_env == RedisConfigs.LOCAL


def __validate_number_input(value: int) -> Tuple[bool, str]:
    if value is None:
        return False, "no number provided"
    if not 1 <= value <= 10**4:
        return False, "number must a positive integer from 1 to 10^4, inclusive"
    return True, ""


router_v0 = APIRouter(prefix="/v0", tags=["FIZZBUZZ"])


@router_v0.get("/fizzbuzz")
def compute(number: int) -> FizzBuzzSequence:
    """Compute the fizzbuzz sequence until the given number."""

    is_valid, error_message = __validate_number_input(number)
    if not is_valid:
        logger.error(f"Invalid input: {error_message}")
        error_data = ErrorResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            text=error_message,
            solution="Please provide a valid 'number' query parameter and try again",
        )
        raise error_data.as_http_exception()

    cache_key = f"fizzbuzz:{number}"
    if __should_use_cache():
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.debug(f"Key '{cache_key}' found in redis, using cached value")
            return FizzBuzzSequence.model_validate_json(str(cached_result))

    logger.debug(f"Key for number={number} not found, will calculate")
    raw_output = generate_fizzbuzz_sequence(number)
    output = FizzBuzzSequence.from_sequence(raw_output)
    if __should_use_cache():
        redis_client.set(cache_key, output.model_dump_json(), ex=3600)
    return output
