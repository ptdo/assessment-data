FROM python:latest

# TODO: Add your image build instructions here
ADD . /src
ADD . /data
COPY . /src
COPY . /data
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "./src/bootstrap.py", "./src/seed.py", ".src/analysis.py"]