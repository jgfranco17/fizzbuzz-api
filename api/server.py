from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from .computation import generate_fizzbuzz_sequence
from .models import FizzBuzzSequence


def create_server() -> FastAPI:
    """
    Creates an instance of the API app.

    Returns:
        FastAPI: API app unit
    """
    app = FastAPI()

    @app.get("/", status_code=HTTPStatus.OK)
    def root():
        return {"message": "Welcome to the FizzBuzz API!"}

    @app.get("/fizzbuzz", status_code=HTTPStatus.OK)
    def compute(number: Optional[int] = None):
        response = {"message": "Invalid input"}
        try:
            if number is None:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="no number provided",
                )

            if not 1 <= number <= 10**4:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="number must a positive integer from 1 to 10^4, inclusive.",
                )

            if not isinstance(number, int):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f" {number} is not integer.",
                )

            raw_output = generate_fizzbuzz_sequence(number)
            output_summary = FizzBuzzSequence(raw_output)
            response = output_summary.get_data_summary()

        except HTTPException as http_err:
            print(f"Invalid input: {http_err.detail}")
            return {
                "status": http_err.status_code,
                "message": f"Invalid input, {http_err.detail}",
            }

        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    return app
