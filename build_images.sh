#!/bin/bash

sudo docker build . -t python-image
sudo docker build . -f Dockerfile-db -t mysql-db

sudo docker-compose up -d rabbit

while [[ "$(curl -u guest:guest -s -o /dev/null -w ''%{http_code}'' http://127.0.0.1:15672/api/queues/%2F/)" != "200" ]]; do
    echo 'Waiting for rabbit connection...'
    sleep 5
done
echo "RabbitMq started!"
sudo docker-compose up -d db
echo 'Waiting for MySQL Database to start...'
while ! sudo docker exec bagendproject_db_1 mysqladmin --user=root --password=root --host "127.0.0.1" ping --silent &> /dev/null ; do
    echo "Waiting for database connection..."
    sleep 5
done
echo "mySQL Database started!"

#sudo docker-compose up -d server
sudo docker-compose up -d publisher
#sudo docker-compose up -d persistor

