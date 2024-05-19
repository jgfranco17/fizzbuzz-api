"""Main server creation setup."""
from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .computation import generate_fizzbuzz_sequence
from .models import FizzBuzzSequence, ServiceInfo, create_model_from_sequence
from .utils import read_specs


def create_server() -> FastAPI:
    """
    Creates an instance of the API app.

    Returns:
        FastAPI: API app unit
    """
    specs = read_specs("specs.json")
    app = FastAPI(
        title="Fizzbuzz API",
        summary="FizzBuzz-as-a-Service",
        description=specs["description"],
        version=specs["version"],
        contact={
            "name": "Chino Franco",
            "email": "chino.franco@gmail.com",
        },
    )

    @app.get("/", status_code=HTTPStatus.OK)
    def root():
        return {"message": "Welcome to the FizzBuzz API!"}

    @app.get("/healthz", status_code=HTTPStatus.OK)
    def root():
        return {"status": "healthy"}

    @app.get("/service-info", status_code=HTTPStatus.OK)
    def get_service_info() -> ServiceInfo:
        """
        Display the FizzBuzz API project information.

        Returns:
            ServiceInfo: Summary of project details
        """
        specs = read_specs("specs.json")
        return ServiceInfo(**specs)

    @app.get("/fizzbuzz")
    def compute(number: Optional[int] = None) -> FizzBuzzSequence:
        """
        Compute the fizzbuzz sequence until the given number.

        Args:
            number (int): Upper limit to compute sequence to, defaults to None

        Raises:
            HTTPException 400: If the number provided is not valid

        Returns:
            FizzBuzzSequence: Fizzbuzz sequence model
        """
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

        except HTTPException as http_err:
            print(f"Invalid input: {http_err.detail}")
            raise HTTPException(
                status_code=http_err.status_code,
                detail=f"Invalid input: {http_err.detail}",
            )

        raw_output = generate_fizzbuzz_sequence(number)
        output = create_model_from_sequence(raw_output)
        return output

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.detail},
        )

    return app
