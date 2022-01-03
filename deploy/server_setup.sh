#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_US.UTF-8

# Install Python, SQLite and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/python_django

mkdir -p $VIRTUALENV_BASE_PATH
python3 -m venv $VIRTUALENV_BASE_PATH/python_django

$VIRTUALENV_BASE_PATH/python_django/bin/pip install -r $PROJECT_BASE_PATH/python_django/requirements.txt

# Run migrations
cd $PROJECT_BASE_PATH/python_django

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/python_django/deploy/supervisor.conf /etc/supervisor/conf.d/python_django.conf
supervisorctl reread
supervisorctl update
supervisorctl restart python_django

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/python_django/deploy/nginx.conf /etc/nginx/sites-available/python_django.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/python_django.conf /etc/nginx/sites-enabled/python_django.conf
systemctl restart nginx.service

echo "DONE!"