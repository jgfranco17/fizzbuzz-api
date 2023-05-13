from api import load_args, create_server


if __name__ == "__main__":
    app = create_server()
    config = load_args()
    app.run(port=config.port)