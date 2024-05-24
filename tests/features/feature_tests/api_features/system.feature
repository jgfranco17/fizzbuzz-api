Feature: Basic Configuration Testing

    Scenario: Access root endpoint
        Given I start the API
        When I send a request to "/"
        Then the response is returned with status code 200
        And the response JSON contains "message" in keys

    Scenario: Access health-check endpoint
        Given I start the API
        When I send a request to "/healthz"
        Then the response is returned with status code 200

    Scenario: Access metrics endpoint
        Given I start the API
        When I send a request to "/metrics"
        Then the response is returned with status code 200
