from opf.helper import get_current_load, run_opf_single, print_current_loads

file_name = "data.m"

# Print current loads
print_current_loads(file_path=file_name)


# Configuration
bus_numbers_abs = [5, 3]
new_loads_abs = [60.0, 55.0]

# Set to False to skip saving results to TXT file
save_to_file = True

# Run OPF (base case if variables are commented out)
run_opf_single(file_path=file_name, save_to_file=save_to_file)
