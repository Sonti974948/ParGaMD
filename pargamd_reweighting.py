#!/usr/bin/env python3
"""
ParGaMD Reweighting Tool
========================

A comprehensive tool for reweighting Gaussian Accelerated MD (GaMD) data using
both Cumulative Expansion (CE) and Maclaurin Series (MC) methods with Weighted
Ensemble (WE) support.

Author: Anugraha Thyagatur Kidigannappa (original) + Enhanced version (Siddharth Sonti)
Requirements: numpy, matplotlib, tqdm, yaml, scipy

Usage Examples:
    # CE method (1D)
    python pargamd_reweighting.py ce --input data_1d.dat --dimensions 1d --temperature 300
    
    # CE method (2D)
    python pargamd_reweighting.py ce --input data_2d.dat --dimensions 2d --temperature 300
    
    # MC method (2D only)
    python pargamd_reweighting.py mc --input data_2d.dat --order 10 --temperature 300
    
    # Using configuration file
    python pargamd_reweighting.py ce --config config.yaml
    
    # With plotting
    python pargamd_reweighting.py ce --input data.dat --plot --output-dir results/
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import yaml
import argparse
from pathlib import Path
from tqdm import tqdm

import warnings
from typing import Tuple, Optional, Dict, Any, Union
import logging

# Constants
k_B = 0.001987  # Boltzmann constant in kcal/(mol*K)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ParGaMDReweightingError(Exception):
    """Custom exception for ParGaMD reweighting errors."""
    pass

class InputValidationError(ParGaMDReweightingError):
    """Exception for input validation errors."""
    pass

class DataProcessingError(ParGaMDReweightingError):
    """Exception for data processing errors."""
    pass

def validate_input_file(filepath: str, expected_columns: int, line_number: Optional[int] = None) -> np.ndarray:
    """
    Validate and load input file with detailed error reporting.
    
    Args:
        filepath: Path to input file
        expected_columns: Expected number of columns
        line_number: Specific line to check (for detailed errors)
    
    Returns:
        Loaded data array
    
    Raises:
        InputValidationError: If file cannot be loaded or has wrong format
    """
    try:
        if not os.path.exists(filepath):
            raise InputValidationError(f"Input file not found: {filepath}")
        
        # Try to load the data
        data = np.loadtxt(filepath)
        
        if len(data.shape) == 1:
            raise InputValidationError(
                f"Data appears to be 1D array with {len(data)} elements. "
                f"Expected 2D array with {expected_columns} columns. "
                f"Check if your data file has the correct format."
            )
        
        if data.shape[1] != expected_columns:
            raise InputValidationError(
                f"Expected {expected_columns} columns, but found {data.shape[1]} columns. "
                f"File: {filepath}, Shape: {data.shape}. "
                f"Please check your input file format."
            )
        
        if data.shape[0] == 0:
            raise InputValidationError(f"Input file is empty: {filepath}")
        
        # Check for NaN or infinite values
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            nan_rows = np.where(np.isnan(data).any(axis=1))[0]
            inf_rows = np.where(np.isinf(data).any(axis=1))[0]
            error_msg = f"Found invalid data in file {filepath}:"
            if len(nan_rows) > 0:
                error_msg += f" NaN values in rows {nan_rows[:5]}{'...' if len(nan_rows) > 5 else ''}"
            if len(inf_rows) > 0:
                error_msg += f" Infinite values in rows {inf_rows[:5]}{'...' if len(inf_rows) > 5 else ''}"
            raise InputValidationError(error_msg)
        
        logger.info(f"Successfully loaded {data.shape[0]} snapshots with {data.shape[1]} columns from {filepath}")
        return data
        
    except ValueError as e:
        # This usually means there's a formatting issue in the file
        if line_number:
            raise InputValidationError(
                f"Error parsing line {line_number} in {filepath}: {str(e)}. "
                f"Please check the data format at this line."
            )
        else:
            raise InputValidationError(
                f"Error parsing file {filepath}: {str(e)}. "
                f"Please check that all lines have the same number of columns and valid numeric data."
            )
    except Exception as e:
        raise InputValidationError(f"Unexpected error loading {filepath}: {str(e)}")

def load_data_1d(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load 1D data with validation.
    
    Expected format: [RC, dV, w_WE] (3 columns)
    
    Returns:
        Tuple of (rc, dV, w_WE) arrays
    """
    data = validate_input_file(filepath, 3)
    
    rc = data[:, 0]
    dV = data[:, 1]
    w_WE = data[:, 2]
    
    # Additional validation
    if np.any(w_WE <= 0):
        negative_weights = np.sum(w_WE <= 0)
        raise InputValidationError(
            f"Found {negative_weights} non-positive weights in column 3. "
            f"All weights must be positive."
        )
    
    return rc, dV, w_WE

