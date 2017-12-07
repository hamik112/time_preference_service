#!/bin/bash
source $2bin/activate
export ADMIN_CONFIG_PATH=config/$1.cfg
export FLASK_APP=main.py
flask rq worker

