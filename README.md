## Introduction 
Self hosted ISMS microservice using pyhton. This services are convenient when you have one main ISMS account and one or more ISMS sub-account derived from main account. 

Sub-account can be created from main account dashboard and main account can assign how much sms credit applicable for each sub-account which is more easy to manage when we have multiple sub-module inside our application that need to use different credential for different module.


## Requirement

1. pyhton v2.7 and above 
2. Flask v0.12.2
3. flask_restful v0.2.12
4. request v2.18.4

## Installation

Clone this repository

```
git clone git@github.com:metallurgical/isms-microservice-pyhton.git isms-microservices
```

Run

```
pip install -i requiments.txt
```

Create folder name `instance` inside folder root directory and create python module file with name `config.py`, paste below code into it. This configuration just for testing purpose as you're able to send username and password together during post request.

```python
ISMS_USERNAME = 'isms username'
ISMS_PASSWORD = 'isms password'
```


## Start Server
Navigate to isms-microservices folder and run

```
python app.py
```

## Usage
You can make HTTP request call from any client client as long as they can accept content type `application/x-www-form-urlencoded` or `application/json`.

Send Message: `POST http(s)://<domain-name>/sms/send`
- **username** : [string] Isms username
- **password** : [string] Isms password
- **phone** : [string|array] Receiver's phone number.Either single string or list of array. e.g: **60134567874** or **['60134567874', '60134567874']**
- **message** : [string] Message to send to the receiver.


Check Balance: `POST http(s)://<domain-name>/sms/check-balance`
- **username** : [string] Isms username
- **password** : [string] Isms password


`<domain-name>` could be TLDN(top level domain name) or `localhost`, depends on where your application is hosted and deploy.


## Test
Run test 

```
pyhton app-test.py
```

## Hosted using apache mod-wsgi(Web Server Gateway Interface)

To host flask application on Apache, we need `mod_wsgi` enabled in order to handle incoming request and handle python code as python is not a native language.

### Requirement
 - mod_wsgi
 - pyhton virtualenv
 - wsgi script
 
 
`mod_wsgi` is not coming together with apache installation, we have two installation options either using `pip` or tradisional installation. Both of these methods is essential depends on your server environment.

Must be noted, `mod_wsgi` and `virtualenv` must be using the same python version for compilation and installation. As example, you cant use `mod_wsgi` with `virtualenv` that compiled using python 2.7 on `virtualenv` that compiled using python 3. If this situation happens, you need to install `mod_wsgi` manually and load the module inside apache configuration.

Using `pip`, the following command can be used:

```
pip install mod_wsgi
```

Above command will install `mod_wsgi` directly from official repository. If for some reason, your `virtualenv` didnt compiled with the same version as `mod_wsgi`, you need to compile it yourself. 

To compile our self, first we need to download the library(change version number):

```
wget https://pypi.python.org/packages/15/d4/83c842c725cb2409e48e2999e80358bc1dee644dabd1f3950a8dd9c5a657/mod_wsgi-4.5.24.tar.gz
```

After download, extract the installation file:

```
tar -xzvf mod_wsgi-4.5.24.tar.gz
```

This will extract the file into `mod_wsgi-4.5.24` folder. Before we can install, you must configure it first:

```
./configure
```

The configure script will attempt to identify the Apache installation to use by searching in various standard locations for the Apache build tools. 

Once the package has been configured, it can be built by running: 

```
make
```

If successful, the only product of the build process that needs to be installed is the Apache module itself. There are no separate Python code files as everything is done within C code compiled into the Apache module.

To install the Apache module into the standard location for Apache modules as dictated by Apache for your installation, run:

```
make install
```

Installation should be done as the ‘root’ user or ‘sudo’ command if appropriate.

The library usually will be installed inside `/usr/lib/apache2/modules`. After installation's done, load the module inside `apache2.conf` or `httpd.conf` depends on `apache2` version you had installed on the server by using this code:

```
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
```

Restart apache:

```
apachectl reload  or service apache2 reload
```

Afterward, install `virtualenv` somewhere in your server. Instead of running our apps using python built-in system, it is recommended to use virtual environment to avoid our system conflict with external library that our application used.

This virtual environment can be install globally or install specific per project. For ease of use, just install per project basis. Enter into your application root project along with others file, run this command to install:

```
python -m virtualenv venv # python 2.7
python3 -m virtualenv venv # python 3
```

Once created, we can activate the environment for checking purpose:

```
source venv/bin/activate
```

To exit/close environment, run:

```
deactivate
```

In order to make our application run under this environment, we need to setup our `Virtualhost` to look for this environment by adding `python-home` and `python-path`. Example `virtualhost` config:

```
<VirtualHost *:80>
        ServerName example.com
        ServerAdmin admin@example.com

        WSGIDaemonProcess myapp user=www-data group=www-data threads=5 python-home=/var/www/example.com/flaskapp/venv python-path=/var/www/example.com/flaskapp
        WSGIProcessGroup myapp
        WSGIScriptAlias / /var/www/example.com/flaskapp/myapp.wsgi
        <Directory /var/www/example.com/flaskapp>
            WSGIApplicationGroup %{GLOBAL}
            Require all granted # apache 2.4 >
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Noted that, this `/var/www/example.com/flaskapp/myapp.wsgi` must be exist somewhere. This file will handle incoming request from apache and send response from our Flask app to the client. Example file:

```
import sys

sys.path.insert(0,'/var/www/example.com/flaskapp')

# activate this if we didnt use python-home and python-path
# activate_this = '/var/www/example.com/flaskapp/venv/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))


from app import app as application
# enable this to create secret key for our application
# application.secret_key = 'hellotherehowareyoudoingisitok'
```

Reload apache. Done!







