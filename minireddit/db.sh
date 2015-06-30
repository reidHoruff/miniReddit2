rm db.sqlite3 &&
rm pulled &&
touch pulled &&
python manage.py syncdb &&
python manage.py createcachetable
