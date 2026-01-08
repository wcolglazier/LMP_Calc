from opf.helper import print_current_loads, run_opf_loop

data_file = "data.m"

# Print current loads
print_current_loads(file_path=data_file)

# Configuration
bus_numbers = [5, 3]
load_starts = [40.0, 20.0]
load_ends = [50.0, 30.0]
load_step_sizes = [1.0, 1.0]

# Run loop (output file name will encode bus and range)
run_opf_loop(bus_numbers, load_starts, load_ends, load_step_sizes, file_path=data_file)

