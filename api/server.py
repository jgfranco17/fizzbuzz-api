from fastapi import FastAPI
from .computation import generate_fizzbuzz_sequence


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
    def compute(number: int = None):
        response = {"result": "none"}
        try:
            if number is None:
                raise ValueError("No number provided.")

            if not isinstance(number, int):
                raise TypeError(f'Number {number} is not integer.')
            
            output = generate_fizzbuzz_sequence(number)
            response = {
                "count": number,
                "sequence": output
            }

        except (TypeError, ValueError) as e:
            print(f'Invalid input: {e}')

        return response

    return app
