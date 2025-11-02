#!/bin/sh
FIXTURE_FILE="fixtures.json"

python manage.py migrate
python manage.py collectstatic --noinput
[ -f "$FIXTURE_FILE" ] && python manage.py loaddata fixtures.json
python manage.py runserver 0.0.0.0:${PORT:-8000}
