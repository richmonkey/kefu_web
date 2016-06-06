#!/bin/sh
project="kefu.gobelieve.io"
app_dir="/data/wwwroot/${project}"
log_dir="/data/logs/${project}"
image="python_dev"

cd ${app_dir} || exit


cp -f pro_config/config.py ./config.py

mkdir -p ${log_dir}

docker restart ${project} || docker run -d --restart=always -e "PYTHONDONTWRITEBYTECODE=1" --name=${project} --net=host -v ${log_dir}:/logs -v ${log_dir}:${app_dir}/.log -v ${app_dir}/pro_config/supervisord.conf:/etc/supervisord.conf -v ${app_dir}:/app ${image} /usr/local/python/bin/supervisord

exit 0
