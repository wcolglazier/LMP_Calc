# LMP_Toolkit

A Python tool that takes a PowerWorld output file and allows users to modify bus-level demand to compute locational marginal prices (LMPs) using optimal power flow (OPF) analysis, enabling fast and computationally efficient evaluation of how prices change across scenarios.

## Features

### Single OPF Analysis

Run optimal power flow calculations for specific load scenarios to determine locational marginal prices (LMPs) at each bus. Modify loads at specific buses using absolute values or incremental changes from the base case. Results include LMPs, voltages, angles, and power flows for all buses, automatically saved to text files. Ideal for analyzing "what-if" scenarios and evaluating the impact of load changes at specific locations.

### Multiple Load Scenarios

Automatically iterate through ranges of load values to analyze LMP sensitivity and create pricing curves. Define independent load ranges and step sizes for multiple buses simultaneously, with batch processing that runs OPF calculations across all combinations. All scenarios are saved in a consolidated output file for easy comparison. Perfect for creating LMP vs. load curves, identifying critical pricing thresholds, and analyzing transmission congestion patterns.

## Setup

```bash
git clone https://github.com/wcolglazier/LMP_Toolkit.git
cd LMP_Toolkit
pip install -r requirements.txt
```

## How to Use

### Single OPF Analysis

**Step 1:** Open `single.py` and set your configuration:

```python
from opf.helper import get_current_load, run_opf_single, print_current_loads

file_name = "data.m"

# Print current loads
print_current_loads(file_path=file_name)

# Configuration - modify these values
bus_numbers_abs = [5, 3]        # Bus numbers to modify
new_loads_abs = [60.0, 55.0]   # New load values in MW

# Set to False to skip saving results to TXT file
save_to_file = True

# Run OPF
run_opf_single(file_path=file_name, save_to_file=save_to_file)
```

**Step 2:** Run the script:
```bash
python single.py
```

**Step 3:** Results are printed to the console and saved to a text file (e.g., `opf_single_b5_60MW_b3_55MW.txt`) containing LMP values for all buses. Set `save_to_file = False` to only print results without saving to a file.

**Alternative:** You can also use absolute or delta-based changes programmatically:
```python
from opf.helper import run_opf_single

# Absolute load values
run_opf_single(bus_numbers_abs=[5, 3], new_loads_abs=[60.0, 55.0], file_path="data.m", save_to_file=True)

# Delta changes (add/subtract from current load)
run_opf_single(bus_numbers_delta=[5], delta_changes=[10.0], file_path="data.m", save_to_file=False)
```

### Multiple Load Scenarios

**Step 1:** Open `multiple.py` and configure your load ranges:

```python
from opf.helper import print_current_loads, run_opf_loop

data_file = "data.m"

# Print current loads
print_current_loads(file_path=data_file)

# Configuration - modify these values
bus_numbers = [5, 3]                    # Buses to modify
load_starts = [40.0, 20.0]              # Starting load values (MW)
load_ends = [50.0, 30.0]                # Ending load values (MW)
load_step_sizes = [1.0, 1.0]            # Step size for each bus (MW)

# Set to False to skip saving results to TXT file
save_to_file = False

# Run loop
run_opf_loop(bus_numbers, load_starts, load_ends, load_step_sizes, file_path=data_file, save_to_file=save_to_file)
```

**Step 2:** Run the script:
```bash
python multiple.py
```

**Step 3:** Results are printed to the console for each scenario. If `save_to_file = True`, results are also saved to a single text file (e.g., `opf_multiple_b5_40to50MW_b3_20to30MW.txt`) with all scenarios and their corresponding LMP values, including base load values at the top of the file.

### Output Files

Results are printed to the console by default. When `save_to_file = True`, results are also saved to text files in the project directory:

- **Single runs:** `opf_single_b{bus}_{load}MW.txt` or `opf_single_basecase.txt` for base case
- **Multiple runs:** `opf_multiple_b{bus}_{start}to{end}MW.txt`

Each output file contains:
- **Multiple runs:** Base load values from the original case file at the top
- Load configuration for each scenario
- LMP values ($/MWh) for each bus in the system

Set `save_to_file = False` in your script to skip file creation and only print results to the console.

### Input File Format

The tool expects Matpower case files (`.m` format) exported from PowerWorld, containing:
- Bus data (bus numbers, types, loads, voltages)
- Generator data (generation limits, costs)
- Branch data (transmission line parameters)
- Generator cost data
