Feature: Basic Configuration Testing

    Background:
        Given I start the API

    Scenario: Access root endpoint
        When I send a request to the index endpoint
        Then the response is returned with status code 200
        And the response JSON contains "message" in keys

    Scenario: Access health-check endpoint
        When I send a request to the health-check endpoint
        Then the response is returned with status code 200

    Scenario: Access metrics endpoint
        When I send a request to the metrics endpoint
        Then the response is returned with status code 200
