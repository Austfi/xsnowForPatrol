# xsnowForPatrol: A Beginner's Guide to xsnow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Austfi/xsnowForPatrol/blob/main/notebooks/01_introduction_and_loading_data.ipynb)

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
- No prior experience with NumPy, pandas, or xarray needed (see notebook 00 for Python fundamentals reference)

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

### Option 3: Using conda (Recommended for Local Development)

**Quick Setup (Automated):**
```bash
# macOS/Linux:
./setup_kernel.sh

# Windows:
setup_kernel.bat
```

**Manual Setup:**
1. Create a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate xsnow-tutorial
   ```

2. Install xsnow from git:
   ```bash
   pip install git+https://gitlab.com/avacollabra/postprocessing/xsnow
   ```

3. Register as Jupyter kernel:
   ```bash
   python -m ipykernel install --user --name xsnow-tutorial --display-name "Python (xsnow-tutorial)"
   ```

**📖 For detailed kernel setup instructions, see [KERNEL_SETUP.md](KERNEL_SETUP.md)**

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

### Main Tutorial Series (Complete in Order)

1. **[01_introduction_and_loading_data.ipynb](notebooks/01_introduction_and_loading_data.ipynb)**
   - Introduction to xsnow and its purpose
   - Understanding the 5-dimensional data model
   - Loading and exploring snowpack data files

2. **[02_basic_operations_and_analysis.ipynb](notebooks/02_basic_operations_and_analysis.ipynb)**
   - Selecting and filtering data
   - Basic data operations
   - Computing snowpack metrics (SWE, weak layers, etc.)

3. **[03_visualization.ipynb](notebooks/03_visualization.ipynb)**
   - Creating snow profile plots
   - Time series visualizations
   - Customizing plots for presentations

4. **[04_advanced_analysis.ipynb](notebooks/04_advanced_analysis.ipynb)** (Gradient and Temporal Analysis)
   - Density and temperature gradient analysis
   - Temporal analysis with rolling windows
   - Comparing multiple locations

5. **[05_working_with_custom_data.ipynb](notebooks/05_working_with_custom_data.ipynb)**
   - Preparing your own .pro and .smet files
   - Loading custom data
   - Troubleshooting common issues
   - Merging multiple data sources

6. **[06_extending_xsnow.ipynb](notebooks/06_extending_xsnow.ipynb)**
   - Understanding xsnow's architecture
   - Creating custom extensions
   - Contributing to xsnow

### Optional Reference Notebooks

These notebooks cover advanced topics and can be consulted as needed:

- **[00_python_fundamentals_reference.ipynb](notebooks/00_python_fundamentals_reference.ipynb)**: Python, NumPy, Pandas, and Xarray basics (for beginners)
- **[07_data_quality_and_cleaning.ipynb](notebooks/07_data_quality_and_cleaning.ipynb)**: Comprehensive missing data handling and data quality strategies
- **[08_advanced_xarray_techniques.ipynb](notebooks/08_advanced_xarray_techniques.ipynb)**: Broadcasting, alignment, groupby, and resampling
- **[09_performance_and_storage.ipynb](notebooks/09_performance_and_storage.ipynb)**: Data type optimization, Zarr format, and performance tuning

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

## Troubleshooting

### Installation Issues

**Problem**: `xsnow` installation fails from git
- **Solution**: Make sure you have `git` installed and can access GitLab. Try: `pip install --upgrade pip` first, then install xsnow.

**Problem**: Import errors after installation
- **Solution**: Verify installation: `python -c "import xsnow; print(xsnow.__version__)"`. If this fails, reinstall xsnow.

**Problem**: Dependencies conflict
- **Solution**: Use a fresh virtual environment. See Installation section above.

### Runtime Issues

**Problem**: Notebooks fail to load sample data
- **Solution**: Make sure xsnow is properly installed. The sample data is included with xsnow, so if loading fails, reinstall xsnow.

**Problem**: Memory errors with large datasets
- **Solution**: Use `dask` for lazy loading (already included in dependencies). Consider loading smaller time ranges or using data chunking.

**Problem**: File not found errors when loading custom data
- **Solution**: Use absolute paths or ensure you're running notebooks from the repository root directory. See notebook 05 for detailed troubleshooting.

## FAQ

### Do I need SNOWPACK installed to use these tutorials?

No! The tutorials use xsnow's built-in sample datasets, so you can learn without having SNOWPACK or any data files. You only need SNOWPACK if you want to work with your own data (covered in notebook 05).

### Can I run these notebooks without installing anything locally?

Yes! Use Google Colab - just click the "Open in Colab" badge at the top of any notebook. The installation cell will set everything up automatically.

### What Python version do I need?

Python 3.8 or higher is required. The tutorials work with Python 3.8, 3.9, 3.10, 3.11, and 3.12.

### How long does it take to complete all tutorials?

Each notebook takes approximately 30-60 minutes depending on your Python experience. The full series can be completed in 4-6 hours.

### Can I use these tutorials with my own data?

Absolutely! Notebook 05 specifically covers working with custom data. You can also adapt examples from other notebooks to your data.

### Where can I get help if I'm stuck?

1. Check the [xsnow API documentation](https://xsnow.avacollabra.org/dev/)
2. Review the troubleshooting section above
3. Open an issue on this repository
4. Check the exercises at the end of each notebook for practice

## Contributing

This is a learning resource! If you find errors, have suggestions, or want to add examples, contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to contribute:
- Report bugs or unclear explanations
- Suggest improvements to examples
- Add new examples or exercises
- Improve documentation
- Fix typos or formatting issues

Please open an issue or submit a pull request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This tutorial repository is built to help users learn xsnow, which is developed by the avalanche research community. Special thanks to all the contributors to the xsnow project.
