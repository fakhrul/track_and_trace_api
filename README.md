# Track and Trace API

1. Running the environment (if already have)
````
conda activate tat
````
2. Install dependecy
````
npm install
````
3. Run the service
````
python run.py
````

# Fresh deployment via SSH
## Setup conda
1. Download the Anaconda bash script
```
mkdir tmp
cd /tmp
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output conda-installer.sh
```
2. Verify installer
```
sha256sum conda-installer.sh
```
3. Run the installer script and complete installation
```
bash conda-installer.sh
```
4. create conda environment
```
conda create
```
## Setup application
1. git clone

2. install requirements
```
pip install -r requirements.txt
```
3. run the application

## Setup ngix
1. Install NGIX
```
sudo apt install nginx
```
2. create new configuration file
```
sudo nano /etc/nginx/sites-enabled/flask_app
```
3. configure configuration file
```
server {
    listen 80;
    server_name 192.0.2.0;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
4. disable default link
```
sudo unlink /etc/nginx/sites-enabled/default
```
5. reload 
```
Reload the NGINX configuration file:
```
Reference
[Reference 1](https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/)

# Development
## Flask Installation
  - Install [Python](https://www.python.org/downloads/), [Pipenv](https://docs.pipenv.org/) and [Postgres](https://www.postgresql.org/) on your machine
  - Clone the repository `$ git clone git@github.com:jerichoruz/backbloggie.git`
  - Change into the directory `$ cd /backbloggie`
  - Create the project virtual environment with `$ pipenv --three` command
  - Activate the project virtual environment with `$ pipenv shell` command
  - Install all required dependencies with `$ pipenv install`
  - Rename .env.sample to .env and edit variables
      ```
      FLASK_ENV=development
      FLASK_PORT=5005
      DATABASE_URL=postgres://user:pass@localhost:5432/bd
      JWT_SECRET_KEY=pass_salt_phrase
      PAYPAL_ID=
      PAYPAL_SECRET=
      MAIL_SERVER=mail.server.com
      MAIL_PORT=465
      MAIL_USERNAME=user
      MAIL_PASSWORD=pass
      ```
    - To know where to get your paypal id & secret got to https://conectika.tech/blog/conectika-tech-1/post/como-obtener-el-id-de-cliente-y-la-clave-secreta-de-paypal-15

  - Create database blog
      ```
      $ sudo su - postgres -c "createuser -s bloguser" 2> /dev/null || true
      $ psql
      # ALTER USER bloguser WITH ENCRYPTED PASSWORD 'bloguser';
      # CREATE DATABASE blog WITH TEMPLATE template0;
      # ALTER DATABASE blog OWNER TO bloguser;
      ```
  - Due to a bad flask relation please Comment line 5 from UserModel before Migrate
      ```
      1 # src/models/UserModel.py
      2 from marshmallow import fields, Schema
      3 import datetime
      4 from . import db
      5 #from ..app import bcrypt #after  python manage.py db upgrade uncomment to execute python run.py
      ```
  - `$ python manage.py db init`
  - `$ python manage.py db migrate`
  - `$ python manage.py db upgrade`
  - it should look like this
      ```
      1 # src/models/UserModel.py
      2 from marshmallow import fields, Schema
      3 import datetime
      4 from . import db
      5 from ..app import bcrypt #after  python manage.py db upgrade uncomment to execute python run.py
      ```
  
  - Start the app with `python run.py`
  - File BACKBLOGGIE.postman_collection.json its a Postman collection just import for test your backend
  - standalone_html_paypal_test_button.html its a html file to test the paypal button with the backend and update items_paid column in user using the button
   
## Where should I host My web app?
The ideal VPS for open community web apps in México https://conectika.tech/standar-vps

## web3py Installation
