#!/bin/bash

echo "DB Connection --- Establishing . . ."

while ! nc -z $POSTGRES_HOST 5432; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

alembic upgrade head

# Start up the product server
uvicorn src.main:app --reload --workers 4 --host 0.0.0.0 --port 8000