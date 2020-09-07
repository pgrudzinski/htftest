FROM python:3.8-slim-buster AS station
RUN set -ex; \
    apt-get update ; \
    apt-get install -y --install-recommends \
    	protobuf-compiler \
; \
    rm -rf /var/lib/apt/lists/*
WORKDIR /home/tests 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 4444 10000/udp
CMD ["python","frontend_example.py"]

