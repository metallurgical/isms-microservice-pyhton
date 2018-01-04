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
You can made HTTP request call from any client client as long as they can accept content type `application/x-www-form-urlencoded` or `application/json`.


## Test
Run test 

```
pyhton app-test.py
```



