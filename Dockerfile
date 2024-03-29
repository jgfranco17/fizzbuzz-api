FROM python:3.10.6-alpine
WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt --no-cache-dir
COPY . /src
EXPOSE 5050
CMD python app.py --port 5050
