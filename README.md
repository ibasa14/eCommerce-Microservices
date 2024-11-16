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
* **Order**: Manages the orders. Once the user makes an order, the inventory is updated accordingly (internal API call to the Product service is made), then a simulated email is sent to the user. This task is handled through the task manager: **Celery**

## Future Work
There are still plenty of things that can improve the current version of the software. Here are some ideas that could be implemented in the future:
- Add the Shopping Cart Service making use of Flask/FastApi for the API along with redis as the DB.
- Implement the Front-end of the application. Possible technologies: ReactJS / Dash (Python).
- Add a blob storage service for the products images.
- Load logs to Clickhouse (OLAP database). Consume this data to extract insights to be shown in a dashboard (developed in plotly-dash) along with ML predictions. This will be implemented this way:
  - Apache kafka will save logs (3 types: see product, search product, buy product) to the corresponding postgres table. Kafka will also handle the enrichment of the logs (will add a generic datetime format).
  - An ETL will be used to load data from postgres to clickhouse. This will be done periodically using Airlfow, once loaded, the model will be retrained with the data.
  - Dash will extract data from Clickhouse to render some graphs in the dashboard.


## Installation
It requires:
* Python 3.10
* Docker
* pre-commit

1.- Pull the project
```
git fetch https://github.com/ibasa14/eCommerce-Microservices
```
2.- Install docker and docker compose if not installed:
```
sudo apt install docker
sudo apt install docker-compose
```
3.- In case you want to run it locally using kubernetes:
```
sudo apt install kubectl
```

## Run the system
In order to start the application in the dev environment:
```
docker-compose -f docker-compose.dev.yaml -up -d
```
After the system is running, you can connect for example into the Account documentation, by browsing the following URL (In case no changes are made here): localhost:8003/docs

To stop the execution, you can just type:
```
docker-compose down
```

You might have noticed there are two different docker compose manifests. One is for dev, the other is por "production".
It is probably not a good option to deploy in production a system using docker-compose. As it is not able to scale and lacks many features. But it is often used for developing porpuses. At the end, you can always convert the docker-compose to a kubernetes manifest.
The difference with the dev and the prod docker compose manifest is the usage of volumes, as well as other adaptions made to the prod one in order to enable the conversion to a kubernetes manifest.

## Development
In this repo it is used the pre-commit hooks tool. If you don't have it installed. Run the following command:
```
pre-commit install
```
Other tool which is very useful in order to be able to quickly connect to the different containers to see logs, etc is the *Docker Desktop*. Other option is install the extension for Vscode, which works good also.

## Deployment
In order to deploy the application, it can be used **kubernetes** technology. In the root folder of the project you can find an example manifest containing all the required services, deployments and PVCs.

This file has been created using **kompose**, which converts a docker-compose.yml to a kubernetes manifest:
```
kompose convert -f docker-compose.yaml -o k8s_deployment.yml
```
Before deploying it in the cloud, if any change has been made and you want to check locally whether it works, you can deploy locally doing the following:

You can use *minikube* to run kubernetes locally. You will need to install it in case you haven't yet.
After, you will need to initialize minikube:
```
minikube start
```
Later, to check if minikube is up and running:
```
minikube status
```
In case everything looks correct, then you can deploy the manifest:
```
kubectl apply -f k8s_deployment.example.yml
```

In case kubernetes is not install, you need to run:
```
sudo apt install kubectl
```


## License
MIT License.
Please refer to the LICENSE file.
