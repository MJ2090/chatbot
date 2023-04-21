#!/bin/sh

sudo apt update
sudo apt install python3-pip -y
sudo apt install nginx -y
pip install --upgrade openai
pip install openai[embeddings]
pip install pandas
pip install scipy
pip install numpy
pip install tiktoken
pip install django
pip install 'gunicorn==20.1.*'

echo 'Setup Done...'
