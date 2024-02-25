FROM python:3.8 as build
# RUN apt update && apt install build-base cmake

WORKDIR /code


COPY requirements.txt /code
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /code/

# Remove static files 
# from code folder
RUN rm -rf static


# Production enviroment 
FROM python:3.8
RUN mkdir -p /var/backupforceplus/conf/
RUN mkdir -p /var/backupforceplus/backup/


WORKDIR /code


COPY --from=build /code/ /code
COPY --from=build /usr/local/lib/python3.8 /usr/local/lib/python3.8
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn


EXPOSE 5000


HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)"


# Run the application
ENTRYPOINT [ "python", "app.py" ]
# ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:5000", "app:app" ]