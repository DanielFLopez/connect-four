###########
# BUILDER #
###########
FROM python:3.8-buster as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/back

# create the appropriate directories
RUN mkdir -p $APP_HOME

# copy project
COPY . $APP_HOME
WORKDIR $APP_HOME
# install dependencies
RUN apt-get update -y && apt-get install libpq-dev gcc python3-dev libc6-dev curl libpq5 netcat dos2unix postgresql-client -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache

# create the app user
RUN addgroup app && useradd app -g app

# change to the app user

RUN chmod +x $APP_HOME/entrypoint.sh
RUN dos2unix $APP_HOME/entrypoint.sh

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]