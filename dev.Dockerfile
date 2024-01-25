FROM python:3.10

# Install required system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential libldap2-dev libsasl2-dev ldap-utils libpq-dev

COPY requirements.txt /tutoring/

# Copy app code
COPY ./*.py  /tutoring/
COPY ./app  /tutoring/app

WORKDIR /tutoring
RUN pip install --upgrade pip && pip install -r requirements.txt


