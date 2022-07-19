sqlg-airflow repository for testing

[![Docker Build status](https://img.shields.io/docker/build/saastoolset/sqlg-airflow?style=plastic)](https://hub.docker.com/r/saastoolset/sqlg-airflow/tags?ordering=last_updated)


[![Docker Hub](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/saastoolset/sqlg-airflow/)
[![Docker Pulls](https://img.shields.io/docker/pulls/saastoolset/sqlg-airflow.svg)]()
[![Docker Stars](https://img.shields.io/docker/stars/saastoolset/sqlg-airflow.svg)]()

This repository contains **Dockerfile** of [apache-airflow](https://github.com/apache/incubator-airflow) for [Docker](https://www.docker.com/)'s [automated build](https://registry.hub.docker.com/u/saastoolset/sqlg-airflow/) published to the public [Docker Hub Registry](https://registry.hub.docker.com/).

- [1. The proposed environment](#1-the-proposed-environment)
- [2. Envirioment preparation](#2-envirioment-preparation)
  - [2.1. Create github repo by fork](#21-create-github-repo-by-fork)
  - [2.2. Create sqlb-test virtual environment for test](#22-create-sqlb-test-virtual-environment-for-test)
  - [2.3. Start IDE for program test](#23-start-ide-for-program-test)
- [3. sqlg-airflow install and run script](#3-sqlg-airflow-install-and-run-script)
  - [3.1 Start container](#31-start-container)
    - [3.1.1. Windows](#311-windows)
    - [3.1.2. Linux](#312-linux)
    - [3.1.3. Mac](#313-mac)
  - [3.2 Open Airflow UI](#32-open-airflow-ui)
- [4. sqlg-airflow image maintain](#4-sqlg-airflow-image-maintain)
  - [4.1. Informations](#41-informations)
  - [4.2. Installation](#42-installation)
  - [4.3. Build](#43-build)
  - [4.4. Usage](#44-usage)
  - [4.5. Configuring Airflow](#45-configuring-airflow)
  - [4.6. Custom Airflow plugins](#46-custom-airflow-plugins)
  - [4.7. Install custom python package](#47-install-custom-python-package)
  - [4.8. UI Links](#48-ui-links)
  - [4.9. Scale the number of workers](#49-scale-the-number-of-workers)
  - [4.10. Running other airflow commands](#410-running-other-airflow-commands)
- [5. Simplified SQL database configuration using PostgreSQL](#5-simplified-sql-database-configuration-using-postgresql)
- [6. Simplified Celery broker configuration using Redis](#6-simplified-celery-broker-configuration-using-redis)
- [7. Wanna help?](#7-wanna-help)


***
# 1. The proposed environment 
Follwing step will assume those tools are installed

- [Docker](https://www.docker.com/products/docker-desktop/) as container tool
- [Visual Code](https://code.visualstudio.com/download) as IDE
- [Python](https://www.anaconda.com/products/distribution) as host language with Anaconda distribution
- conda as environment manager
- pypi/pip as package repository and manager
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html) as scheduler 
- sqlg as ETL transformation tools

# 2. Envirioment preparation

## 2.1. Create github repo by fork

1. [create fork from sqlg-airflow-test](https://github.com/saastoolset/sqlg-airflow-test/fork)

2. Clone sqlg-airflow-test from github
  - Suggest directory as C:\Proj\saastoolset\sqlg-airflow-test
3. Open Anaconda command line, and switch to working directory to
  - C:\Proj\saastoolset\sqlg-airflow-test

## 2.2. Create sqlb-test virtual environment for test

- Python used to create virtual environment to keep environment clean when leverage and test different package during development. 

1. Create virtual env by conda

    $ conda env create -f sqlb_env/sqlb-test-env.yml

2. Activate sqlb-test environment
    
    $ conda activate sqlb-test


## 2.3. Start IDE for program test
1. start 
   
    $ code .

2. Verify required extension 
- python
  
# 3. sqlg-airflow install and run script

    (sqlb-test) C:\Proj\saastoolset\sqlg-airflow-test>up -h
    Batch start: 2022/07/14 週四-20:21:13.22
    .
    "up.bat: The Airflow startup script, usage:"
    "up.bat [0|1|2|3|-h]"
    "0, Start SingleNode, port=8080"
    "1, Start MultiNode, port=8081"
    "2, Start Tutorial, port=8082"
    "3, Start Example, port=8083"
    "-h, help message"

## 3.1 Start container 

### 3.1.1. Windows
- Start by option and open in browser, e.g. tutorial model
    
    C:> up 2

### 3.1.2. Linux
- Start by option and open in browser, e.g. tutorial model    
    $ up.sh 2

### 3.1.3. Mac
- Start by option and open in browser, e.g. tutorial model    
    $ sh up.sh 2

## 3.2 Open Airflow UI
- Open browser with 
  127.0.0.1:8082

# 4. sqlg-airflow image maintain

## 4.1. Informations

* Based on Python (3.9.6) official Image [python:3.9.6-bullseye](https://hub.docker.com/_/python/) and uses the official [Postgres](https://hub.docker.com/_/postgres/) as backend and [Redis](https://hub.docker.com/_/redis/) as queue
* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)

## 4.2. Installation

Pull the image from the Docker repository.

    docker pull saastoolset/sqlg-airflow-test

## 4.3. Build

Build default from Dockerfile

    docker build --rm  -t saastoolset/sqlg-airflow-test:latest .

Optionally install [Extra Airflow Packages](https://airflow.incubator.apache.org/installation.html#extra-package) and/or python dependencies at build time :

    docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" -t saastoolset/sqlg-airflow-test .
    docker build --rm --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t saastoolset/sqlg-airflow-test .

or combined

    docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t saastoolset/sqlg-airflow-test .

Don't forget to update the airflow images in the docker-compose files to saastoolset/sqlg-airflow:latest.

## 4.4. Usage

By default, sqlg-airflow runs Airflow with **SequentialExecutor** :

    docker run -d -p 8080:8080 saastoolset/sqlg-airflow-test webserver

If you want to run another executor, use the other docker-compose.yml files provided in this repository.

For **LocalExecutor** :

    docker-compose -f docker-compose-LocalExecutor.yml up -d

For **CeleryExecutor** :

    docker-compose -f docker-compose-CeleryExecutor.yml up -d

NB : If you want to have DAGs example loaded (default=False), you've to set the following environment variable :

`LOAD_EX=n`

    docker run -d -p 8080:8080 -e LOAD_EX=y saastoolset/sqlg-airflow-test

If you want to use Ad hoc query, make sure you've configured connections:
Go to Admin -> Connections and Edit "postgres_default" set this values (equivalent to values in airflow.cfg/docker-compose*.yml) :
- Host : postgres
- Schema : airflow
- Login : airflow
- Password : airflow

For encrypted connection passwords (in Local or Celery Executor), you must have the same fernet_key. By default sqlg-airflow generates the fernet_key at startup, you have to set an environment variable in the docker-compose (ie: docker-compose-LocalExecutor.yml) file to set the same key accross containers. To generate a fernet_key :

    docker run saastoolset/sqlg-airflow python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"

## 4.5. Configuring Airflow

It's possible to set any configuration value for Airflow from environment variables, which are used over values from the airflow.cfg.

The general rule is the environment variable should be named `AIRFLOW__<section>__<key>`, for example `AIRFLOW__CORE__SQL_ALCHEMY_CONN` sets the `sql_alchemy_conn` config option in the `[core]` section.

Check out the [Airflow documentation](http://airflow.readthedocs.io/en/latest/howto/set-config.html#setting-configuration-options) for more details

You can also define connections via environment variables by prefixing them with `AIRFLOW_CONN_` - for example `AIRFLOW_CONN_POSTGRES_MASTER=postgres://user:password@localhost:5432/master` for a connection called "postgres_master". The value is parsed as a URI. This will work for hooks etc, but won't show up in the "Ad-hoc Query" section unless an (empty) connection is also created in the DB

## 4.6. Custom Airflow plugins

Airflow allows for custom user-created plugins which are typically found in `${AIRFLOW_HOME}/plugins` folder. Documentation on plugins can be found [here](https://airflow.apache.org/plugins.html)

In order to incorporate plugins into your docker container
- Create the plugins folders `plugins/` with your custom plugins.
- Mount the folder as a volume by doing either of the following:
    - Include the folder as a volume in command-line `-v $(pwd)/plugins/:/usr/local/airflow/plugins`
    - Use docker-compose-LocalExecutor.yml or docker-compose-CeleryExecutor.yml which contains support for adding the plugins folder as a volume

## 4.7. Install custom python package

- Create a file "requirements.txt" with the desired python modules
- Mount this file as a volume `-v $(pwd)/requirements.txt:/requirements.txt` (or add it as a volume in docker-compose file)
- The entrypoint.sh script execute the pip install command (with --user option)

## 4.8. UI Links

- Airflow: [localhost:8080](http://localhost:8080/)
- Flower: [localhost:5555](http://localhost:5555/)


## 4.9. Scale the number of workers

Easy scaling using docker-compose:

    docker-compose -f docker-compose-CeleryExecutor.yml scale worker=5

This can be used to scale to a multi node setup using docker swarm.

## 4.10. Running other airflow commands

If you want to run other airflow sub-commands, such as `list_dags` or `clear` you can do so like this:

    docker run --rm -ti saastoolset/sqlg-airflow-test airflow list_dags

or with your docker-compose set up like this:

    docker-compose -f docker-compose-CeleryExecutor.yml run --rm webserver airflow list_dags

You can also use this to run a bash shell or any other command in the same environment that airflow would be run in:

    docker run --rm -ti saastoolset/sqlg-airflow-test bash
    docker run --rm -ti saastoolset/sqlg-airflow-test ipython

# 5. Simplified SQL database configuration using PostgreSQL

If the executor type is set to anything else than *SequentialExecutor* you'll need an SQL database.
Here is a list of PostgreSQL configuration variables and their default values. They're used to compute
the `AIRFLOW__CORE__SQL_ALCHEMY_CONN` and `AIRFLOW__CELERY__RESULT_BACKEND` variables when needed for you
if you don't provide them explicitly:

| Variable            | Default value |  Role                |
|---------------------|---------------|----------------------|
| `POSTGRES_HOST`     | `postgres`    | Database server host |
| `POSTGRES_PORT`     | `5432`        | Database server port |
| `POSTGRES_USER`     | `airflow`     | Database user        |
| `POSTGRES_PASSWORD` | `airflow`     | Database password    |
| `POSTGRES_DB`       | `airflow`     | Database name        |
| `POSTGRES_EXTRAS`   | empty         | Extras parameters    |

You can also use those variables to adapt your compose file to match an existing PostgreSQL instance managed elsewhere.

Please refer to the Airflow documentation to understand the use of extras parameters, for example in order to configure
a connection that uses TLS encryption.

Here's an important thing to consider:

> When specifying the connection as URI (in AIRFLOW_CONN_* variable) you should specify it following the standard syntax of DB connections,
> where extras are passed as parameters of the URI (note that all components of the URI should be URL-encoded).

Therefore you must provide extras parameters URL-encoded, starting with a leading `?`. For example:

    POSTGRES_EXTRAS="?sslmode=verify-full&sslrootcert=%2Fetc%2Fssl%2Fcerts%2Fca-certificates.crt"

# 6. Simplified Celery broker configuration using Redis

If the executor type is set to *CeleryExecutor* you'll need a Celery broker. Here is a list of Redis configuration variables
and their default values. They're used to compute the `AIRFLOW__CELERY__BROKER_URL` variable for you if you don't provide
it explicitly:

| Variable          | Default value | Role                           |
|-------------------|---------------|--------------------------------|
| `REDIS_PROTO`     | `redis://`    | Protocol                       |
| `REDIS_HOST`      | `redis`       | Redis server host              |
| `REDIS_PORT`      | `6379`        | Redis server port              |
| `REDIS_PASSWORD`  | empty         | If Redis is password protected |
| `REDIS_DBNUM`     | `1`           | Database number                |

You can also use those variables to adapt your compose file to match an existing Redis instance managed elsewhere.

# 7. Wanna help?

Fork, improve and PR.
