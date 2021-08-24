# guane-intern-fastapi

![N|Solid](./images/Architecture.png)


## _Adopt a doggy_

## Tech

For this app, was used a number of Technologies:

* [Python 3.8] 
* [pipenv] - ```$ pip install pipenv```
* [PostgreSQL]
* [Docker]
* [Docker Compose]
* [RAbbitMQ]
* [Redis]

## Develop
With the intention of bringing the situation closer to reality, this app was developed like a plataform used to adopt dogs, therefore, in addition to the basic characteristics of the test, some more were added:

#### Dog Model:
- column in_charge: is used to define who is in charge of the dog, if the Dog is new, the person who create the register becomes the responsible.

#### User CRUD:
- Endpoint _deactivate_: is used to avoid delete the complete register of a user.

#### Dog CRUD:
- Endpoint adopt/{name}: is used to asign the owner and the new responsible for the dog.

**Note:** In the same way, the app has all the endpoints required for both entities: User and Dog

## Usage
First, clone the repository to get all the files
```sh
$ git clone https://github.com/danieltorresg/guane-intern-fastapi.git
```

Install [Docker] and [Docker Compose]

Then, in the main directory, configure the .env file, this file contains the environment variables that are used in the app.

Run the images
```sh
$ docker-compose up --build
```

The docker compose file creates an image to run the the main app (doggys-app), and another image with de database service (doggys-db). The app can be seen visited at `0.0.0.0:8000/docs`, once in the link, is possible to send the request

Some endpoints (Post, Put and Delete) was protected with JWT, to access to them, is necessary to authenticate. In the top right, there is a button to Log in, in the app there is a default user to test the endpoints:
```sh
email: init@mail.com
password: SecurePassword
```
The rest of the fields are left empty.

## Entity Relationship Diagram

![N|Solid](./images/ERDiagram.png)

## Environment Variables

The .env file contains all the environment variables used in the app, below there is an example how should be defined

```sh
WEB_APP_TITLE=guane Intern Fastapi
WEB_APP_DESCRIPTION=This is a app about adopt dogs - Technical test
WEB_APP_VERSION=1.0
SECRET_KEY=cfd11da5af04ab43747b19afdddfb5a82914a793f21c5209b4c9e2ae3fcad009
ALGORITHM=HS256
DATABASE_URL=postgres://postgres:postgres@doggys_db:5432/doggys #if change, change too in data/create.sql
IMAGE_API=https://dog.ceo/api/breeds/image/random
INITIAL_EMAIL="init@mail.com" #email to default initial user
INITIAL_PASSWORD="SecurePassword" #password to default initial user
```

   
   [Docker]: <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-es>
   [Docker Compose]: <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-es>
   [Python 3.8]:<https://www.python.org/>
   [pipenv]:<https://pypi.org/project/pipenv/>
   [PostgreSQL]:<https://www.postgresql.org/>
   [RAbbitMQ]:<https://www.rabbitmq.com/>
   [Redis]:<https://redis.io/>
