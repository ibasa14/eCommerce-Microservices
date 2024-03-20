#!/bin/bash

echo "DB Connection --- Establishing . . ."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

alembic upgrade head

# Start up the authentication server
uvicorn src.main:app --reload --workers $SERVER_WORKERS --host 0.0.0.0 --port $SERVER_PORT
