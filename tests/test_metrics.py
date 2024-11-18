from prometheus_client.exposition import generate_latest

from api.core.observability import PrometheusMetrics


def test_request_count_increment():
    method = "GET"
    endpoint = "/service-info"

    PrometheusMetrics.REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    metrics = generate_latest()
    assert b"http_request_count_total" in metrics


def test_request_latency_observe():
    latency = 0.05

    PrometheusMetrics.REQUEST_LATENCY.observe(latency)

    metrics = generate_latest()
    assert b"http_request_latency_seconds_sum" in metrics, str(metrics)
