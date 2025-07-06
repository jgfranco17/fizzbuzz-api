# FizzBuzz API

![STATUS](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)
![LICENSE](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

</div>

---

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Testing](#testing)
- [Authors](#authors)

## About

The whole point of this project is to showcase the concepts of SWE and DevOps that I have learned
so far. This project features CI/CD workflows and automations, unittesting, and containerization.
Git & Github were used as the VCS, and a Docker Hub image is published for container deployment.
I dub this as "FizzBuzz-as-a-Service".

This program aims to create a FastAPI-based microservice that solves the FizzBuzz algorithm. The
FizzBuzz problem is a common coding challenge often used in interviews to evaluate a candidate's
basic programming skills. The task is to write a program that prints numbers from `1` to `n`;
however, for multiples of `3`, it should print `"Fizz"` instead of the number, for multiples of
`5`, it should print `"Buzz"`, and for numbers that are multiples of both `3` and `5`, it would
print `"FizzBuzz"`. The FizzBuzz API provides a simple HTTP API to solve the FizzBuzz problem.
It allows users to make requests to the microservice and receive the resulting FizzBuzz sequence
as a response. This microservice can be easily integrated into other applications or used for
testing and learning purposes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for
development and testing purposes.

### Prerequisites

Before running the FizzBuzz Microservice API, make sure you have the following prerequisites
installed:

- [Python 3.9](https://www.python.org/downloads/) or above
- [Poetry](https://python-poetry.org/) dependency manager
- [Just](https://github.com/casey/just) command runner

### Installing

To get started with this project, clone the repository to your local machine and install the required
dependencies.

```bash
git clone https://github.com/jgfranco17/fizzbuzz-api.git
cd fizzbuzz-api
poetry install
poetry shell
```

## Usage

### Dev mode

To run the API server in dev mode, simply execute either of the following commands:

```bash
# Default Python execution
python app.py --port <PORT>

# Or use the Justfile command
just run-debug
```

### Build with Docker

To run the microservice in a container, the package comes with both a Dockerfile and a Compose YAML
configuration. Run either of the following to get the API launched in a container; by default, the
API will be set to listen on port `5050` for the Compose.

```bash
# Plain Docker build
docker build -t fizzbuzz-api .
docker run -p 5050:5050 fizzbuzz-api

# Docker-Compose build
docker compose up
```

The Docker image is also available on [Docker Hub](https://hub.docker.com/r/jgfranco17/fizzbuzz-api).
The port used in the Dockerfile is `5050`.

```bash
docker pull jgfranco17/fizzbuzz-api:latest
docker run -p 5050:5050 jgfranco17/fizzbuzz-api:latest
```

### Calling the API

Once the microservice is launched, the API is now reachable. To get a FizzBuzz sequence, simply send
a `GET` request to the server, with the number as a parameter.

```bash
curl http://localhost:<PORT>/fizzbuzz?number=<number>
```

## Testing

### Running unittest suite

In order to run diagnostics and unittests, first install the testing dependencies. This will allow
you to utilize the full capacity of the test modules we have built. To run the full test suite,
run the Justfile command as follows:

```bash
just pytest
```

### Using PyTest

You can run these tests using the [PyTest](https://docs.pytest.org/en/7.3.x/) CLI tool. To run all
tests in the directory containing the test files, navigate to the directory and enter `pytest` in
the command line. Prepending `just` ensures that the Pytest used is the one from the current
dev environment.

```bash
# Run all tests in the testing module with verbose detail
just pytest -vv

# Or, run a specific test file
just pytest -v <filepath>
```

This will run the specified test module and generates a detailed result report in the terminal.

### Running Behave suite

Behave is a Python-based BDD framework that allows you to write tests in a natural language style
using Gherkin syntax. Gherkin uses a simple, human-readable format that is easy for both technical
and non-technical stakeholders to understand. Behave translates these plain-text scenarios into
executable code, allowing teams to collaborate on defining and implementing software features.

To run the full Behave suite, run the Justfile command as follows:

```bash
just behave
```

This will run the specified test module and generates a detailed result report in the terminal.

#### Why BDD?

Behavior-Driven Development (BDD) is a software development methodology that focuses on collaboration
among developers, QA, and non-technical stakeholders. BDD aims to foster and enhance communication
and understanding by using natural language descriptions of software behaviors and features. BDD
allows teams to define the expected behavior of the software before implementation; clear specifications
help developers focus on delivering features that meet business requirements. Non-technical team members
can also easily understand and contribute to the specification process.

For example, below is a demonstration of a simple test case for pinging the `/healthz` endpoint.

```gherkin
Scenario: Access health-check endpoint
    Given I start the API
    When I send a request to "/healthz"
    Then the response is returned with status code 200
```

Using Gherkin allows us to run simple test cases without diving too deep into the technicals. As long
as the test-writer is familiarized with the basic test steps that can be used, there is no need to use
more complex testing frameworks for routine tests. Feel free to write your own Gherkin steps for this
project!

### Load-testing with Locust

Load testing is a type of performance testing that evaluates how a system behaves under a specific load.
The primary goal is to ensure the system can handle expected user traffic and identify potential bottlenecks
or performance issues before they affect end users. During load test execution, the system is subjected to
increasing numbers of simultaneous users or transactions to determine its capacity, stability, and
scalability.

For this project, we use [Locust](https://locust.io/), an open-source load testing tool that is highly
flexible and scalable, making it a popular choice for load testing web applications, APIs, and other
services.

## CI/CD

This project uses Github Actions for DevOps automations. On push to main, the following pipeline is enacted.

- Run build and test
- Codebase linting
- Coverage reporting
- Deployment to [hosting service](https://fizzbuzz-api.onrender.com/)

Smoke tests and load tests are run periodically on schedule.

## Authors

- [Chino Franco](https://github.com/jgfranco17)
