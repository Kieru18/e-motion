#!/bin/bash

docker start label_studio

cd ./e_motion

python3 ./manage.py runserver
