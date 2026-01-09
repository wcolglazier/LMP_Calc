from opf.helper import print_current_loads, run_opf_loop

data_file = "data.m"

# Print current loads
print_current_loads(file_path=data_file)

# Configuration
bus_numbers = [5, 3]                # Buses to modify
load_starts = [40, 20]              # Starting load values (MW)
load_ends = [50, 30]                # Ending load values (MW)
load_step_sizes = [1, 1]            # Step size for each bus (MW)

# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = False

# Runs OPF
run_opf_loop(bus_numbers, load_starts, load_ends, load_step_sizes, file_path=data_file, save_to_file=save_to_file)

