#!bin/bash

basepath=`dirname $0`
cd $basepath

echo "starting to run class file"

python manage.py runserver 8000
