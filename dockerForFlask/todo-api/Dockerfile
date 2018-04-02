# python:alpine is 3.{latest}
FROM python:latest

LABEL maintainer="Jeeva S. Chelladhurai"

RUN pip3 install flask

COPY src /src/

RUN pip3 install -r /src/requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "/src/app.py"]