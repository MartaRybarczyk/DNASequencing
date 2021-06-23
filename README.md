# Ant Colony algorithm for DNA sequencing by hybridization

![CI status](https://github.com/dziulek/DNASequencing/actions/workflows/build.yml/badge.svg)

## Overview

This is implementation of ant colony optimization algorithm applied to DNA sequencig problem by hybridzation. 

## Setup
Go to the main directory of the project.
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
To run algorithm
```
python main.py <DATA_FILE>
```
For more options type
```
python main.py -h
```

where instead of <DATA_FILE> you should place your file with input for algorithm. Example of how the <DATA_FILE> should look like is in a `demo_file.txt`.