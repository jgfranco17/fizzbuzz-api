Feature: API Operation Testing

    Background:
        Given I start the API

    Scenario: Access numeric endpoint
        When I send a request to the fizzbuzz endpoint with value 15
        Then the response is returned with status code 200
        And the sequence contains 4 instances of "fizz"
        And the sequence contains 2 instances of "buzz"
        And the sequence contains 1 instances of "fizzbuzz"

    Scenario: Invalid input raises error
        When I send a request to the fizzbuzz endpoint with value 0
        Then the response is returned with status code 400
        And an error is raised with "number must a positive integer" in "message"
