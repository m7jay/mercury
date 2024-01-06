FROM python:3.11-slim-buster
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV PYTHONUNBUFFERED 1

ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

WORKDIR /app

# install mysql dependencies
RUN apt-get update
RUN apt-get install gcc g++ default-libmysqlclient-dev -y


# install dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r ./requirements.txt

COPY . /app
