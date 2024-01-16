Admin manual
============

[- instrukcja budowy systemu z kodu źródłowego
- instrukcja instalacji i konfiguracji systemu
- instrukcja aktualizacji oprogramowania
- instrukcja zarządzania użytkownikami i uprawnieniami
- instrukcja tworzenia kopii zapasowych i odtwarzania systemu
- instrukcja zarządzania zasobami systemu]

Installation
------------
To install all the packages needed to run the application, run the ``install.sh`` script
(creates venv, install Python packages, npm dependencies and LS docker image).

It is recommended to use provided scripts, but if you want to install dependencies manually,
you can follow commands from ``install.sh`` script and change them.

``install.sh`` details:

1. Python Virtual Environment:
    Create:
    ``python3 -m venv venv``

    Activate:
    ``venv/bin/activate``

2. Python requirements
    ``pip install -r requirements.txt``

3. NPM dependencies
    ``npm install``

4. LabelStudio Docker image
    ``docker pull heartexlabs/label-studio:latest``

5. LabelStudio Docker container
    ``docker run --name label_studio --hostname=6c1add37c0c9 --user=1001 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=DEBIAN_FRONTEND=noninteractive --env=LS_DIR=/label-studio --env=PIP_CACHE_DIR=/.cache --env=POETRY_CACHE_DIR=/.poetry-cache --env=DJANGO_SETTINGS_MODULE=core.settings.label_studio --env=LABEL_STUDIO_BASE_DATA_DIR=/label-studio/data --env=OPT_DIR=/opt/heartex/instance-data/etc --env=SETUPTOOLS_USE_DISTUTILS=stdlib --env=HOME=/label-studio --workdir=/label-studio -p 8089:8080 --label='org.opencontainers.image.ref.name=ubuntu' --label='org.opencontainers.image.version=22.04' --runtime=runc -d heartexlabs/label-studio:latest``

Usage
-----
To run installed application, use the ``run.sh`` script.

``run.sh`` details:

1. Start LabelStudio Docker container
    ``docker start label_studio``

2. Go to application directory
    ``cd ./e_motion``

3. Run Django server
    ``python3 ./manage.py runserver``
