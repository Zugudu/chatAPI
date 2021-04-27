FROM alpine:3.13.5

RUN apk add --upgrade python3 py3-pip
RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir gunicorn

COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

COPY src/ /opt/app/

EXPOSE 5000
WORKDIR /opt/app/
ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:5000 wsgi:app" ]