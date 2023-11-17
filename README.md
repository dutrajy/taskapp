# Task App

Install:
    - Python
    - PostgreSQL
    - RabbitMQ

Create the database:

```sql
CREATE USER taskapp WITH PASSWORD 'taskapp';

CREATE DATABASE taskapp WITH OWNER taskapp;

GRANT ALL PRIVILEGES ON DATABASE taskapp TO taskapp;
```

Run migrations:

```sh
flask db upgrade
```

Run flask server:
```sh
flask run
```

In another terminal run celery worker:
```sh
celery --app app.celery worker --loglevel=info
```

Open http://localhost:5000/
