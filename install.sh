#!/bin/bash

echo "正在安装pip工具..."
apt-get install pip
echo "正在安装httplib2..."
pip install httplib2
echo "httplib2安装完毕"

echo "正在安装Django..."
pip install Django
echo "Django安装完毕"

exit 0