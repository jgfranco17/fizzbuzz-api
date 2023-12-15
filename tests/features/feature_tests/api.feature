Feature: API Testing

    Scenario: Access root endpoint
        When I send a request to "/"
        Then the response is returned with status code 200
        And the response JSON contains "Welcome" in message
