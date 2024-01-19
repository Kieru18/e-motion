#!/bin/bash

# Python venv
python3 -m venv venv
venv/bin/activate

# requirements
pip install -r requirements.txt

# npm packages
npm install

# LabelStudio image
docker pull heartexlabs/label-studio:latest

# LS container
docker run --name label_studio --hostname=6c1add37c0c9 --user=1001 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=DEBIAN_FRONTEND=noninteractive --env=LS_DIR=/label-studio --env=PIP_CACHE_DIR=/.cache --env=POETRY_CACHE_DIR=/.poetry-cache --env=DJANGO_SETTINGS_MODULE=core.settings.label_studio --env=LABEL_STUDIO_BASE_DATA_DIR=/label-studio/data --env=OPT_DIR=/opt/heartex/instance-data/etc --env=SETUPTOOLS_USE_DISTUTILS=stdlib --env=HOME=/label-studio --workdir=/label-studio -p 8089:8080 --label='org.opencontainers.image.ref.name=ubuntu' --label='org.opencontainers.image.version=22.04' --runtime=runc -d heartexlabs/label-studio:latest
