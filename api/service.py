import logging
import os
import time
from http import HTTPStatus
from typing import Any, Callable, Dict

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from api.core.models import HealthCheck
from api.observability.metrics import PrometheusMetrics
from api.routes.system import get_service_info
from api.routes.v0.fizzbuzz import router_v0

specs = get_service_info(time.time())

app = FastAPI(
    title="Fizzbuzz API",
    summary="FizzBuzz-as-a-Service",
    description=specs["description"],
    version=specs["version"],
    contact={
        "name": "Chino Franco",
        "email": "chino.franco@gmail.com",
    },
)
startup_time = time.time()


@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next: Callable[[Request], Any]):
    method = request.method
    endpoint = request.url.path
    if "healthz" in endpoint:
        PrometheusMetrics.HEALTH_CHECK_COUNT.inc()
    else:
        PrometheusMetrics.REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    with PrometheusMetrics.REQUEST_LATENCY.time():
        response = await call_next(request)
    return response


@app.get("/", status_code=HTTPStatus.OK, tags=["SYSTEM"])
def root():
    """Project main page."""
    return {"message": "Welcome to the FizzBuzz API!"}


@app.get("/healthz", status_code=HTTPStatus.OK, tags=["SYSTEM"])
def health_check() -> HealthCheck:
    """Health check for the API."""
    return HealthCheck(status="healthy")


@app.get("/service-info", status_code=HTTPStatus.OK, tags=["SYSTEM"])
def service_info() -> Dict[str, Any]:
    """Display the FizzBuzz API project information."""
    return get_service_info(startup_time)


@app.get("/metrics")
async def get_metrics():
    """Get the metrics using Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """General exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "message": exc.detail},
    )


app.include_router(router_v0)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
