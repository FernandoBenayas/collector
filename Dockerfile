FROM python:3.4

RUN pip install --upgrade pip

ADD . /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt
CMD ["python", "/usr/src/app/app.py"]
EXPOSE 4000