def load_data_2d(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Load 2D data with validation.
    
    Expected format: [cv1, cv2, dV, w_WE] (4 columns)
    
    Returns:
        Tuple of (cv1, cv2, dV, w_WE) arrays
    """
    data = validate_input_file(filepath, 4)
    
    cv1 = data[:, 0]
    cv2 = data[:, 1]
    dV = data[:, 2]
    w_WE = data[:, 3]
    
    # Additional validation
    if np.any(w_WE <= 0):
        negative_weights = np.sum(w_WE <= 0)
        raise InputValidationError(
            f"Found {negative_weights} non-positive weights in column 4. "
            f"All weights must be positive."
        )
    
    return cv1, cv2, dV, w_WE

def define_bins(values: np.ndarray, disc: float, xy_range: Optional[Tuple[float, float]] = None) -> np.ndarray:
    """
    Define bin edges for histogramming.
    
    Args:
        values: Data values
        disc: Bin width
        xy_range: Optional (min, max) range
    
    Returns:
        Array of bin edges
    """
    if xy_range is not None:
        xmin, xmax = xy_range
    else:
        vmin, vmax = np.min(values), np.max(values)
        # Round outward to multiples of disc for neat bins
        xmin = disc * (int(vmin/disc) - 1)
        xmax = disc * (int(vmax/disc) + 1)
    
    nbins = int((xmax - xmin)/disc + 0.9999)
    edges = np.arange(nbins+1)*disc + xmin
    return edges

def compute_cumulants(sum_w: np.ndarray, sum_w_dV: np.ndarray, 
                     sum_w_dV2: np.ndarray, sum_w_dV3: np.ndarray, 
                     cutoff: float, T: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute cumulants c1, c2, c3 for CE method.
    
    Args:
        sum_w: Sum of weights in each bin
        sum_w_dV: Sum of weights * dV in each bin
        sum_w_dV2: Sum of weights * dV^2 in each bin
        sum_w_dV3: Sum of weights * dV^3 in each bin
        cutoff: Minimum weight threshold
        T: Temperature
    
    Returns:
        Tuple of (c1, c2, c3) cumulant arrays
    """
    beta = 1.0/(k_B * T)
    shape = sum_w.shape
    
    c1 = np.zeros(shape)
    c2 = np.zeros(shape)
    c3 = np.zeros(shape)
    
    # Find bins with sufficient weight
    valid_bins = sum_w >= cutoff
    
    if np.any(valid_bins):
        mean_dV = np.where(valid_bins, sum_w_dV / sum_w, 0.0)
        mean_dV2 = np.where(valid_bins, sum_w_dV2 / sum_w, 0.0)
        mean_dV3 = np.where(valid_bins, sum_w_dV3 / sum_w, 0.0)
        
        var_dV = mean_dV2 - mean_dV**2
        
        # 1st cumulant: c1 = beta * <dV>
        c1 = np.where(valid_bins, beta * mean_dV, 0.0)
        
        # 2nd cumulant: c2 = 1/2 * beta^2 * variance
        c2 = np.where(valid_bins, 0.5 * (beta**2) * var_dV, 0.0)
        
        # 3rd cumulant: c3 = (1/6)*beta^3*(<dV^3>-3<dV^2><dV>+2<dV>^3)
        c3 = np.where(valid_bins, 
                     (1.0/6.0) * (beta**3) * (mean_dV3 - 3.0*mean_dV2*mean_dV + 2.0*(mean_dV**3)), 
                     0.0)
    
    return c1, c2, c3

def reweight_ce_1d(rc: np.ndarray, dV: np.ndarray, w_WE: np.ndarray, 
                   binsX: np.ndarray, discX: float, cutoff: float, T: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute CE reweighting for 1D data.
    
    Returns:
        Tuple of (hist, newedges, c1, c2, c3)
    """
    beta = 1.0/(k_B * T)
    nbins = len(binsX) - 1
    
    sum_w = np.zeros(nbins)
    sum_w_dV = np.zeros(nbins)
    sum_w_dV2 = np.zeros(nbins)
    sum_w_dV3 = np.zeros(nbins)
    
    # Bin assignment & accumulation with progress bar
    for i in tqdm(range(len(rc)), desc="Processing 1D CE bins"):
        bx = int((rc[i] - binsX[0])//discX)
        if bx < 0 or bx >= nbins:
            continue
        w = w_WE[i]
        dv_i = dV[i]
        sum_w[bx] += w
        sum_w_dV[bx] += np.log(w)/beta + dv_i
        sum_w_dV2[bx] += np.power(np.log(w)/beta + dv_i, 2)
        sum_w_dV3[bx] += np.power(np.log(w)/beta + dv_i, 3)
    
    # Compute cumulants
    c1, c2, c3 = compute_cumulants(sum_w, sum_w_dV, sum_w_dV2, sum_w_dV3, cutoff, T)
    
    # Raw histogram
    hist, newedges = np.histogram(rc, bins=binsX, weights=w_WE)
    
    return hist, newedges, c1, c2, c3

def reweight_ce_2d(cv1: np.ndarray, cv2: np.ndarray, dV: np.ndarray, w_WE: np.ndarray,
                   binsX: np.ndarray, binsY: np.ndarray, discX: float, discY: float, 
                   cutoff: float, T: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute CE reweighting for 2D data.
    
    Returns:
        Tuple of (hist2D, edgesX, edgesY, c1_2D, c2_2D, c3_2D)
    """
    beta = 1.0/(k_B * T)
    nx = len(binsX) - 1
    ny = len(binsY) - 1
    
    sum_w = np.zeros((nx, ny))
    sum_w_dV = np.zeros((nx, ny))
    sum_w_dV2 = np.zeros((nx, ny))
    sum_w_dV3 = np.zeros((nx, ny))
    
    # Bin assignment with progress bar
    for i in tqdm(range(len(cv1)), desc="Processing 2D CE bins"):
        bx = int((cv1[i] - binsX[0]) // discX)
        by = int((cv2[i] - binsY[0]) // discY)
        if bx < 0 or bx >= nx or by < 0 or by >= ny:
            continue
        w = w_WE[i]
        dv_i = dV[i]
        sum_w[bx, by] += w
        sum_w_dV[bx] += np.log(w)/beta + dv_i
        sum_w_dV2[bx] += np.power(np.log(w)/beta + dv_i, 2)
        sum_w_dV3[bx] += np.power(np.log(w)/beta + dv_i, 3)
    
    # Compute cumulants
    c1_2D, c2_2D, c3_2D = compute_cumulants(sum_w, sum_w_dV, sum_w_dV2, sum_w_dV3, cutoff, T)
    
    # 2D raw histogram
    hist2D, edgesX, edgesY = np.histogram2d(cv1, cv2, bins=[binsX, binsY], weights=w_WE)
    
    return hist2D, edgesX, edgesY, c1_2D, c2_2D, c3_2D

def compute_maclaurin_expansion(dV: np.ndarray, order: int, T: float) -> np.ndarray:
    """
    Compute Maclaurin series expansion of exp(beta * dV).
    
    Args:
        dV: GaMD boost potential
        order: Order of expansion
        T: Temperature
    
    Returns:
        Maclaurin expansion weights
    """
    beta = 1.0/(k_B * T)
    mc_weight = np.zeros(len(dV))
    beta_dV = beta * dV
    
    for k in tqdm(range(order+1), desc="Computing Maclaurin expansion"):
        term = np.power(beta_dV, k) / np.math.factorial(k)
        mc_weight += term
    
    return mc_weight

def reweight_mc_2d(cv1: np.ndarray, cv2: np.ndarray, dV: np.ndarray, w_WE: np.ndarray,
                   binsX: np.ndarray, binsY: np.ndarray, order: int, T: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute MC reweighting for 2D data.
    
    Returns:
        Tuple of (hist2D, edgesX, edgesY)
    """
    # Compute Maclaurin expansion
    mc_weight = compute_maclaurin_expansion(dV, order, T)
    
    # Combine with WE weights
    combined_weight = w_WE * mc_weight
    
    # Build 2D histogram
    hist2D, edgesX, edgesY = np.histogram2d(
        cv1, cv2,
        bins=(binsX, binsY),
        weights=combined_weight
    )
    
    return hist2D, edgesX, edgesY

def histogram_to_pmf(hist: np.ndarray, T: float) -> np.ndarray:
    """
    Convert histogram to PMF.
    
    Args:
        hist: Histogram array (1D or 2D)
        T: Temperature
    
    Returns:
        PMF array
    """
    kT = k_B * T
    hist_safe = hist + 1e-18
    pmf_temp = kT * np.log(hist_safe)
    pmf = np.max(pmf_temp) - pmf_temp
    return pmf

def normalize_pmf(pmf: np.ndarray, Emax: float) -> np.ndarray:
    """
    Normalize PMF by shifting minimum to 0 and capping at Emax.
    
    Args:
        pmf: PMF array
        Emax: Maximum energy cutoff
    
    Returns:
        Normalized PMF
    """
    finite_mask = np.isfinite(pmf)
    if np.any(finite_mask):
        pmf_min = np.min(pmf[finite_mask])
    else:
        pmf_min = 0.0
    
    pmf_norm = pmf - pmf_min
    pmf_norm[~finite_mask] = Emax
    pmf_norm[pmf_norm > Emax] = Emax
    
    return pmf_norm

def write_pmf_1d(filename: str, pmf: np.ndarray, bin_edges: np.ndarray) -> None:
    """
    Write 1D PMF to file.
    
    Args:
        filename: Output filename
        pmf: PMF values
        bin_edges: Bin edges
    """
    with open(filename, 'w') as f:
        f.write("# RC   PMF(kcal/mol)\n")
        for i in range(len(pmf)):
            rc_mid = 0.5*(bin_edges[i] + bin_edges[i+1])
            f.write(f"{rc_mid:12.5f}  {pmf[i]:12.5f}\n")
    logger.info(f"1D PMF written to {filename}")

def write_pmf_2d(filename: str, pmf: np.ndarray, edgesX: np.ndarray, edgesY: np.ndarray) -> None:
    """
    Write 2D PMF to file.
    
    Args:
        filename: Output filename
        pmf: 2D PMF array
        edgesX: X bin edges
        edgesY: Y bin edges
    """
    with open(filename, 'w') as f:
        f.write("# X   Y   PMF(kcal/mol)\n@TYPE xy\n")
        nx = len(edgesX) - 1
        ny = len(edgesY) - 1
        for i in range(nx):
            xcenter = 0.5*(edgesX[i]+edgesX[i+1])
            for j in range(ny):
                ycenter = 0.5*(edgesY[j]+edgesY[j+1])
                val = pmf[i,j]
                f.write(f"{xcenter:12.4f} {ycenter:12.4f} {val:12.4f}\n")
            f.write("\n")
    logger.info(f"2D PMF written to {filename}")

def create_plots(pmf_data: Dict[str, np.ndarray], output_dir: str, method: str, dimensions: str) -> None:
    """
    Create plots of PMF results.
    
    Args:
        pmf_data: Dictionary of PMF arrays
        output_dir: Output directory
        method: Reweighting method ('ce' or 'mc')
        dimensions: Dimensions ('1d' or '2d')
    """
    plt.style.use('default')
    
    if dimensions == '1d':
        fig, axes = plt.subplots(1, len(pmf_data), figsize=(5*len(pmf_data), 5))
        if len(pmf_data) == 1:
            axes = [axes]
        
        for i, (name, pmf) in enumerate(pmf_data.items()):
            axes[i].plot(pmf, 'b-', linewidth=2)
            axes[i].set_title(f'{name.upper()} PMF')
            axes[i].set_xlabel('Bin Index')
            axes[i].set_ylabel('Free Energy (kcal/mol)')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/pmf_1d_{method}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
    elif dimensions == '2d':
        fig, axes = plt.subplots(1, len(pmf_data), figsize=(5*len(pmf_data), 5))
        if len(pmf_data) == 1:
            axes = [axes]
        
        for i, (name, pmf) in enumerate(pmf_data.items()):
            im = axes[i].imshow(pmf.T, origin='lower', cmap='viridis', aspect='auto')
            axes[i].set_title(f'{name.upper()} PMF')
            axes[i].set_xlabel('X Bin')
            axes[i].set_ylabel('Y Bin')
            plt.colorbar(im, ax=axes[i], label='Free Energy (kcal/mol)')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/pmf_2d_{method}.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    logger.info(f"Plots saved to {output_dir}/")



def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to YAML config file
    
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_file}")
        return config
    except Exception as e:
        raise InputValidationError(f"Error loading config file {config_file}: {str(e)}")

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="ParGaMD Reweighting Tool - CE and MC methods for GaMD + WE data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # CE method (1D)
  python pargamd_reweighting.py ce --input data_1d.dat --dimensions 1d --temperature 300
  
  # CE method (2D)
  python pargamd_reweighting.py ce --input data_2d.dat --dimensions 2d --temperature 300
  
  # MC method (2D only)
  python pargamd_reweighting.py mc --input data_2d.dat --order 10 --temperature 300
  
  # Using configuration file
  python pargamd_reweighting.py ce --config config.yaml
  
  # With plotting
  python pargamd_reweighting.py ce --input data.dat --plot --output-dir results/
        """
    )
    
    # Subparsers for different methods
    subparsers = parser.add_subparsers(dest='method', help='Reweighting method')
    
    # CE method parser
    ce_parser = subparsers.add_parser('ce', help='Cumulative Expansion method')
    ce_parser.add_argument('--input', help='Input data file')
    ce_parser.add_argument('--dimensions', choices=['1d', '2d'], required=True,
                          help='Dimensionality of the data')
    ce_parser.add_argument('--temperature', type=float, default=300.0,
                          help='Temperature in K (default: 300)')
    ce_parser.add_argument('--bin-width', type=float, default=0.2,
                          help='Bin width (default: 0.2)')
    ce_parser.add_argument('--x-range', nargs=2, type=float, default=None,
                          help='X range: min max')
    ce_parser.add_argument('--y-range', nargs=2, type=float, default=None,
                          help='Y range: min max (2D only)')
    ce_parser.add_argument('--cutoff', type=float, default=10.0,
                          help='Minimum weight threshold (default: 10)')
    ce_parser.add_argument('--energy-cutoff', type=float, default=8.0,
                          help='Maximum energy cutoff (default: 8.0 kcal/mol)')
    
    # MC method parser
    mc_parser = subparsers.add_parser('mc', help='Maclaurin Series method')
    mc_parser.add_argument('--input', help='Input data file')
    mc_parser.add_argument('--order', type=int, default=10,
                          help='Order of Maclaurin expansion (default: 10)')
    mc_parser.add_argument('--temperature', type=float, default=300.0,
                          help='Temperature in K (default: 300)')
    mc_parser.add_argument('--bin-width-x', type=float, default=0.5,
                          help='Bin width in X dimension (default: 0.5)')
    mc_parser.add_argument('--bin-width-y', type=float, default=0.5,
                          help='Bin width in Y dimension (default: 0.5)')
    mc_parser.add_argument('--x-range', nargs=2, type=float, default=None,
                          help='X range: min max')
    mc_parser.add_argument('--y-range', nargs=2, type=float, default=None,
                          help='Y range: min max')
    mc_parser.add_argument('--energy-cutoff', type=float, default=8.0,
                          help='Maximum energy cutoff (default: 8.0 kcal/mol)')
    
    # Common arguments
    for subparser in [ce_parser, mc_parser]:
        subparser.add_argument('--config', help='YAML configuration file')
        subparser.add_argument('--output-dir', default='./',
                              help='Output directory (default: current directory)')
        subparser.add_argument('--plot', action='store_true',
                              help='Generate plots')

    
    args = parser.parse_args()
    
    if not args.method:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Load config if provided
        if args.config:
            config = load_config(args.config)
            # Override config with command line arguments
            for key, value in vars(args).items():
                if value is not None and key != 'config':
                    config[key] = value
            args = argparse.Namespace(**config)
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate input file
        if not args.input:
            raise InputValidationError("Input file must be specified (--input)")
        
        logger.info(f"Starting {args.method.upper()} reweighting...")
        
        if args.method == 'ce':
            if args.dimensions == '1d':
                # Load 1D data
                rc, dV, w_WE = load_data_1d(args.input)
                
                # Define bins
                binsX = define_bins(rc, args.bin_width, args.x_range)
                
                # Perform CE reweighting
                hist, newedges, c1, c2, c3 = reweight_ce_1d(
                    rc, dV, w_WE, binsX, args.bin_width, args.cutoff, args.temperature
                )
                
                # Convert to PMF
                pmf_raw = histogram_to_pmf(hist, args.temperature)
                beta = 1.0/(k_B * args.temperature)
                
                pmf_c1 = normalize_pmf(pmf_raw + (-1.0/beta)*c1, args.energy_cutoff)
                pmf_c2 = normalize_pmf(pmf_raw + (-1.0/beta)*(c1 + c2), args.energy_cutoff)
                pmf_c3 = normalize_pmf(pmf_raw + (-1.0/beta)*(c1 + c2 + c3), args.energy_cutoff)
                
                # Write outputs
                write_pmf_1d(f"{output_dir}/pmf_c1.xvg", pmf_c1, newedges)
                write_pmf_1d(f"{output_dir}/pmf_c2.xvg", pmf_c2, newedges)
                write_pmf_1d(f"{output_dir}/pmf_c3.xvg", pmf_c3, newedges)
                
                pmf_data = {'c1': pmf_c1, 'c2': pmf_c2, 'c3': pmf_c3}
                
            elif args.dimensions == '2d':
                # Load 2D data
                cv1, cv2, dV, w_WE = load_data_2d(args.input)
                
                # Define bins
                binsX = define_bins(cv1, args.bin_width, args.x_range)
                binsY = define_bins(cv2, args.bin_width, args.y_range)
                
                # Perform CE reweighting
                hist2D, edgesX, edgesY, c1_2D, c2_2D, c3_2D = reweight_ce_2d(
                    cv1, cv2, dV, w_WE, binsX, binsY, args.bin_width, args.bin_width,
                    args.cutoff, args.temperature
                )
                
                # Convert to PMF
                pmf_raw_2D = histogram_to_pmf(hist2D, args.temperature)
                beta = 1.0/(k_B * args.temperature)
                
                pmf_c1_2D = normalize_pmf(pmf_raw_2D + (-1.0/beta)*c1_2D, args.energy_cutoff)
                pmf_c2_2D = normalize_pmf(pmf_raw_2D + (-1.0/beta)*(c1_2D + c2_2D), args.energy_cutoff)
                pmf_c3_2D = normalize_pmf(pmf_raw_2D + (-1.0/beta)*(c1_2D + c2_2D + c3_2D), args.energy_cutoff)
                
                # Write outputs
                write_pmf_2d(f"{output_dir}/pmf_c1_2D.xvg", pmf_c1_2D, edgesX, edgesY)
                write_pmf_2d(f"{output_dir}/pmf_c2_2D.xvg", pmf_c2_2D, edgesX, edgesY)
                write_pmf_2d(f"{output_dir}/pmf_c3_2D.xvg", pmf_c3_2D, edgesX, edgesY)
                
                pmf_data = {'c1': pmf_c1_2D, 'c2': pmf_c2_2D, 'c3': pmf_c3_2D}
        
        elif args.method == 'mc':
            # Load 2D data
            cv1, cv2, dV, w_WE = load_data_2d(args.input)
            
            # Define bins
            binsX = define_bins(cv1, args.bin_width_x, args.x_range)
            binsY = define_bins(cv2, args.bin_width_y, args.y_range)
            
            # Perform MC reweighting
            hist2D, edgesX, edgesY = reweight_mc_2d(
                cv1, cv2, dV, w_WE, binsX, binsY, args.order, args.temperature
            )
            
            # Convert to PMF
            pmf_mc = histogram_to_pmf(hist2D, args.temperature)
            pmf_mc = normalize_pmf(pmf_mc, args.energy_cutoff)
            
            # Write output
            write_pmf_2d(f"{output_dir}/pmf-{args.input}.xvg", pmf_mc, edgesX, edgesY)
            
            pmf_data = {'mc': pmf_mc}
        
        # Generate plots if requested
        if args.plot:
            create_plots(pmf_data, str(output_dir), args.method, 
                        args.dimensions if args.method == 'ce' else '2d')
        

        
        logger.info(f"Reweighting completed successfully! Results saved to {output_dir}/")
        
    except (InputValidationError, DataProcessingError) as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

