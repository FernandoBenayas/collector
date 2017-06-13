FROM python:3.4

MAINTAINER Manuel García-Amado

RUN pip install --upgrade pip

RUN apt-get update && apt-get -y install zip default-jre

ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN python /usr/src/app/setup.py install
RUN wget -q https://artifacts.elastic.co/downloads/logstash/logstash-5.4.1.zip
RUN unzip *.zip && rm *.zip
RUN logstash-5.4.1/bin/logstash-plugin install logstash-output-elasticsearch
CMD ["logstash-5.4.1/bin/logstash",  "-f", "logstash-collector.conf"]
