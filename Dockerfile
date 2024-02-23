FROM python:3.11.6
WORKDIR /code

# Install system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential libldap2-dev libsasl2-dev ldap-utils libpq-dev

# Install python packages
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app code
COPY ./*.py /code/
COPY ./alembic.ini /code/
COPY ./migrations /code/migrations
COPY ./app /code/app

CMD ["gunicorn", "--config", "gunicorn_config.py", "main:app"]
