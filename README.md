# SpotCorona Backend

## 1. Installation

### 1.1. Setup Prerequisites

1. Install python3 and docker
2. Install python3 dependencies in one go from root folder : `cd ./api && pip3 install --no-cache-dir -r requirements.txt`

#### Manual Installation (In case the previous step fails on your system)

```bash
Numpy (pip install numpy)
Pandas (pip install pandas)
Django (pip install django)
Django rest framework (pip install djangorestframework)
Django pandas (pip install django_pandas)
Django rest multiple models (pip install django-rest-multiple-models)
psycopg2 (pip install psycopg2)
Shapely (pip install Shapely)
Geopandas (some of it’s pre-requirements)  (pip install geopandas)
```

There may arise some problems\errors while installing geopandas, check if versions match the ones in ./api/reqirements.txt

In this case download the latest, compatible GDAL .whl file (Ex. if your OS is windows 64 bit, and if your python version is 3.6, download GDAL-3.0.4-cp36-cp36m-win_amd64.whl) from this website:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

Run :

`pip install /path/to/GDAL-***.whl`

Repeat the above steps for Fiona:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona

Now Run:

`pip install geopandas`

### 1.2. Setup postgres database

Install in one go : `cd ./containers/postgres && ./start_postgres.sh`

Perequisites: Should have docker installed in the system, should know/set the db password

#### Manual Installation (In case docker install fails, or you want to view the database using PgAdmin GUI )

Download the package from this website:
https://www.postgresql.org/download/

Click on the download the installer and click on the latest version for your OS to download.

Run the installer. Select all the packages to be installed.

While the installer runs it asks for a password setup for the superuser: postgres

Default we are using `spotcorona`. Do not use this in a production environment

Complete the installation

Open pgAdmin from start menu.

Once it opens in the web browser, Authorize with your password.

In the browser panel on the left, right click on Databases and create a new database with the name: corona_project.

You would not see any tables yet because they havent been populated from the django project.

Export the password using `export DB_PASSWORD=your_password` for the next step.

### 1.3. Setup Django Server

Install in one go : `cd ./containers/server && ./start_server.sh`

#### Manual Installation (In case start server fails, or you want to host online)

1. If hosting, ssh into your machine, eg `ssh -i covidkey.pem ubuntu@52.66.156.232` and git clone https://github.com/GoCorona-org/Backend.git. Else skip this step.
2. In Command terminal
   1. Go to the directory $ ./api  
   2. To make the server avaliable globally add your public IP to the ALLOWED_HOSTS field in ./api/corona_project/settings.py
   3. Run: `python manage.py makemigrations corona_app`
   4. Run: `python manage.py sqlmigrate corona_app 0001_initial`
   5. Run: `python manage.py migrate`
        After this you can check the corona_project database/schemas/tables in the pgAdmin if installed. Right click and refresh. you can see the corona_app_coronaapp and corona_app_medicalmap tables
   6. Run: `python manage.py runserver`
3. Open http://127.0.0.1:8000/report in your browser

## 2. API

The reference doc for the Backend API is https://github.com/GoCorona-org/Backend/blob/master/docs/swagger.yaml ( swagger.yaml in docs folder)

Copy paste the yaml files into https://editor.swagger.io/ to view the api.

## 3.Release Notes

### Release 0.0.1

1. Refactored the folders
2. Moved gocorona_api (@wadkar's folder) to experimental, until code maturity.
3. Moved intersection and medical folders to experimental, to be deprecated in the next release.
4. Added helpful bash scripts and readmes in order to get started faster.
