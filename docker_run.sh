#!/bin/bash
# since the command was getting too long, I scripted it
exec docker run --name personal_blog -d -p 8000:5000 --rm \
    -v ~/Projects/personal_blog/personal_blog/static:/home/personal_blog/personal_blog/static:rw \
    -e SECRET_KEY=$SECRET_KEY \
    -e DATABASE_URI=$DATABASE_URI \
    -e MAIL_USERNAME=$MAIL_USERNAME \
    -e MAIL_PASSWORD=$MAIL_PASSWORD \
    --link elasticsearch:elasticsearch \
    -e ELASTICSEARCH_URL=http://elasticsearch:9200 \
    personal_blog:latest
