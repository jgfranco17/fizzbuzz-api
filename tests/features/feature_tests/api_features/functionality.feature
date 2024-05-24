Feature: API Operation Testing

    Scenario: Access numeric endpoint
        Given I start the API
        When I send a request to "/v0/fizzbuzz?number=15"
        Then the response is returned with status code 200
        And the sequence contains 4 instances of "fizz"
        And the sequence contains 2 instances of "buzz"
        And the sequence contains 1 instances of "fizzbuzz"

    Scenario: Invalid input raises error
        Given I start the API
        When I send a request to "/v0/fizzbuzz?number=0"
        Then the response is returned with status code 400
        And an error is raised with "number must a positive integer" in "message"

    Scenario: Attempt non-existent route
        Given I start the API
        When I send a request to "/fake-endpoint"
        Then the response is returned with status code 404
        And an error is raised with "Not Found" in "detail"
