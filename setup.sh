#!/bin/sh

sudo apt update
sudo apt install python3-pip -y
pip install --upgrade openai
pip install openai[embeddings]
pip install pandas
pip install scipy
pip install numpy
pip install tiktoken
pip install django

echo 'Setup Done...'