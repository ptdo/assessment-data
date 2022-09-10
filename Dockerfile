FROM python:latest

# TODO: Add your image build instructions here
ADD . /src
COPY . /src
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
