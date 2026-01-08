import numpy as np
import inspect
from contextlib import redirect_stdout
from io import StringIO
from .solver import load_matpower_case, modify_load_mpc, run_opf_matpower

_case_cache = {}

def get_case(file_path="data.m"):
    if file_path not in _case_cache:
        f_temp = StringIO()
        with redirect_stdout(f_temp):
            _case_cache[file_path] = load_matpower_case(file_path)
    return _case_cache[file_path]

def get_current_load(bus_num, file_path="data.m"):
    mpc = get_case(file_path)
    bus_indices = np.where(mpc['bus'][:, 0] == bus_num)[0]
    if len(bus_indices) > 0:
        return mpc['bus'][bus_indices[0], 2]
    return None

def print_current_loads(file_path="data.m"):
    mpc = get_case(file_path)
    print("Current Load Values:")
    print("=" * 40)
    for bus in mpc['bus']:
        if bus[2] > 0:
            print(f"Bus {int(bus[0])}: {bus[2]:.2f} MW")
    print("=" * 40)
    print()

def run_opf_with_loads(load_changes, file_path="data.m"):
    f = StringIO()
    with redirect_stdout(f):
        mpc = load_matpower_case(file_path)
        for bus_num, new_load in load_changes.items():
            modify_load_mpc(mpc, bus_num=bus_num, new_load_mw=new_load)
        return run_opf_matpower(mpc)

def save_lmps(results, filename, load_changes=None):
    with open(filename, 'w') as f:
        if load_changes:
            loads_str = ', '.join([f"Bus {bus}: {load:.2f} MW" for bus, load in sorted(load_changes.items())])
            header = f"Loads: {loads_str}"
            print(header)
            f.write(header + '\n')
        
        for _, row in results.iterrows():
            line = f"Bus {row['Bus_Number']}: ${row['LMP_$/MWh']:.2f}/MWh"
            print(line)
            f.write(line + '\n')

def run_opf_single(bus_numbers_abs=None, new_loads_abs=None, bus_numbers_delta=None, delta_changes=None, file_path="data.m", output_file=None):
    frame = inspect.currentframe().f_back
    caller_locals = frame.f_locals if frame else {}
    
    if bus_numbers_abs is None:
        bus_numbers_abs = caller_locals.get('bus_numbers_abs', [])
    if new_loads_abs is None:
        new_loads_abs = caller_locals.get('new_loads_abs', [])
    if bus_numbers_delta is None:
        bus_numbers_delta = caller_locals.get('bus_numbers_delta', [])
    if delta_changes is None:
        delta_changes = caller_locals.get('delta_changes', [])
    
    load_changes = {}
    
    for bus_num, new_load in zip(bus_numbers_abs, new_loads_abs):
        load_changes[bus_num] = new_load
    
    for bus_num, delta in zip(bus_numbers_delta, delta_changes):
        old_load = get_current_load(bus_num, file_path)
        if old_load is not None:
            load_changes[bus_num] = old_load + delta
    
    if output_file is None:
        if load_changes:
            load_desc = "_".join([f"b{b}_{int(p)}MW" for b, p in sorted(load_changes.items())])
            output_file = f"opf_single_{load_desc}.txt"
        else:
            output_file = "opf_single_basecase.txt"
    
    result = run_opf_with_loads(load_changes, file_path=file_path)
    if result is None:
        print("OPF failed to converge!")
        return None
    
    results, _ = result
    save_lmps(results, output_file, load_changes)
    return results

def run_opf_loop(bus_numbers, load_starts, load_ends, load_step_sizes, file_path="data.m", output_file=None):
    load_ranges = [
        np.arange(load_starts[i], load_ends[i] + load_step_sizes[i], load_step_sizes[i])
        for i in range(len(bus_numbers))
    ]
    max_len = max(len(lr) for lr in load_ranges) if load_ranges else 0
    
    if output_file is None:
        range_desc = "_".join(
            [f"b{b}_{int(s)}to{int(e)}MW" for b, s, e in zip(bus_numbers, load_starts, load_ends)]
        )
        output_file = f"opf_loop_{range_desc}.txt"
    
    all_results = []
    for i in range(max_len):
        load_changes = {}
        for bus_idx, bus_num in enumerate(bus_numbers):
            if i < len(load_ranges[bus_idx]):
                load_changes[bus_num] = load_ranges[bus_idx][i]
        
        result = run_opf_with_loads(load_changes, file_path=file_path)
        if result is not None:
            results, _ = result
            all_results.append({'load_changes': load_changes, 'results': results})
    
    with open(output_file, 'w') as f:
        for idx, iteration in enumerate(all_results):
            loads_str = ', '.join([f"Bus {bus}: {load:.2f} MW" for bus, load in sorted(iteration['load_changes'].items())])
            header = f"Loads: {loads_str}"
            print(f"\n{header}" if idx > 0 else header)
            f.write(('\n' if idx > 0 else '') + header + '\n')
            
            for _, row in iteration['results'].iterrows():
                line = f"Bus {row['Bus_Number']}: ${row['LMP_$/MWh']:.2f}/MWh"
                print(line)
                f.write(line + '\n')
    
    return all_results

