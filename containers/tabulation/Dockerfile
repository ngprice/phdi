FROM python:3.11-slim

WORKDIR /code

# Install git.
# TODO: remove this step when a PyPi release of PHDI is available that includes Tabulation.
RUN apt-get -y update && \
    apt-get upgrade -y && \
    apt-get -y install gcc

RUN apt-get install -y git

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get -y remove gcc && \
    apt-get -y autoremove

COPY ./app /code/app
COPY ./description.md /code/description.md

EXPOSE 8080
CMD uvicorn app.main:app --host 0.0.0.0 --port 8080