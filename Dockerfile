FROM python:latest

# TODO: Add your image build instructions here
ADD . /src
ADD . /data
COPY . .
WORKDIR /src
RUN dir /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "bootstrap.py", "seed.py", "analysis.py", "test.py"]