FROM mongo:4.4
RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
WORKDIR /backup
COPY backup.sh /usr/local/bin/
COPY upload.py .
ENTRYPOINT ["backup.sh"]
