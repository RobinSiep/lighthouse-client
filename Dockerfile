FROM python:3.7

RUN apt-get update
RUN apt-get install wakeonlan

RUN addgroup lighthouse
RUN useradd -g lighthouse lighthouse

COPY . /home/lighthouse/lighthouse-client
WORKDIR /home/lighthouse

RUN pip install -e lighthouse-client

USER lighthouse

WORKDIR /home/lighthouse/lighthouse-client

EXPOSE 7103
ENTRYPOINT ["python3 main.py"]
