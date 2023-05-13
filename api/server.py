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

    @app.get("/fizzbuzz/{number}")
    def compute(number: int):
        response = ({"result": "none"}, 400)
        try:
            if not isinstance(number, int):
                raise TypeError(f'Number given must be integer.')
            
            output = generate_fizzbuzz_sequence(number)
            response = {
                "count": number,
                "sequence": output
            }

        except TypeError as e:
            print(f'Invalid input: {e}')

        return response, 200

    return app
