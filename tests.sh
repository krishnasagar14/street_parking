#!/bin/bash

cd server/;


# clean coverage data, reports
rm -rf htmlcov
coverage erase

coverage run --source='.' --omit='*/migrations/*' manage.py test
coverage report
coverage html
