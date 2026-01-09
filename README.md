# LMP_Toolkit

A Python tool that takes a PowerWorld output file and allows users to modify bus-level demand to compute locational marginal prices (LMPs) using optimal power flow (OPF) analysis, enabling fast and computationally efficient evaluation of how prices change across scenarios. The output can also be used for easy integration into machine learning workflows or other types of models.

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

### Input File Format

The tool expects Matpower case files (`.m` format) exported from PowerWorld Simulator. Export your case file in Matpower format and place it in the project directory. The default filename is `data.m`, but you can specify any filename in your scripts.


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

# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = True

# Run OPF
run_opf_single(file_path=file_name, save_to_file=save_to_file)
```

**Step 2:** Run the script:
```bash
python single.py
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

# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = False

# Run loop
run_opf_loop(bus_numbers, load_starts, load_ends, load_step_sizes, file_path=data_file, save_to_file=save_to_file)
```

**Step 2:** Run the script:
```bash
python multiple.py
```

## Example Outputs

### Single OPF Analysis Output


**Console/File Output:**
```text
Base Load Values:
========================================
Bus 2: 25.00 MW
Bus 3: 28.00 MW
Bus 4: 35.00 MW
Bus 5: 70.00 MW
========================================

Loads: Bus 3: 55.00 MW, Bus 5: 58.00 MW
Bus 1: $6.80/MWh
Bus 2: $7.26/MWh
Bus 3: $7.67/MWh
Bus 4: $7.72/MWh
Bus 5: $7.78/MWh
```



### Multiple Load Scenarios Output

**Console/File Output:**
```text
Base Load Values:
========================================
Bus 2: 25.00 MW
Bus 3: 28.00 MW
Bus 4: 35.00 MW
Bus 5: 70.00 MW
========================================

Loads: Bus 3: 20.00 MW, Bus 5: 40.00 MW
Bus 1: $6.61/MWh
Bus 2: $6.89/MWh
Bus 3: $7.08/MWh
Bus 4: $7.13/MWh
Bus 5: $7.16/MWh

Loads: Bus 3: 21.00 MW, Bus 5: 41.00 MW
Bus 1: $6.62/MWh
Bus 2: $6.91/MWh
Bus 3: $7.10/MWh
Bus 4: $7.15/MWh
Bus 5: $7.18/MWh

Loads: Bus 3: 22.00 MW, Bus 5: 42.00 MW
Bus 1: $6.64/MWh
Bus 2: $6.93/MWh
Bus 3: $7.12/MWh
Bus 4: $7.17/MWh
Bus 5: $7.21/MWh
...
```

