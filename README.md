# COSMO Data Processing

## Overview

This repository contains scripts for downloading and processing chemical compound data from PubChem, specifically focusing on 3D conformer SDF files.

## Features

- Downloads 3D conformer SDF files from PubChem
- Organizes compounds by CID in separate folders
- Combines individual SDF files into a single file
- Generates a CSV file with CID in ascending order.

## Requirements

- Python 3.x
- pandas
- pubchempy
- requests

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/COSMO-data-processing.git
   cd COSMO-data-processing
   ```

2. Install required packages:
   ```
   pip install pandas pubchempy requests
   ```

## Usage

1. Prepare a CSV file named `compounds.csv` with a column "Compound Name" in the Scripts folder.

2. Run the download script:

   ```
   python download.py
   ```

3. Run the combine script:
   ```
   python combine.py
   ```

## Directory Structure

```
COSMO/
├── Scripts/
│   ├── download.py
│   ├── combine.py
│   └── compounds.csv
└── Data/
    ├── sdf_library/
    └── combined_output/
        ├── combined_compounds.sdf
        └── compound_list.csv
```
