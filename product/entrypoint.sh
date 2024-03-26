#!/bin/bash

echo "DB Connection --- Establishing . . ."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

alembic downgrade base
alembic upgrade head

python src/data/populate_db.py

# Start up the product server
uvicorn src.main:app --reload --workers $SERVER_WORKERS --host 0.0.0.0 --port $SERVER_PORT
# tail -f /dev/null