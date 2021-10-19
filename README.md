### simple application for scheduling dental appointments for patients with django ###

> simple application for scheduling dental appointments for patients.

- Collaborator registration
- patient registration
- Scheduling appointments
- Insertion of types of service and their prices
- Service activation and deactivation
- Sending email to the patient with scheduled appointments 

## Technologies used requirements.txt

- Python==3.6
- django==2.2.10
- pytz==2019.3
- gunicorn==19.9.0
- mysqlclient==1.4.1
- pyasn1==0.4.5
- sqlparse==0.3.0
- Pillow==6.1.0
- django-filebrowser-no-grappelli==3.7.8
- ics==0.5

## CI/CD

``` 
.gitlab-ci.yml 

Dockerfile 
```
    

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pip.

```
pip install -r requiriments.txt
```
Now just generate the django tables with the following command ```makemigrations``` and ```migrate```

```
$ python manage.py makemigrations
```
```
$ python manage.py migrate
```
Create a new user

```
$ python manage.py createsuperuser
```
Run the project

```
$ python manage.py runserver
```

