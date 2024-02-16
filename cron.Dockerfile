FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install python3 python3-pip && \
    apt-get -y install cron

WORKDIR /cron

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY delete_expired_tokens.py .
RUN chmod 0744 delete_expired_tokens.py
RUN echo "*/15 * * * * /cron/delete_expired_tokens.py" | crontab -

COPY graffiti_site/ graffiti_site/

CMD ["cron", "-f"]
