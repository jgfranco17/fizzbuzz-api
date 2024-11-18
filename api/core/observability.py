from prometheus_client import Counter, Histogram


class PrometheusMetrics:
    REQUEST_COUNT = Counter(
        "http_request_count", "Total number of requests", ["method", "endpoint"]
    )
    REQUEST_LATENCY = Histogram(
        "http_request_latency_seconds",
        "Request latency in seconds",
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    )
    HEALTH_CHECK_COUNT = Counter(
        "http_service_health_check_count",
        "Total number of successful requests to the health check",
    )
