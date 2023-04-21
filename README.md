# Code Structure:

- setup.sh: run this sh to install necessary libs
- src: contains code for all the embedding related functions
- data: contains all the training data and generated cvs
- chatapp: a Django project that expose the API to src

# How to Use:

Generate embedding CVS based on a given text file:
run the embedding_training function in main.py

Generate an answer to a query:
runt the handle_chat function in main.py

# Design Doc:
https://docs.google.com/document/d/11SL-OnSBckfBvf4MjyUOPLEMFVpAbDLLqb20cWLwmW4/edit#
