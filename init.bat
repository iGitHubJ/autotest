@echo off
@rem "开始同步数据库"
python manage.py makemigrations
python manage.py migrate