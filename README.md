# Crops Growth Analysis

## Introduction

This projects aims to extract NDVI and NDWI values from satellite images and analyze the growth of crops in a given region. The project is divided into three parts: data extraction, data processing and data display. 

- Extract : reading csv and loading sentinel-2 items.
- Process : loading images and calculating the NDVI and NDWI.
- Store : storing the NDVI and NDWI values in a database.
- Display : displaying the NDVI and NDWI values on a map.

Development instructions are available in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

Some notes about development are available in the [NOTES.md](NOTES.md) file.

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

If you want to start databases locally, you can use docker. Install docker using the following command:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
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
