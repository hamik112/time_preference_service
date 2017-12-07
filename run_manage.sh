#!/bin/bash
export ADMIN_CONFIG_PATH=config/$1.cfg
export FILE_PATH=static/uploads/
PYTHONPATH=./ python manage.py $2