Feature: API Testing

    Scenario: Access root endpoint
        When I send a request to "/"
        Then the response is returned with status code 200
        And the response JSON contains "message" in keys

    Scenario: Access root endpoint
        When I send a request to "/fizzbuzz?number=15"
        Then the response is returned with status code 200
        And the sequence contains 4 instances of "fizz"
        And the sequence contains 2 instances of "buzz"
        And the sequence contains 1 instances of "fizzbuzz"
