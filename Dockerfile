FROM continuumio/miniconda3

RUN adduser personal_blog

WORKDIR /home/personal_blog

COPY environment.yaml environment.yaml
RUN conda env create -f environment.yaml --name personal_blog_env

COPY personal_blog personal_blog
COPY migrations migrations
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R personal_blog:personal_blog ./
USER personal_blog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

