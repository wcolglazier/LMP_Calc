# LMP_Toolkit

**LMP_Toolkit** is a Python based tool for efficiently computing **Locational Marginal Prices (LMPs)** from power system models exported from **PowerWorld Simulator**.

The tool allows users to modify electricity demand at individual buses and evaluate how LMPs change in response, using (approximate) **Optimal Power Flow (OPF)** analysis. Instead of manually running a single OPF case, **LMP_Toolkit** is designed for **large scale scenario analysis**, making it easy to run many load variations quickly and consistently.

The resulting outputs are structured text files that are easy to parse and well suited for:

- Data analysis
- Sensitivity studies
- Machine learning workflows

## Features

1. **Single OPF Analysis**

Run an OPF for a specific load configuration to answer targeted "what if" questions.

- Modify load at one or more buses (absolute values or incremental changes)
- Compute locational marginal prices (LMPs) across all buses
- Results are printed to the console and optionally saved to text files

2. **Multiple Load Scenarios (Batch Mode)**

Automatically sweep across many load configurations to study price sensitivity.

- Define load ranges and step sizes for multiple buses
- Run OPF across all combinations of specified load values
- Analyze how LMPs change as bus level load varies
- Consolidated output for easy post processing
- Designed for fast, repeatable scenario sweeps and dataset generation

## Setup

```bash
git clone https://github.com/wcolglazier/LMP_Toolkit.git
cd LMP_Toolkit
pip install -r requirements.txt
```


## How to Use

### Input File Format

The tool expects MATPOWER format (.m) case files exported from PowerWorld Simulator.


### Single OPF Analysis

**Step 1:** Open `single.py` and set your configuration:

```python
from opf.helper import get_current_load, run_opf_single, print_current_loads

file_name = "data.m"

# Print current loads
print_current_loads(file_path=file_name)

# Configuration - modify these values
bus_numbers_abs = [5, 3]        # Bus numbers to modify
new_loads_abs = [60, 55]   # New load values in MW

# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = True

# Runs OPF
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
bus_numbers = [5, 3]                  # Buses to modify
load_starts = [40, 20]                # Starting load values (MW)
load_ends = [50, 30]                  # Ending load values (MW)
load_step_sizes = [1, 1]              # Step size for each bus (MW)

# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = False

# Runs OPF
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

