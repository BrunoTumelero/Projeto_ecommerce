FROM python:3.6-slim

#set directory
WORKDIR /app

#copy requirements
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

#install dependencies
RUN apt-get update -y && \
    apt-get install -y gnupg2 && \
    apt-get install  gcc g++ musl-dev libpq-dev git -y && \
    apt-get install -y apt-transport-https ca-certificates && \
    apt-get -y install libreadline-dev && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    sh -c echo 'deb http://apt.postgresql.org/pub/repos/apt stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list  && \
	apt-get clean && apt-get install -y wget  && \
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -  && \
    apt-get update  && \
	yes Y | apt-get install postgresql-client
    
#add app
COPY . /app