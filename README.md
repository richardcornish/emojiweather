# Emoji Weather ☀️

**Emoji Weather** is a website that allows a user to search, text, or call for the weather conditions.

- [Code repository](https://github.com/richardcornish/emojiweather)
- [Public domain](https://emojiweather.app)

## Local

```bash
git clone git@github.com:richardcornish/emojiweather.git
cd emojiweather/
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd emojiweather/
python manage.py migrate
python manage.py loaddata emojiweather/fixtures/*
python manage.py runserver
```

[127.0.0.1:8000](http://127.0.0.1:8000)

## Production

```bash
cd emojiweather/
source env/bin/activate
fab deploy
```