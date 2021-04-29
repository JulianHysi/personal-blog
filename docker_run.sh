#!/bin/bash
# since the command was getting too long, I scripted it
exec docker run --name personal_blog -d -p 8000:5000 --rm \
    -e SECRET_KEY=$SECRET_KEY \
    -e DATABASE_URI=$DATABASE_URI \
    -e MAIL_USERNAME=$MAIL_USERNAME \
    -e MAIL_PASSWORD=$MAIL_PASSWORD \
    -e ELASTICSEARCH_URL=$ELASTICSEARCH_URL \
    personal_blog:latest
