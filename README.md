# ParGaMD Reweighting Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourusername/pargamd-reweighting/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/pargamd-reweighting/actions/workflows/test.yml)

<<<<<<< HEAD
A comprehensive tool for reweighting Gaussian Accelerated MD (GaMD) data using both Cumulative Expansion (CE) and Maclaurin Series (MC) methods with Weighted Ensemble (WE) support. 

Created by [Siddharth Sonti](https://github.com/Sonti974948) and [Anugraha Thyagatur](https://github.com/anugrahat) @ UC Davis
=======
A comprehensive tool for reweighting Gaussian Accelerated MD (GaMD) data using both Cumulative Expansion (CE) and Maclaurin Series (MC) methods with Weighted Ensemble (WE) support.
>>>>>>> master

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/pargamd-reweighting.git
cd pargamd-reweighting

# Install dependencies
pip install -r requirements.txt

# Run a quick test
python pargamd_reweighting.py ce --input example_data_1d.dat --dimensions 1d --temperature 300 --plot
```

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Installation](#-installation)
- [Input File Formats](#-input-file-formats)
- [Usage Examples](#-usage-examples)
- [Command Line Options](#-command-line-options)
- [Output Files](#-output-files)
- [Error Handling](#-error-handling)
- [Configuration Files](#-configuration-files)
- [Plotting](#-plotting)
- [Performance Features](#-performance-features)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Dependencies](#-dependencies)
- [Citation](#-citation)
- [License](#-license)

## ✨ Features

- **🔬 Two Reweighting Methods**: 
  - Cumulative Expansion (CE) for 1D and 2D data
<<<<<<< HEAD
  - Maclaurin Series (MC) for 2D data
=======
  - Maclaurin Series (MC) for 1D and 2D data
>>>>>>> master
- **📁 Streamlined Input Handling**: Automatic format detection and validation
- **🐛 Detailed Error Reporting**: Pinpoint errors to specific lines with explanations
- **📊 Progress Tracking**: Visual progress bars for long computations
- **⚙️ Configuration Files**: YAML-based configuration support
- **📈 Plotting**: Automatic generation of PMF plots
- **💻 Command Line Interface**: Easy-to-use CLI with subcommands

## Installation

1. **Clone or download the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Input File Formats

### 1D Data (CE method)
```
# Format: [RC, dV, w_WE] (3 columns)
# RC: Reaction coordinate
# dV: GaMD boost potential (kcal/mol)
# w_WE: Weighted Ensemble weight

1.234  0.567  1.000
2.345  0.789  0.950
3.456  0.123  1.050
...
```

### 2D Data (CE and MC methods)
```
# Format: [cv1, cv2, dV, w_WE] (4 columns)
# cv1: First collective variable
# cv2: Second collective variable
# dV: GaMD boost potential (kcal/mol)
# w_WE: Weighted Ensemble weight

1.234  2.345  0.567  1.000
2.345  3.456  0.789  0.950
3.456  4.567  0.123  1.050
...
```

## Usage Examples

### Basic Usage

#### CE Method (1D)
```bash
python pargamd_reweighting.py ce --input data_1d.dat --dimensions 1d --temperature 300
```

#### CE Method (2D)
```bash
python pargamd_reweighting.py ce --input data_2d.dat --dimensions 2d --temperature 300
```

<<<<<<< HEAD
#### MC Method (2D only)
```bash
python pargamd_reweighting.py mc --input data_2d.dat --order 10 --temperature 300
=======
#### MC Method (1D)
```bash
python pargamd_reweighting.py mc --input data_1d.dat --dimensions 1d --order 10 --temperature 300
```

#### MC Method (2D)
```bash
python pargamd_reweighting.py mc --input data_2d.dat --dimensions 2d --order 10 --temperature 300
>>>>>>> master
```

### Advanced Usage

#### Using Configuration Files
```bash
# CE 1D with config file
python pargamd_reweighting.py ce --config config_ce_1d.yaml

# CE 2D with config file
python pargamd_reweighting.py ce --config config_ce_2d.yaml

<<<<<<< HEAD
=======
# MC 1D with config file
python pargamd_reweighting.py mc --config config_mc_1d.yaml

>>>>>>> master
# MC 2D with config file
python pargamd_reweighting.py mc --config config_mc_2d.yaml
```

#### With Plotting
```bash
python pargamd_reweighting.py ce --input data.dat --dimensions 2d --plot --output-dir results/
```

#### Custom Parameters
```bash
python pargamd_reweighting.py ce \
    --input data.dat \
    --dimensions 2d \
    --temperature 310 \
    --bin-width 0.1 \
    --x-range 0 15 \
    --y-range -5 5 \
    --cutoff 5.0 \
    --energy-cutoff 10.0 \
    --output-dir ./my_results \
    --plot
```

## Command Line Options

### CE Method Options
- `--input`: Input data file (required)
- `--dimensions`: Data dimensionality (`1d` or `2d`, required)
- `--temperature`: Temperature in K (default: 300.0)
- `--bin-width`: Bin width for histogramming (default: 0.2)
- `--x-range`: X range as min max (optional, auto-detect if not specified)
- `--y-range`: Y range as min max (2D only, optional)
- `--cutoff`: Minimum weight threshold (default: 10.0)
- `--energy-cutoff`: Maximum energy cutoff in kcal/mol (default: 8.0)

### MC Method Options
- `--input`: Input data file (required)
<<<<<<< HEAD
- `--order`: Order of Maclaurin expansion (default: 10)
- `--temperature`: Temperature in K (default: 300.0)
- `--bin-width-x`: Bin width in X dimension (default: 0.5)
- `--bin-width-y`: Bin width in Y dimension (default: 0.5)
- `--x-range`: X range as min max (optional)
- `--y-range`: Y range as min max (optional)
=======
- `--dimensions`: Data dimensionality (`1d` or `2d`, required)
- `--order`: Order of Maclaurin expansion (default: 10)
- `--temperature`: Temperature in K (default: 300.0)
- `--bin-width`: Bin width for 1D (default: 0.2)
- `--bin-width-x`: Bin width in X dimension for 2D (default: 0.5)
- `--bin-width-y`: Bin width in Y dimension for 2D (default: 0.5)
- `--x-range`: X range as min max (optional)
- `--y-range`: Y range as min max (2D only, optional)
>>>>>>> master
- `--energy-cutoff`: Maximum energy cutoff in kcal/mol (default: 8.0)

### Common Options
- `--config`: YAML configuration file
- `--output-dir`: Output directory (default: current directory)
- `--plot`: Generate PMF plots


## Output Files

### CE Method Outputs
- `pmf_c1.xvg` / `pmf_c1_2D.xvg`: First cumulant PMF
- `pmf_c2.xvg` / `pmf_c2_2D.xvg`: Second cumulant PMF  
- `pmf_c3.xvg` / `pmf_c3_2D.xvg`: Third cumulant PMF

### MC Method Outputs
<<<<<<< HEAD
- `pmf-{input_file}.xvg`: Maclaurin series PMF
=======
- `pmf_mc_1d.xvg`: 1D Maclaurin series PMF
- `pmf_mc_2d.xvg`: 2D Maclaurin series PMF
>>>>>>> master

### Additional Outputs (when using --plot)
- `pmf_1d_{method}.png` / `pmf_2d_{method}.png`: PMF plots

## Error Handling

The tool provides detailed error messages that pinpoint issues to specific lines and explain the problem:

- **File not found**: Clear path information
- **Wrong number of columns**: Shows expected vs. found columns
- **Invalid data**: Identifies rows with NaN or infinite values
- **Format errors**: Points to specific problematic lines
- **Validation errors**: Explains why data is invalid

## Configuration Files

Configuration files use YAML format and can specify all parameters:

```yaml
method: ce
input: data_2d.dat
dimensions: 2d
temperature: 300.0
bin_width: 0.2
x_range: [0.0, 10.0]
y_range: [-2.0, 2.0]
cutoff: 10.0
energy_cutoff: 8.0
output_dir: ./results
plot: true
analyze: true
```



## Plotting

When using `--plot`, the tool generates:
- **1D**: Line plots of PMF vs. bin index
- **2D**: Heatmap plots with colorbars
- High-resolution PNG files (300 DPI)
- Professional styling with proper labels

## Performance Features

- **Progress bars**: Visual feedback for long computations
- **Memory efficient**: Handles large datasets
- **Vectorized operations**: Fast numerical computations
- **Parallel processing**: Where applicable

## Troubleshooting

### Common Issues

1. **"Input file not found"**: Check the file path and ensure the file exists
2. **"Expected X columns, but found Y"**: Verify your data format matches the expected format
3. **"Found invalid data"**: Check for NaN or infinite values in your input file
4. **"Non-positive weights"**: Ensure all weights are positive

### Getting Help

Run with `--help` for detailed usage information:
```bash
python pargamd_reweighting.py --help
python pargamd_reweighting.py ce --help
python pargamd_reweighting.py mc --help
```

## Dependencies

- numpy >= 1.20.0
- matplotlib >= 3.3.0
- tqdm >= 4.60.0
- PyYAML >= 5.4.0


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for all functions
- Write tests for new features

## 📚 Citation

If you use this tool in your research, please cite:

```bibtex
<<<<<<< HEAD
@article{sonti2025accelerating,
  title={Accelerating free energy exploration using parallelizable Gaussian accelerated molecular dynamics (ParGaMD)},
  author={Sonti, Siddharth and Thyagatur, Anugraha and Wan, Hung-Yu and Hamelynck, Maxen and Faller, Roland and Ahn, Surl-Hee},
  year={2025}
=======
@software{pargamd_reweighting,
  title={ParGaMD Reweighting Tool},
  author={Kidigannappa, Anugraha Thyagatur and Contributors},
  year={2024},
  url={https://github.com/yourusername/pargamd-reweighting}
>>>>>>> master
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

