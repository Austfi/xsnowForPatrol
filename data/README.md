# Sample Data for xsnow Tutorials

This directory is where you should place sample data files for the tutorials. The actual data files are not included in this repository because they can be quite large.

## Obtaining Sample Data

### Option 1: Using xsnow Sample Data

If xsnow provides sample data or example files, check the xsnow documentation:
- Visit [xsnow.avacollabra.org](https://xsnow.avacollabra.org) for the latest documentation
- Look for example datasets or sample files in the xsnow repository

### Option 2: SNOWPACK Example Outputs

SNOWPACK model outputs are typically in `.pro` (profile) or `.smet` (meteorological) formats. You can:

1. **Run SNOWPACK yourself**: If you have SNOWPACK installed, you can generate sample outputs
   - Configure SNOWPACK to output `.pro` files (set `PROF_FORMAT = PRO` in your .ini file)
   - Run a simulation for a test location
   - The output will be in `.pro` format

2. **Download example outputs**: Check the SNOWPACK documentation or community resources for example files
   - SNOWPACK website: [snowpack.slf.ch](https://snowpack.slf.ch)
   - Look for example configurations or test datasets

### Option 3: Using Your Own Data

If you have your own SNOWPACK outputs, you can use those! See notebook `06_working_with_custom_data.ipynb` for guidance on preparing and loading your data.

## File Format Requirements

### .pro Files (Profile Time Series)

SNOWPACK profile files contain:
- Header with station metadata (name, coordinates, elevation)
- Time series of snow profiles
- Layer-by-layer properties (density, temperature, grain type, etc.)

### .smet Files (Meteorological Time Series)

SMET files (MeteoIO format) contain:
- Header with variable descriptions
- Time series of scalar variables (temperature, precipitation, etc.)
- No layered data (just time series)

## File Naming

For the tutorials to work smoothly, you can name your files descriptively:
- `sample_profile.pro` - A sample profile file
- `sample_meteo.smet` - A sample meteorological file
- `VIR1A.pro` - A file named after a station (common SNOWPACK convention)

## Directory Structure

Place your data files directly in this `data/` directory:

```
data/
├── README.md (this file)
├── sample_profile.pro
├── sample_meteo.smet
└── (your other data files)
```

## Notes

- **File Size**: SNOWPACK output files can range from a few KB to several MB depending on the simulation length and number of layers
- **Multiple Files**: You can load multiple files at once using `xsnow.read()` with a list of file paths
- **File Paths**: In the notebooks, we'll reference files using relative paths like `"data/sample_profile.pro"`

## Troubleshooting

If you're having trouble finding or loading data:

1. **Check file format**: Make sure files are actual `.pro` or `.smet` format (not just renamed text files)
2. **Check file location**: Ensure files are in the `data/` directory or update paths in the notebooks
3. **Check file permissions**: Make sure you have read access to the files
4. **See notebook 06**: The custom data notebook covers common issues and solutions

## Example: Downloading from xsnow (if available)

If xsnow provides sample data, you might download it like this:

```python
# Example (check xsnow docs for actual method)
import xsnow
# xsnow.download_sample_data()  # If such a function exists
```

Or manually download from the xsnow repository/examples section.

