FROM python:3.11.6

# Install required system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential libldap2-dev libsasl2-dev ldap-utils libpq-dev

COPY requirements.txt /module-selection/

WORKDIR /module-selection
RUN pip install --upgrade pip && pip install -r requirements.txt


