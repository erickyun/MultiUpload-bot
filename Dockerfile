FROM ubuntu:20.04
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install python3-pip curl
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pycryptodomex pillow pyrogram tgcrypto pycryptodomex python-dotenv

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

RUN ["chmod", "+x", "start.sh"]
CMD ["bash", "start.sh"]
