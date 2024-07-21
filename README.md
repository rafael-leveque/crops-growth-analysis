# Crops Growth Analysis

## Introduction

This projects aims to extract NDVI and NDWI values from satellite images and analyze the growth of crops in a given region. The project is divided into three parts: data extraction, data processing and data display. 

- The data extraction part is responsible for downloading the satellite images from the Microsoft Planetarium API, filtering meaningful informations. 
- The data processing part is responsible for calculating the NDVI and NDWI values from the images. 
- The data display part is responsible for displaying the NDVI and NDWI values in a graph.

## Pre-requisites

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

# Benchmark

To process results, we can either use an external library (stackstac) or use xarrays. The first option is easier to use, but the second option is more flexible  (and has some serious memory economy).

Here is a benchmark comparing the two methods:

| Method | Parcels | Assets | Time (s) | Memory (GB) | Result |
|--------|---------|--------|----------|-------------|--------|
| stackstac | 1 | 1 | 20s | 2.8 | 950 |
| xarrays | 1 | 1 | 30s | 1.6 | 428 |
| stackstac | 1 | 2 | N/A | > 4 | N/A |
| xarrays | 1 | 2 | 46s | 2.8 | 428 |

Now with bounds:

| Method | Parcels | Assets | Time (s) | Memory (GB) | Result |
|--------|---------|--------|----------|-------------|--------|
| stackstac | 1 | 1 | 20s | 3.5 | 950 |
| xarrays | 1 | 1 | 30s | 2 | 428 |
