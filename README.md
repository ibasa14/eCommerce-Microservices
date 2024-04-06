# eCommerce-Microservices IBC

This project serves as a way to use and practice with some of the most popular tech stack for backend development using Python.

The project emulates a real-world application of an e-commerce following the micro-services pattern.


## Table of Contents
- [Stack](#stack)
- [Architecture and Decisions](#architecture)
- [Installation](#installation)
- [Future Work](#future-work)
- [Usage](#usage)
- [Deployment](#deployment)
- [License](#license)

## Stack
The project uses the following tech-stack:
This template utilizes the following tech-stack:

**Main**
* 🐳 [Dockerized](https://www.docker.com/)
* 🐘 [Asynchronous PostgreSQL](https://www.postgresql.org/docs/current/libpq-async.html)
* 🐍 [FastAPI](https://fastapi.tiangolo.com/)
* 🥦 [Celery](https://docs.celeryq.dev/en/stable/)
* ☸ [Kubernetes](https://kubernetes.io/es/docs/concepts/overview/what-is-kubernetes/)

**Complementary**
* [TOML](https://toml.io/en/) $\rightarrow$ The one-for-all configuration file. This makes it simpler to setup our project.
* [Pre-Commit](https://pre-commit.com/) $\rightarrow$ Git hook scripts to identify issues and quality of your code before pushing it to GitHub. These hooks are implemented for the following linting pakcages:
  * [Black (Python)](https://black.readthedocs.io/en/stable/) $\rightarrow$ Manage your code style with auto formatting and parallel continuous integration runner for Python.
  * [Ruff](https://docs.astral.sh/ruff/)$\rightarrow$ An extremely fast Python linter and code formatter, written in Rust.
* [PyTest](https://docs.pytest.org/en/7.2.x/) $\rightarrow$ The testing framework for Python code.
* [GitHub Actions](https://github.com/features/actions) $\rightarrow$ The platform to setup our CI/CD by GitHub.
* [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) $\rightarrow$ The go-to database interface library for Python. The 2.0 is the most recent update where it provides asynchronous setup.
* [JWT](https://jwt.io/introduction) $\rightarrow$ Is an open standard which defines a compact and self-contained way for securely transmitting information between parties as a JSON object


### Why this tech stack?
Well, the easy answer is **Asynchronousity** and **Speed**!

* **FastAPI** is crowned as the fastest web framework for Python and thus we use it for our backend development.
* The database of my choice is the **asynchronous** version of **PostgreSQL** (via [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)). Read [this blog from Packt](https://subscription.packtpub.com/book/programming/9781838821135/6/ch06lvl1sec32/synchronous-asynchronous-and-threaded-execution) if you want to educate yourself further about the topic **Asynchronous, Synchronous, Concurrency,** and **Parallelism**.
* **Docker** is a technology that packages an application into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime.

## Architecture
The project has been implemented using microservices. This way, it simulates more nearly what a real-world application looks like and the challenges it presents.

However, everything is contained in the same project, in order to avoid innecesary overhead: *monorepo*

There are currently 3 different services:
* **Account**: Currently it handles the login and manages the users database. For the login, it creates JWT with the corresponding scopes, attending to the role of the user.
* **Product**: Manages the inventory of the products offered in the application.
* **Order**: Manages the orders. Once the user makes an order, the inventory is updated accordingly (internal API call to the Product service is made), then a simulated email is sent to the user. This task is handled thuough the task manager: **Celery**

## Future Work
There are still plenty of things that can improve the current version of the software. Here are some ideas that could be implemented in the future:
- Add the Shopping Cart Service making use of Flask/FastApi for the API along with redis as the DB
- Implement the Front-end of the application. Possible technologies: ReactJS / Dash (Python).
- Add a blob storage service for the products images.
- Consume order events to populate an OLAP db (such as Clickhouse). This would require a first save into postqresQL and the implementation of an ETL. This OLAP could be used as a new dashboard service for data analytics.


## Installation
It requires:
* Python 3.10
* Docker

1.- Pull the project
```
git fetch https://github.com/ibasa14/FastAPI-template-IBC.git
```
2.- Create the virtual environment:
```
python3.10 -m venv env && source env/bin/activate
```
3.- Install dependencies (with the environment activated):
```
pip install -r order/requirements.txt
```
_*Any of the 3 requirements.txt can be used_


## Usage
In order to start the application in the dev environment:
```
docker-compose -f docker-compose.dev.yaml -up -d
```

## Deployment
In order to deploy the application, it can be used **kubernetes** technology. In the root folder of the project you can find an example manifest containing all the required services, deployments and PVCs.

This file has been created using **kompose**, which converts a docker-compose.yml to a kubernetes manifest:
```
kompose convert -f docker-compose.yaml -o k8s_deployment.yml
```


## License
MIT License.
Please refer to the LICENSE file.
