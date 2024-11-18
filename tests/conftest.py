import pytest
from fastapi.testclient import TestClient
from prometheus_client import CollectorRegistry, Counter, Histogram

from api import create_server
from api.core.observability import PrometheusMetrics


@pytest.fixture
def client():
    app = create_server()
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_registry():
    # Create a custom registry for testing
    registry = CollectorRegistry()

    # Re-register the metrics to the custom registry
    PrometheusMetrics.REQUEST_COUNT = Counter(
        "http_request_count",
        "Total number of requests",
        ["method", "endpoint"],
        registry=registry,
    )
    PrometheusMetrics.REQUEST_LATENCY = Histogram(
        "http_request_latency_seconds",
        "Request latency in seconds",
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        registry=registry,
    )
    PrometheusMetrics.HEALTH_CHECK_COUNT = Counter(
        "http_service_health_check_count",
        "Total number of successful requests to the health check",
        registry=registry,
    )
