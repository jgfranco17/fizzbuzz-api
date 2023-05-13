<h1 align="center">FizzBuzz API</h1>

<div align="center">

![STATUS](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)
![LICENSE](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

</div>

---

## 📝 Table of Contents

* [About](#about)
* [Getting Started](#getting_started)
* [Usage](#usage)
* [Authors](#authors)

## 🔎 About <a name = "about"></a>

This project aims to create a FastAPI-based microservice that solves the classic FizzBuzz programming problem. The FizzBuzz problem is a common coding challenge often used in interviews to evaluate a candidate's basic programming skills. The task is to write a program that prints numbers from 1 to n; however, for multiples of 3, it should print "Fizz" instead of the number, for multiples of 5, it should print "Buzz," and for numbers that are multiples of both 3 and 5, it should print "FizzBuzz."

The FizzBuzz Microservice API provides a simple HTTP-based API to solve the FizzBuzz problem. It allows users to make requests to the microservice and receive the FizzBuzz sequence as a response. This microservice can be easily integrated into other applications or used for testing and learning purposes.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the FizzBuzz Microservice API, make sure you have the following prerequisites installed:

* Python 3.8 or above
* pip package manager

### Installing

To get started with this project, clone the repository to your local machine and install the required dependencies.

```bash
git clone https://github.com/jgfranco17/fizzbuzz-api.git
cd fizzbuzz-api
pip install -r requirements.txt
```

## 🚀 Usage <a name = "usage"></a>

### CLI usage

To run the API server in dev mode, simply execute either of the following commands:

```bash
# Default Python execution
python app.py --port PORT

# Or, after editing the Makefile to set a port number
make run
```

## Calling the API

To get a FizzBuzz sequence, simply send a `GET` request to the server, with the number as a parameter.

```text
http://localhost:<PORT>/fizzbuzz?number=<number>
```

## ✒️ Authors <a name = "authors"></a>

* [Chino Franco](https://github.com/jgfranco17) 
