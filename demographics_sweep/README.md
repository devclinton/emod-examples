# Overview

This example demostrates how to perform sweeps within idmtools/EMOD workflows

# Detailed Explantation

## Run Environment

This would run using the [orchestration environment](https://github.com/devclinton/emod-examples/tree/main/orchestration-enviroment). See 

## Submission Script

### manifest.py

Mainfest holds most of the common configuration pameters for EMOD workflows in emodpy
https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/manifest.py#L8-L19

### Input Files

- https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/dtk_sif.id - This is reference to asset that container singularity image environment in COMPS
- https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/experiment_id - This is experiment id from a previous run
- https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/demographics.json - Demographics input file for EMOD

## example.py - Submission script

1. The functions defined in https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/example.py#L25-L99 are all around configuration of each simulation defined later within https://github.com/devclinton/emod-examples/blob/main/demographics_sweep/example.py#L102
