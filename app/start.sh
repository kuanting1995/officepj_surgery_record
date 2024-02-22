#!/bin/bash

echo Starting Gunicorn.
exec gunicorn app:app -c ./gunicorn_config.py --log-config ./gunicorn_logging.conf
 