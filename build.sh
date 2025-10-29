#! /usr/bin/env bash

set -o errexit

# Build phase: install dependencies and collect static files.
pip install -r requirements.txt
python manage.py collectstatic --noinput

# NOTE:
# - Migrations, superuser creation, and data seeding must NOT run in build.
#   They belong to the Pre-Deploy Command. See predeploy.sh in the repo root.