#!/usr/bin/env bash
# Script de build usado no Render (Build Command: bash build.sh).
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
