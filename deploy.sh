cd /var/www/iktzap/api && git pull && source venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && deactivate && sudo systemctl restart iktzap_api
