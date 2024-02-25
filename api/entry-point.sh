#!/bin/sh

cp -r /var/uasset/static/*  /var/data_static
cp -r /var/uasset/default.conf  /var/data_conf/default.conf

# Create media folder to
# store uploaded images
mkdir -p ./static/vol/media/img/
# copy default image 
cp -r /var/uasset/static/vol/media/img/default.png  ./static/vol/media/img/default.png

rm -rf /var/uasset




# Run the application
# gunicorn -b 0.0.0.0:5000 app:app
python app.py