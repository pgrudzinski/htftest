FROM python:3.8 AS base
RUN apt-get update && apt-get install -y protobuf-compiler
WORKDIR /tests 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM base AS station
COPY . .
EXPOSE 4444
EXPOSE 10000/udp
EXPOSE 10000
CMD ["python","frontend_example.py"]

FROM base AS dashboard
EXPOSE 12000
EXPOSE 10000/udp
EXPOSE 10000
CMD python -m openhtf.output.servers.dashboard_server
