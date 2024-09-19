"""Main server creation setup."""
import logging
import os
import time
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from redis import Redis

from .computation import generate_fizzbuzz_sequence
from .constants import EnvironmentVariables
from .models import (
    FizzBuzzSequence,
    HealthCheck,
    ServiceInfo,
    create_model_from_sequence,
)
from .observability import PrometheusMetrics
from .system import get_service_info

logger = logging.getLogger(__name__)
redis_client = Redis(
    host=os.getenv(EnvironmentVariables.REDIS_HOST), port=6379, decode_responses=True
)


def __set_v0_routes() -> APIRouter:
    router_v0 = APIRouter(prefix="/v0", tags=["FIZZBUZZ"])

    @router_v0.get("/fizzbuzz")
    def compute(number: Optional[int] = None) -> FizzBuzzSequence:
        """
        Compute the fizzbuzz sequence until the given number.
        """
        try:
            if number is None:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="no number provided",
                )

            if not 1 <= number <= 10**4:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="number must a positive integer from 1 to 10^4, inclusive.",
                )

            if not isinstance(number, int):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"{number} is not integer.",
                )

        except HTTPException as http_err:
            print(f"Invalid input: {http_err.detail}")
            raise HTTPException(
                status_code=http_err.status_code,
                detail=f"Invalid input: {http_err.detail}",
            )

        # Check cache
        cache_key = f"fizzbuzz:{number}"
        if os.getenv(EnvironmentVariables.REDIS_HOST) == "localhost":
            cached_result = redis_client.get(cache_key)
            if cached_result:
                logger.info(f"Key '{cache_key}' found in redis, using cached value")
                return FizzBuzzSequence.model_validate_json(cached_result)

        logger.debug(f"Key for number={number} not found, will calculate")
        raw_output = generate_fizzbuzz_sequence(number)
        output = create_model_from_sequence(raw_output)
        redis_client.set(cache_key, output.model_dump_json(), ex=3600)
        return output

    return router_v0


def __init_base_app() -> FastAPI:
    specs = get_service_info(0.0)
    app = FastAPI(
        title="Fizzbuzz API",
        summary="FizzBuzz-as-a-Service",
        description=specs.description,
        version=specs.version,
        contact={
            "name": "Chino Franco",
            "email": "chino.franco@gmail.com",
        },
    )
    startup_time = time.time()

    @app.get("/", status_code=HTTPStatus.OK, tags=["SYSTEM"])
    def root():
        """
        Project main page.
        """
        return {"message": "Welcome to the FizzBuzz API!"}

    @app.get("/healthz", status_code=HTTPStatus.OK, tags=["SYSTEM"])
    def health_check() -> HealthCheck:
        """
        Health check for the API.
        """
        return HealthCheck(status="healthy")

    @app.get("/service-info", status_code=HTTPStatus.OK, tags=["SYSTEM"])
    def service_info() -> ServiceInfo:
        """
        Display the FizzBuzz API project information.
        """
        return get_service_info(startup_time)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """
        Exception handler.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.detail},
        )

    return app


def create_server() -> FastAPI:
    """
    Creates an instance of the API app.

    Returns:
        FastAPI: API app unit
    """
    app = __init_base_app()

    @app.middleware("http")
    async def add_prometheus_metrics(request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        if "healthz" in endpoint:
            PrometheusMetrics.HEALTH_CHECK_COUNT.inc()
        else:
            PrometheusMetrics.REQUEST_COUNT.labels(
                method=method, endpoint=endpoint
            ).inc()
        with PrometheusMetrics.REQUEST_LATENCY.time():
            response = await call_next(request)
        return response

    @app.get("/metrics")
    async def get_metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    main_routes = [
        __set_v0_routes(),
    ]
    for router in main_routes:
        app.include_router(router)
        print(f"Registered group: {router.prefix}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this to restrict origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
