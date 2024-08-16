# CWL and Dockstore YAML Generator

This project includes a Python script to generate CWL placeholder files and a `.dockstore.yml` file from a CSV containing CWL tool and workflow metadata.

## Overview

- **Placeholder Files**: Creates empty CWL files in directories named after the `label` column from the CSV.
- **.dockstore.yml**: Generates a Dockstore YAML file based on the tool and workflow metadata from the CSV.

## Requirements

- Python 3.x
- pandas
- numpy

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>