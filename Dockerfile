FROM python:3.11.0a6-alpine3.15
RUN sudo apt-get update && sudo apt-get install -y python3-pip 
WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt --no-cache-dir
COPY . /src
CMD python app.py --port 5050