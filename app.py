import uvicorn
from api import load_args, create_server


if __name__ == "__main__":
    app = create_server()
    config = load_args()
    uvicorn.run(app, host="0.0.0.0", port=config.port)