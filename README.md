# WormsSockets 

A simple backend using sockets to play Worms with friends.
We use docker and docker-compose to run the server, so you need to have docker installed in your machine.
Using docker, we have 3 containers: web, mongodb and redis.

- [WormsSockets](#wormssockets)
  - [Containers](#containers)
  - [Installation](#installation)
  - [Usage](#usage)


## Containers

We have 3 containers:
- **web**: The web server, which is a simple python server using sockets.
- **mongodb**: The database, which is a mongo database.
- **redis**: The cache, which is a redis database.

## Installation

To run the server, you need to have docker and docker-compose installed in your machine.
Then, you just need to run the following command:

```bash
make build
```

## Usage

To run the server, you just need to run the following command:

```bash
make up
```

To stop the server, you just need to run the following command:

```bash
make down
```
or 
```bash
ctrl + c
```     

