# Blog Posts Assessment


## Pre-requisites

* Python 3.9
* Docker (optional)
* Docker compose (optional)

To install all of the python libraries that were used in this project, run:

```bash
pip install -r requirements.txt
```

### Config redis

The settings in the redis are in the file: `.env`

```bash
CACHE_TYPE=redis
CACHE_REDIS_HOST=localhost
CACHE_REDIS_PORT=6379
CACHE_REDIS_DB=0
CACHE_REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=500
```

## To run

To run application:

```bash
python run.py
```

Server running by default in address: `http://127.0.0.1:5000/`

In the `.env` file you can set variable `DEBUG`, to run application in debug mode or not, by default debug mode is `True`

### To run using docker

If you have docker and docker-compose installed, can you run application with this command:
```bash
docker-compose up --build
```

OBS: If you have redis installed in your local machine, it's necessary stop the service, you can this with following command: `systemctl stop redis.service`

## To run tests

To run automated tests to application:

```bash
python test.py
```


## Authors
[**Jose Henrique Roquette**](https://github.com/jroquette)
