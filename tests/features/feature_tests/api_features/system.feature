Feature: Basic Configuration Testing

    Background:
        Given I start the API

    Scenario: Access root endpoint
        When I send a request to "/"
        Then the response is returned with status code 200
        And the response JSON contains "message" in keys

    Scenario: Access health-check endpoint
        When I send a request to "/healthz"
        Then the response is returned with status code 200

    Scenario: Access metrics endpoint
        When I send a request to "/metrics"
        Then the response is returned with status code 200
