# Ant Colony algorithm for DNA sequencing by hybridization

![CI status](https://github.com/dziulek/DNASequencing/actions/workflows/build.yml/badge.svg)

## Overview

The implementation of the ant colony optimization algorithm applied to DNA sequencing problem by hybridization. 

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
where instead of <DATA_FILE> you should place file name with input. You can look into `demo_file.txt` to see how the <DATA_FILE> should look like.
