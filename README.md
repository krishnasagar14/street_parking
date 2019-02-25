# Street Parking Spot Reservation

This repository is for street spot parking reservation service to enable vehicle owners (portal users) reserve street parking spot.
It serves for a portal/ client/ app via REST API which includes:

1. User services - 
   portal registration and portal login, 
   portal login is delivered with JWT token for other authorized protected services
2. Authentication services - 
   Json Web Token(JWT) bearer authorization, 6hours expiry of token
3. Parking spot services - 
   view and search available spots (Authorization protected), 
4. Reservation services (Authorization protected) - 
   reserve spot and cancel spot, 
   view cost of reservation


## Architecture and Design of project

1. REST pattern is utilized via django rest framework.
2. Above services are modular, tied up into project via Django settings to form string of services.
3. Database design:
Please follow: 


## Technology used

1. Python3.6
2. Django2.1.7
3. DjangoRestFramework3.9.1
4. MySql5.8


## Platform Needed

This project is cross-platform to windows and linux, but tested on:
1. Windows 10
2. Ubuntu 16.04 LTS

## Installations Needed:

This project needs basic pythonic installations on your OS platforms:

1. python3.6.8
2. pip3
3. python3.6-dev

## Project Setup

1. Execute setup.sh script file to setup MySql database.
2. Execute start.sh script file to start API service via django.
3. You can execute and check unit tests via executing tests.sh script file.

## Unit tests coverage:

coverage.py tool is used to generate coverage report. Check steps of using tool in tests.sh script file.
Current tests coverage is 86%

## Future

Development in deployment scenarios via Docker, Ansible - for deployment configs
