FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install python3 python3-pip && \
    apt-get -y install cron

WORKDIR /graffiti_site_cron

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY crontask.py ./
RUN chmod 0744 ./crontask.py
RUN echo "*/15 * * * * /graffiti_site_cron/crontask.py" | crontab -

COPY graffiti_site_api/ ./

CMD ["cron", "-f"]
