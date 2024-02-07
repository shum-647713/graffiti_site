FROM python:3.12-alpine

WORKDIR /graffiti_site_api

COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY graffiti_site_api/ ./

CMD ["gunicorn", "-b", "0.0.0.0:8000", "graffiti_site_api.prod_wsgi"]
EXPOSE 8000
