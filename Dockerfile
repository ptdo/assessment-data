FROM python:latest

# TODO: Add your image build instructions here
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "run", "--host=0.0.0.0"]