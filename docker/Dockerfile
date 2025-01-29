##### Build stage #####

FROM python:3.10.6-alpine AS build

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt --no-cache-dir

COPY ./api /src/api
COPY ./app.py /src

##### Run stage #####

FROM build as app

EXPOSE 5050
CMD python app.py --port 5050
