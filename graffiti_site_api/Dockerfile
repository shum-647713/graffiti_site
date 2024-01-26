FROM python:3.12-alpine
WORKDIR /graffiti_site_api
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["gunicorn", "graffiti_site_api.prod_wsgi"]
EXPOSE 8000
