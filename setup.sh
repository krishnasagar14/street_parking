#!/bin/bash

echo "Database setup on ubuntu system"

apt-get update
apt-get install -y mysql-server

mysql <<EOF
CREATE USER street_parking@localhost IDENTIFIED BY 'street_parking';
GRANT ALL PRIVILEGES ON street_parking.* TO street_parking@localhost;
FLUSH PRIVILEGES;
CREATE DATABASE street_parking;
EOF

pip install -R requirements.txt