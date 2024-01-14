# ML-assisted Labeling
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/e-motion/badge/?version=latest)](https://e-motion.readthedocs.io/en/latest/?badge=latest)

## Overview
The project aims to create an advanced system supporting data annotation in the field of CV. The main functionalities include: creating new projects or continuing work on existing ones, defining data categories, adding photos, annotating visual data, managing annotations, selecting model architecture, and automatic training after manually tagging photos. Additionally, the system enables applying predictions to unlabeled data, correcting model results, analyzing data and versioning models.

## Features
- Label data manually (Label Studio)
- Train ML model for auto-labeling
- Check the results your model achieves
- Predict annotations with object detector
- Correct the predicted annotations manually (Label Studio)
- Download annotations in JSON file
- Save/download trained ML model

## Tech Stack
- Python
- Django
- Django Rest Framework
- React.js
- PyTorch

## Docs
See the documentation for more detailed information:
https://e-motion.readthedocs.io/en/latest/

## Installation (recommended):
To automatically install all app dependencies:
```bash
./install.sh
```

## Usage
To run (installed) application:
```bash
./run.sh
```

## Manual installation (optional):
It is recommended to use a virtual environment. If you selected the localization and the environment:
```
pip install -r requirements.txt
```

Download the image:
```
docker pull heartexlabs/label-studio:latest
```
On first run (create a container):
```
docker run --name label_studio --hostname=6c1add37c0c9 --user=1001 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=DEBIAN_FRONTEND=noninteractive --env=LS_DIR=/label-studio --env=PIP_CACHE_DIR=/.cache --env=POETRY_CACHE_DIR=/.poetry-cache --env=DJANGO_SETTINGS_MODULE=core.settings.label_studio --env=LABEL_STUDIO_BASE_DATA_DIR=/label-studio/data --env=OPT_DIR=/opt/heartex/instance-data/etc --env=SETUPTOOLS_USE_DISTUTILS=stdlib --env=HOME=/label-studio --workdir=/label-studio -p 8089:8080 --label='org.opencontainers.image.ref.name=ubuntu' --label='org.opencontainers.image.version=22.04' --runtime=runc -d heartexlabs/label-studio:latest
```
To stop the container:
```
docker stop label_studio
```
On next runs (start existing container):
```
docker start label_studio
```

## Authors
- [@Karol Ziarek](https://github.com/ziarekk)
- [@Jan Fidor](https://github.com/JanFidor)
- [@Wojciech Lapacz](https://github.com/WojciechL02)
- [@Jakub Kieruczenko](https://github.com/Kieru18)

## License
Please check the MIT license that is listed in this repository.
