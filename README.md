# graffiti_site

graffiti_site is a small project that demonstrates example of architecture and api of a graffiti posting site

# Setup

### Installation

requirements: git

```
git clone https://github.com/shum-647713/graffiti_site
cd graffiti_site/
```

### Development

requirements: python (>= 3.10)

```
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

to run dev server:
```
python manage.py runserver
```
to check if server is running, try to access http://127.0.0.1:8000/api/

### Production

requirements: docker compose (tested with docker desktop)

create `.env` file with similar content:
```
SECRET_KEY=insecure_secret_key
POSTGRES_NAME=graffiti_site
POSTGRES_USER=django
POSTGRES_PASSWORD=insecure_password
POSTGRES_HOST=db
ALLOWED_HOSTS=*
```

to build and run in production:
```
sudo docker compose up -d --build
sudo docker compose --env-file .env exec site python manage.py migrate
sudo docker compose exec site python manage.py collectstatic
```
if build fails to download images you may need to do that manually with `docker pull`
to check if server is running, try to access http://127.0.0.1/api/

# Api

| url                                 | type      | auth  | example                                                                                                                                                                                                                                                                                           |
| ----------------------------------- | --------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /api/users/                         | GET       | None  | -> `{"count": 1, "next": null, "previous": null, "results": [{"url": "/api/users/user_name/", "username": "user_name"}, ...]}`                                                                                                                                                                    |
| /api/users/                         | POST      | None  | `{"username": "user_name", "email": "email@example.com", "password": "password"}`<br>-><br>Location: `/api/users/user_name/`<br>`{"username": "user_name", "change": "/api/users/user_name/change/", "graffiti": [], "add_graffiti": "/api/users/user_name/add_graffiti/"}`                       |
| /api/users/id/                      | GET       | None  | -> `{"username": "user_name", "change": "/api/users/user_name/change/", "graffiti": [{"url": "/api/graffiti/1/", "name": "user's graffiti"}, ...], "add_graffiti": "/api/users/user_name/add_graffiti/"}`                                                                                         |
| /api/users/id/                      | DELETE    | Owner |                                                                                                                                                                                                                                                                                                   |
| /api/users/id/activate/?token=token | POST      | None  | -> Location: `/api/users/user_name/`                                                                                                                                                                                                                                                              |
| /api/users/id/change/               | POST      | Owner | `{"username": "new_user_name", "email": "new_email@example.com", "password": "new_password", "old_password": "password"}`<br>-><br>Location: `/api/users/new_user_name/`<br>`{"username": "new_user_name"}`                                                                                       |
| /api/users/id/add_graffiti/         | POST      | Owner | `{"name": "user's graffiti"}`<br>-><br>Location: `/api/graffiti/1/`<br>`{"name": "user's graffiti", "owner": {"url": "/api/users/user_name/", "name": "user_name"}, "photos": [], "add_photo": "/api/graffiti/1/add_photo/"}`                                                                     |
| /api/graffiti/                      | GET       | None  | -> `{"count": 1, "next": null, "previous": null, "results": [{"url": "/api/graffiti/1/", "name": "user's graffiti"}, ...]}`                                                                                                                                                                       |
| /api/graffiti/                      | POST      | Any   | `{"name": "user's graffiti"}`<br>-><br>Location: `/api/graffiti/1/`<br>`{"name": "user's graffiti", "owner": {"url": "/api/users/user_name/", "name": "user_name"}, "photos": [], "add_photo": "/api/graffiti/1/add_photo/"}`                                                                     |
| /api/graffiti/id/                   | GET       | None  | -> `{"name": "user's graffiti", "owner": {"url": "/api/users/user_name/", "name": "user_name"}, "photos": [{"url": "/api/photos/1/", "image": "/media/images/hash_of_image.png"}, ...], "add_photo": "/api/graffiti/1/add_photo/"}`                                                               |
| /api/graffiti/id/                   | PUT/PATCH | Owner | `{"name": "new name for user's graffiti"}`<br>-><br>`{"name": "new name for user's graffiti", "owner": {"url": "/api/users/user_name/", "name": "user_name"}, "photos": [{"url": "/api/photos/1/", "image": "/media/images/hash_of_image.png"}, ...], "add_photo": "/api/graffiti/1/add_photo/"}` |
| /api/graffiti/id/                   | DELETE    | Owner |                                                                                                                                                                                                                                                                                                   |
| /api/graffiti/id/add_photo/         | POST      | Owner | `{"image": *image*}`<br>-><br>Location: `/api/photo/1/`<br>`{"image": "/media/images/hash_of_image.png", "graffiti": {"url": "/api/graffiti/1/", "name": "user's graffiti"}}`                                                                                                                     |
| /api/photo/                         | GET       | None  | -> `{"count": 1, "next": null, "previous": null, "results": [{"url": "/api/photo/1/", "image": "/media/images/hash_of_image.png"}, ...]}`                                                                                                                                                         |
| /api/photo/id/                      | GET       | None  | -> `{"image": "/media/images/hash_of_image.png", "graffiti": {"url": "/api/graffiti/1/", "name": "user's graffiti"}}`                                                                                                                                                                             |
| /api/photo/id/                      | DELETE    | Owner |                                                                                                                                                                                                                                                                                                   |
