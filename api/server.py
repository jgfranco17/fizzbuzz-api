"""Main server creation setup."""
import time
from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .computation import generate_fizzbuzz_sequence
from .models import (
    FizzBuzzSequence,
    HealthCheck,
    ServiceInfo,
    create_model_from_sequence,
)
from .observability import PrometheusMetrics
from .system import get_service_info


def __set_v0_routes() -> APIRouter:
    router_v0 = APIRouter(prefix="/v0", tags=["FIZZBUZZ"])

    @router_v0.get("/fizzbuzz")
    def compute(number: Optional[int] = None) -> FizzBuzzSequence:
        """
        Compute the fizzbuzz sequence until the given number.

        Args:
            number (int): Upper limit to compute sequence to, defaults to None

        Raises:
            HTTPException 400: If the number provided is not valid

        Returns:
            FizzBuzzSequence: Fizzbuzz sequence model
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
                    detail=f" {number} is not integer.",
                )

        except HTTPException as http_err:
            print(f"Invalid input: {http_err.detail}")
            raise HTTPException(
                status_code=http_err.status_code,
                detail=f"Invalid input: {http_err.detail}",
            )

        raw_output = generate_fizzbuzz_sequence(number)
        output = create_model_from_sequence(raw_output)
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
        return {"message": "Welcome to the FizzBuzz API!"}

    @app.get("/healthz", status_code=HTTPStatus.OK, tags=["SYSTEM"])
    def health_check() -> HealthCheck:
        """
        Health check for the API.

        Returns:
            HealthCheck: API status
        """
        return HealthCheck(status="healthy")

    @app.get("/service-info", status_code=HTTPStatus.OK, tags=["SYSTEM"])
    def service_info() -> ServiceInfo:
        """
        Display the FizzBuzz API project information.

        Returns:
            ServiceInfo: Summary of project details
        """
        return get_service_info(startup_time)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
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
