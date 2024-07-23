# Crops Growth Analysis

## Introduction

This projects aims to extract NDVI and NDWI values from satellite images and analyze the growth of crops in a given region. The project is divided into three parts: data extraction, data processing and data display. 

- Extract : reading csv and loading sentinel-2 items.
- Process : loading images and calculating the NDVI and NDWI.
- Store : storing the NDVI and NDWI values in a database.

## Pre-requisites

Install pyenv using the following command:

```bash
curl https://pyenv.run | bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```

Restart your terminal and install python:

```bash
# Check if pyenv was installed correctly
pyenv --version
# Install python
pyenv install 3.12.4
# Check if python was installed correctly
python --version
```

## Start Database

Three database may be useful for this project : postgresql, mongodb and minio. To start them, you can use the makefile:

```bash
make start-postgres
make start-mongo
make start-minio
```

This will start the databases locally. You can access them using the following urls:

- Postgres : `postgresql://postgres:postgres@localhost:5432/postgres`
- Mongo : `mongodb://localhost:27017/`
- Minio : `http://localhost:9000`

## Run

To run the project, you can use the makefile : 

```bash
make install run
```
