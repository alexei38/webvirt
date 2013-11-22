webvirt
=======

libvirt connection


apt-get update
apt-get install python-pip python-libvirt python-dev python-ldap
pip install -r requirements.txt
./manage.py syncdb
./manage.py runserver 0.0.0.0:80