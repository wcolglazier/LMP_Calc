from opf.helper import get_current_load, run_opf_single, print_current_loads

#powerworld data file name(has to be a .m)
file_name = "data.m"

# Print current loads
print_current_loads(file_path=file_name)


# Configuration
bus_numbers = [5, 3]   # Bus numbers to modify
new_loads = [59, 55]   # New load values in MW


# Set to True to save results to .txt 
# Set to False to not save results
save_to_file = False

# Runs OPF
run_opf_single(file_path=file_name, save_to_file=save_to_file)
