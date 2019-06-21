#!/bin/sh

echo "Waiting for DBs..."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
done

echo "DB started"

#python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --noinput

if [ $create_superuser = 'true' ]; then

python manage.py shell -c "import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('BDAPI_SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('BDAPI_SUPERUSER_NAME'), os.environ.get('BDAPI_SUPERUSER_MAIL'), os.environ.get('BDAPI_SUPERUSER_PASS'))
else:
    pass"
fi

exec python manage.py runserver $BDAPI_HOST:$BDAPI_PORT