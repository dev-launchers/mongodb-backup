FROM mongo:4.4
COPY backup.sh /usr/local/bin/
ENTRYPOINT ["backup.sh"]