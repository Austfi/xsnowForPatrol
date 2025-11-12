# xsnowForPatrol: A Beginner's Guide to xsnow

A comprehensive Python tutorial repository for learning how to use `xsnow`, a powerful library for working with snowpack simulation data from SNOWPACK and other snow models.

## Overview

This repository contains step-by-step Jupyter notebooks designed to teach you how to use `xsnow` from the ground up. Whether you're an avalanche forecaster, snow researcher, or just curious about snowpack data analysis, these tutorials will guide you through:

- Installing xsnow (each notebook includes installation instructions)
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
   pip install git+https://gitlab.com/avacollabra/postprocessing/xsnow
   ```

   **Note**: The git URL above is correct. For the latest xsnow documentation and API reference, visit [xsnow.avacollabra.org/dev/](https://xsnow.avacollabra.org/dev/).

### Option 3: Using conda

1. Create a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate xsnow-tutorial
   ```

2. Install xsnow from git:
   ```bash
   pip install git+https://gitlab.com/avacollabra/postprocessing/xsnow
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
4. **Open the notebooks in order**, starting with `01_introduction_and_loading_data.ipynb`

## Notebook Progression

The tutorials are designed to be completed in sequence. Each notebook is standalone and includes installation instructions for Colab users:

1. **[01_introduction_and_loading_data.ipynb](notebooks/01_introduction_and_loading_data.ipynb)**
   - Introduction to xsnow and its purpose
   - Understanding the 5-dimensional data model
   - Python fundamentals (NumPy, pandas, xarray basics)
   - Loading and exploring snowpack data files

2. **[02_basic_operations_and_analysis.ipynb](notebooks/02_basic_operations_and_analysis.ipynb)**
   - Selecting and filtering data
   - Basic data operations
   - Computing snowpack metrics (SWE, weak layers, etc.)

3. **[03_visualization.ipynb](notebooks/03_visualization.ipynb)**
   - Creating snow profile plots
   - Time series visualizations
   - Customizing plots for presentations

4. **[04_advanced_analysis.ipynb](notebooks/04_advanced_analysis.ipynb)**
   - Stability indices and hazard calculations
   - Advanced temporal analysis
   - Using xsnow extensions

5. **[05_working_with_custom_data.ipynb](notebooks/05_working_with_custom_data.ipynb)**
   - Preparing your own .pro and .smet files
   - Loading custom data
   - Troubleshooting common issues

6. **[06_extending_xsnow.ipynb](notebooks/06_extending_xsnow.ipynb)**
   - Understanding xsnow's architecture
   - Creating custom extensions
   - Contributing to xsnow

## Sample Data

All tutorials use xsnow's built-in lightweight sample datasets! No need to download anything - the notebooks automatically load sample data using:

- **`xsnow.single_profile()`**: Single snow profile (no time dimension) - used in notebook 06
- **`xsnow.single_profile_timeseries()`**: Time series of profiles - used in notebooks 01-05

These are lightweight datasets included with xsnow, perfect for learning. For more sample datasets and detailed information, see [data/README.md](data/README.md) and the [xsnow API documentation](https://xsnow.avacollabra.org/dev/).

## Learning Objectives

By the end of these tutorials, you will be able to:

- ✅ Load and inspect snowpack data from SNOWPACK model outputs
- ✅ Understand the structure of xsnowDataset and how it organizes data
- ✅ Perform common snowpack analyses (SWE, weak layers, stability indices)
- ✅ Create publication-quality visualizations
- ✅ Work with your own snowpack data
- ✅ Extend xsnow for custom analysis needs

## Resources

- **xsnow API Documentation**: [xsnow.avacollabra.org/dev/](https://xsnow.avacollabra.org/dev/) - Complete API reference, tutorials, and sample data documentation
- **xsnow Getting Started**: [xsnow.avacollabra.org/dev/getting_started.html](https://xsnow.avacollabra.org/dev/getting_started.html) - Official getting started guide
- **SNOWPACK Model**: [snowpack.slf.ch](https://snowpack.slf.ch) - SNOWPACK model documentation
- **xarray Documentation**: [docs.xarray.dev](https://docs.xarray.dev) - xarray fundamentals (xsnow is built on xarray)

## Contributing

This is a learning resource! If you find errors, have suggestions, or want to add examples, contributions are welcome. Please open an issue or submit a pull request.

### Development workflow

To contribute code or documentation updates, install the development tooling and pre-commit hooks:

```bash
pip install -r requirements.txt
pre-commit install
```

Running `pre-commit run --all-files` before opening a pull request helps ensure formatting (via Black and Ruff), strips notebook outputs with nbstripout, and catches trailing whitespace issues early.


## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This tutorial repository is built to help users learn xsnow, which is developed by the avalanche research community. Special thanks to all the contributors to the xsnow project.
