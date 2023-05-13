from fastapi import FastAPI
from .computation import fizzbuzz


def create_server() -> FastAPI:
    """
    Creates an instance of the API app.

    Returns:
        FastAPI: API app unit
    """
    app = FastAPI()

    def validate_url(url: str) -> tuple:
        """
        Validates the given endpoint.

        Args:
            url (str): URL to validate

        Returns:
            tuple: returns validity, as well as message and error code if needed
        """
        if url is None or url.strip() == "":
            return (False, {'message': 'Invalid data for QR code'}, 400)
        return (True, None, None)

    @app.route("/", methods=['GET'])
    def root():
        return {"message": "<h1>Welcome to the FizzBuzz API!</h1>"}

    @app.route("/fizzbuzz/{number}", methods=['GET'])
    def compute(number: int):
        response = ({"result": "none"}, 400)
        try:
            output = fizzbuzz(number)
            response = {"fizzbuzz": output}

        except TypeError as e:
            print(f'Invalid input: {e}')

        return response, 200

    return app
