FROM python:3.8-slim

RUN adduser personal_blog

WORKDIR /home/personal_blog

# create the virtual env
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

# copy the necessary files and folders
COPY personal_blog personal_blog
COPY migrations migrations
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py
   
RUN chown -R personal_blog:personal_blog ./
USER personal_blog

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
