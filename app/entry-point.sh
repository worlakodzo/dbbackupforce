#!/bin/sh

cp -r /var/assetmgmt/static/*  /var/data_static
cp -r /var/assetmgmt/default.conf  /var/data_conf/default.conf


# Run the application
gunicorn -b 0.0.0.0:5000 app:app