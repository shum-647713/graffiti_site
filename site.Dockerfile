FROM python:3.12-alpine

WORKDIR /site

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY graffiti_site/ graffiti_site/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "graffiti_site.wsgi"]
EXPOSE 8000
