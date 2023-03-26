#!/bin/bash
sudo systemctl start nginx
cd /home/anurag/URL_Shortener/
source venv/bin/activate
gunicorn "urlshort:create_app()" -b 0.0.0.0
