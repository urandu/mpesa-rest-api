#!/bin/sh

# Starting Gunicorn processes
echo Starting Gunicorn.
exec gunicorn mpesa.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3