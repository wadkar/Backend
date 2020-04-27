#!/bin/bash

# Read Password
echo -n Database Password: 
read -s DB_PASSWORD
echo

docker rm -f postgres
docker run --network=host --name postgres -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=corona_project  -d postgres