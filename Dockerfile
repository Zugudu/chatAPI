FROM alpine:3.13.5

RUN apk add --upgrade python3 py3-pip
RUN pip3 install --upgrade pip3

COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

COPY ./src/core.py /opt/app

EXPOSE 5000
CMD [ "python3", "/opt/app/core.py" ]