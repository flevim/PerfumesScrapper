#!/bin/sh
if [ ! -f "/app/requirements_installed" ]; then
    pip install -r /app/requierements.txt
    touch /app/requirements_installed
fi
python /app/main.py