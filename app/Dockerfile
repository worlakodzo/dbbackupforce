# Reference:
# https://yashmehrotra.com/posts/building-minimal-docker-images-using-multi-stage-builds/
# https://gabnotes.org/lighten-your-python-image-docker-multi-stage-builds/

FROM python:3.8-alpine as build
RUN apk update && apk add build-base

RUN mkdir -p /var/assetmgmt/static
WORKDIR /code

COPY requirements.txt /code

RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY static /var/assetmgmt/static
COPY entry-point.sh default.conf /var/assetmgmt/
COPY . /code/

# Remove static files 
# from code folder
RUN rm -rf static


# Production enviroment
FROM python:3.8-alpine

RUN mkdir -p /var/assetmgmt/static
WORKDIR /code

COPY --from=build /code/ /code
COPY --from=build /usr/local/lib/python3.8 /usr/local/lib/python3.8
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=build /var/assetmgmt/entry-point.sh  /usr/local/bin/entry-point.sh
COPY --from=build /var/assetmgmt/default.conf  /var/assetmgmt/default.conf
COPY --from=build /var/assetmgmt/static/  /var/assetmgmt/static

EXPOSE 5000
RUN chmod 755  /usr/local/bin/entry-point.sh


HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)"


# Run the application
ENTRYPOINT [ "entry-point.sh" ]