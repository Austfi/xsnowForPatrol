# xsnowForPatrol: A Beginner's Guide to xsnow

A comprehensive Python tutorial repository for learning how to use `xsnow`, a powerful library for working with snowpack simulation data from SNOWPACK and other snow models.

## Overview

This repository contains step-by-step Jupyter notebooks designed to teach you how to use `xsnow` from the ground up. Whether you're an avalanche forecaster, snow researcher, or just curious about snowpack data analysis, these tutorials will guide you through:

- Installing and setting up xsnow
- Understanding the xsnow data model
- Loading and exploring snowpack data
- Performing basic and advanced analyses
- Creating visualizations
- Working with your own data
- Extending xsnow for custom applications

## Prerequisites

- Basic Python knowledge (variables, functions, basic data types)
- Familiarity with Jupyter notebooks (helpful but not required)
- No prior experience with NumPy, pandas, or xarray needed (we'll cover the basics)

## Installation

### Option 1: Google Colab (Easiest - No Local Setup!)

Click the "Open in Colab" badge at the top of any notebook to open it directly in Google Colab. Then run the installation cell to install xsnow from git.

### Option 2: Local Installation

xsnow is not available via standard pip, so you need to install it from the git repository:

1. Create a virtual environment (recommended):
   ```bash
   python -m venv xsnow-env
   source xsnow-env/bin/activate  # On Windows: xsnow-env\Scripts\activate
   ```

2. Install dependencies and xsnow:
   ```bash
   pip install numpy pandas xarray matplotlib seaborn dask netcdf4
   pip install git+https://gitlab.com/avacollabra/xsnow.git
   ```

   **Note**: Update the git URL to the actual xsnow repository location. Check [xsnow documentation](https://xsnow.avacollabra.org) for the correct repository URL.

### Option 3: Using conda

1. Create a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate xsnow-tutorial
   ```

2. Install xsnow from git:
   ```bash
   pip install git+https://gitlab.com/avacollabra/xsnow.git
   ```

## Quick Start

### Using Google Colab (Recommended for Beginners)

1. **Click the "Open in Colab" badge** at the top of any notebook
2. **Run the installation cell** to install xsnow from git
3. **Start learning!** Work through the notebooks in order

### Using Local Jupyter

1. **Clone or download this repository**
2. **Install dependencies** (see Installation above)
3. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```
4. **Open the notebooks in order**, starting with `01_installation_and_setup.ipynb`

## Notebook Progression

The tutorials are designed to be completed in sequence:

1. **[01_installation_and_setup.ipynb](notebooks/01_installation_and_setup.ipynb)**
   - Setting up your Python environment
   - Installing xsnow and dependencies
   - Verifying your installation

2. **[02_introduction_and_loading_data.ipynb](notebooks/02_introduction_and_loading_data.ipynb)**
   - Introduction to xsnow and its purpose
   - Understanding the 5-dimensional data model
   - Python fundamentals (NumPy, pandas, xarray basics)
   - Loading and exploring snowpack data files

3. **[03_basic_operations_and_analysis.ipynb](notebooks/03_basic_operations_and_analysis.ipynb)**
   - Selecting and filtering data
   - Basic data operations
   - Computing snowpack metrics (SWE, weak layers, etc.)

4. **[04_visualization.ipynb](notebooks/04_visualization.ipynb)**
   - Creating snow profile plots
   - Time series visualizations
   - Customizing plots for presentations

5. **[05_advanced_analysis.ipynb](notebooks/05_advanced_analysis.ipynb)**
   - Stability indices and hazard calculations
   - Advanced temporal analysis
   - Using xsnow extensions

6. **[06_working_with_custom_data.ipynb](notebooks/06_working_with_custom_data.ipynb)**
   - Preparing your own .pro and .smet files
   - Loading custom data
   - Troubleshooting common issues

7. **[07_extending_xsnow.ipynb](notebooks/07_extending_xsnow.ipynb)**
   - Understanding xsnow's architecture
   - Creating custom extensions
   - Contributing to xsnow

## Sample Data

To follow along with the tutorials, you'll need sample data files. See [data/README.md](data/README.md) for instructions on how to obtain sample .pro and .smet files from xsnow or SNOWPACK.

## Learning Objectives

By the end of these tutorials, you will be able to:

- ✅ Load and inspect snowpack data from SNOWPACK model outputs
- ✅ Understand the structure of xsnowDataset and how it organizes data
- ✅ Perform common snowpack analyses (SWE, weak layers, stability indices)
- ✅ Create publication-quality visualizations
- ✅ Work with your own snowpack data
- ✅ Extend xsnow for custom analysis needs

## Resources

- **xsnow Documentation**: [xsnow.avacollabra.org](https://xsnow.avacollabra.org)
- **SNOWPACK Model**: [snowpack.slf.ch](https://snowpack.slf.ch)
- **xarray Documentation**: [docs.xarray.dev](https://docs.xarray.dev)

## Contributing

This is a learning resource! If you find errors, have suggestions, or want to add examples, contributions are welcome. Please open an issue or submit a pull request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This tutorial repository is built to help users learn xsnow, which is developed by the avalanche research community. Special thanks to all the contributors to the xsnow project.
