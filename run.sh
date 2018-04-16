#!/bin/bash

basedir=$(cd `dirname $0`; pwd)
set -x

sudo systemctl start httpd

python3 run.py

sudo systemctl stop httpd
