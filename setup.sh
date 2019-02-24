#!/bin/bash

echo "Database setup on ubuntu system"

sudo apt-get update
sudo apt-get install mysql-server

sudo mysql <<EOF
CREATE USER street_parking@localhost IDENTIFIED BY 'street_parking';
GRANT ALL PRIVILEGES ON street_parking.* TO street_parking@localhost;
FLUSH PRIVILEGES;
CREATE DATABASE street_parking;
EOF
