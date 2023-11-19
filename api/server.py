from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from .computation import generate_fizzbuzz_sequence
from .models import FizzBuzzSequence, get_data_summary


def create_server() -> FastAPI:
    """
    Creates an instance of the API app.

    Returns:
        FastAPI: API app unit
    """
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Welcome to the FizzBuzz API!"}

    @app.get("/fizzbuzz", status_code=200)
    def compute(number: Optional[int] = None):
        response = {"message": "Invalid input"}
        try:
            if number is None:
                raise ValueError("No number provided.")

            if not 1 <= number <= 10**4:
                raise HTTPException(
                    status_code=404,
                    detail="Number must a positive integer from 1 to 10^4, inclusive.",
                )

            if not isinstance(number, int):
                raise HTTPException(
                    status_code=404, detail=f"Number {number} is not integer."
                )

            raw_output = generate_fizzbuzz_sequence(number)
            output_summary = FizzBuzzSequence(raw_output)
            response = get_data_summary(output_summary)

        except HTTPException as e:
            print(f"Invalid input: {e}")

        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    return app
