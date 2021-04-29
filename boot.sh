#!/bin/bash
# this script is used as the entrypoint of a Docker container
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app
