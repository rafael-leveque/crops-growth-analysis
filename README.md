# Crops Growth Analysis

## Introduction

This projects aims to extract NDVI and NDWI values from satellite images and analyze the growth of crops in a given region. The project is divided into three parts: data extraction, data processing and data display. The data extraction part is responsible for downloading the satellite images from the Microsoft Planetarium API, filtering meaningful informations. The data processing part is responsible for calculating the NDVI and NDWI values from the images. The data display part is responsible for displaying the NDVI and NDWI values in a graph.

## How to install pyenv

Install pyenv using the following command:

```bash
curl https://pyenv.run | bash
```

Add the following lines to your `.bashrc` or `.zshrc` file:

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Restart your terminal and check if pyenv was installed correctly using the following command:

```bash
pyenv --version
```

Install Python 3.12.4 using the following command:

```bash
pyenv install 3.12.4
```

Check if Python was installed correctly using the following command:

```bash
python --version
```
