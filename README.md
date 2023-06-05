# places_remember
### Веб-приложение, с помощью которого люди смогут хранить свои впечатления о посещаемых местах.
## Запуск:
* Установить `python 3.11` и `pipenv` (`pip install pipenv`) 
* Установить зависимости
* Создать файл `.env` в `/src` по примеру `.env.example`
* Применить миграции
* Создать SuperUser
* Запустить сервер : `python manage.py runserver`
## Docker compose
* В командной строке перейдите в корневой каталог проекта place_remember, где находятся файлы `Dockerfile` и `docker-compose.yml`.
* Выполните команду `docker-compose up` для запуска проекта. Docker Compose создаст и запустит контейнеры на основе настроек, указанных в файле `docker-compose.yml`
### Проблемы:
* Heroku блочит регистрацию из России, а затем душит добавлением карты, PythonAnywhere не поддерживает python 3.11, RIP деплой
* GitActions для запуска тестов должны видить .env, не безопасно, но мне пришлось его добавить
* GitActions не хотят воспринимать `django.db.backends.postgresql_psycopg2` как базу данных и предлагают `django.db.backends.postgresql`, с которыми тоже не работает
