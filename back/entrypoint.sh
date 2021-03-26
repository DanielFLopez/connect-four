#!/bin/sh

until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -c '\q'; do
  echo "Waiting for postgres server"
  sleep 1
done

echo "WITH RELOAD"
gunicorn back.asgi:application -k uvicorn.workers.UvicornWorker --log-file=- --log-level=info --bind 0.0.0.0:8000 --reload

exec "$@"
