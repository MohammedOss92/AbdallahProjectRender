#!/bin/bash

# إعطاء إذن التنفيذ للملف نفسه (اختياري)
chmod +x build.sh

# تحديث pip
pip install --upgrade pip

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الترحيلات
python manage.py migrate

# تجميع الملفات الساكنة
python manage.py collectstatic --noinput
