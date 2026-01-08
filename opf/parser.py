import pandas as pd
import numpy as np
import re

def parse_matpower_file(m_file_path: str):
    with open(m_file_path, 'r') as f:
        content = f.read()
    
    base_mva_match = re.search(r'mpc\.baseMVA\s*=\s*([\d.]+)', content)
    base_mva = float(base_mva_match.group(1)) if base_mva_match else 100.0
    
    bus_match = re.search(r'mpc\.bus\s*=\s*\[(.*?)\];', content, re.DOTALL)
    bus_rows = []
    if bus_match:
        for line in bus_match.group(1).strip().split('\n'):
            line = re.sub(r'%.*', '', line.strip())
            if line and not line.startswith('%'):
                values = line.split()
                if len(values) >= 13:
                    while len(values) < 17:
                        values.append('0.0')
                    bus_rows.append([float(v) for v in values])
    
    bus_columns = ['bus_i', 'type', 'Pd', 'Qd', 'Gs', 'Bs', 'area', 'Vm', 'Va', 
                   'baseKV', 'zone', 'Vmax', 'Vmin', 'lam_P', 'lam_Q', 'mu_Vmax', 'mu_Vmin']
    max_cols = max(len(row) for row in bus_rows) if bus_rows else 17
    bus_df = pd.DataFrame(bus_rows, columns=bus_columns[:max_cols]) if bus_rows else pd.DataFrame()
    
    gen_match = re.search(r'mpc\.gen\s*=\s*\[(.*?)\];', content, re.DOTALL)
    gen_rows = []
    if gen_match:
        for line in gen_match.group(1).strip().split('\n'):
            line = re.sub(r'%.*', '', line.strip())
            if line and not line.startswith('%'):
                values = line.split()
                if len(values) >= 10:
                    while len(values) < 25:
                        values.append('0.0')
                    gen_rows.append([float(v) for v in values])
    
    gen_columns = ['bus', 'Pg', 'Qg', 'Qmax', 'Qmin', 'Vg', 'mBase', 'status', 
                   'Pmax', 'Pmin', 'Pc1', 'Pc2', 'Qc1min', 'Qc1max', 'Qc2min', 
                   'Qc2max', 'ramp_agc', 'ramp_10', 'ramp_30', 'ramp_q', 'apf', 
                   'mu_Pmax', 'mu_Pmin', 'mu_Qmax', 'mu_Qmin']
    max_cols = max(len(row) for row in gen_rows) if gen_rows else 25
    gen_df = pd.DataFrame(gen_rows, columns=gen_columns[:max_cols]) if gen_rows else pd.DataFrame()
    
    gencost_match = re.search(r'mpc\.gencost\s*=\s*\[(.*?)\];', content, re.DOTALL)
    gencost_rows = []
    if gencost_match:
        for line in gencost_match.group(1).strip().split('\n'):
            line = re.sub(r'%.*', '', line.strip())
            if line and not line.startswith('%'):
                values = line.split()
                if len(values) >= 4:
                    gencost_rows.append([float(v) for v in values])
    
    gencost_df = pd.DataFrame(gencost_rows, columns=['model', 'startup', 'shutdown', 'n', 'c0', 'c1', 'c2', 'c3']) if gencost_rows else pd.DataFrame()
    
    branch_match = re.search(r'mpc\.branch\s*=\s*\[(.*?)\];', content, re.DOTALL)
    branch_rows = []
    if branch_match:
        for line in branch_match.group(1).strip().split('\n'):
            line = re.sub(r'%.*', '', line.strip())
            if line and not line.startswith('%'):
                values = line.split()
                if len(values) >= 13:
                    while len(values) < 21:
                        values.append('0.0')
                    branch_rows.append([float(v) for v in values])
    
    branch_columns = ['fbus', 'tbus', 'r', 'x', 'b', 'rateA', 'rateB', 'rateC', 
                      'ratio', 'angle', 'status', 'angmin', 'angmax', 'Pf', 'Qf', 
                      'Pt', 'Qt', 'mu_Sf', 'mu_St', 'mu_angmin', 'mu_angmax']
    max_cols = max(len(row) for row in branch_rows) if branch_rows else 21
    branch_df = pd.DataFrame(branch_rows, columns=branch_columns[:max_cols]) if branch_rows else pd.DataFrame()
    
    bus_name_match = re.search(r'mpc\.bus_name\s*=\s*\{(.*?)\};', content, re.DOTALL)
    bus_names = []
    if bus_name_match:
        for line in bus_name_match.group(1).split('\n'):
            name_match = re.search(r"'([^']+)'", line.strip())
            if name_match:
                bus_names.append(name_match.group(1))
    
    return {
        'bus': bus_df,
        'gen': gen_df,
        'gencost': gencost_df,
        'branch': branch_df,
        'bus_name': bus_names,
        'baseMVA': base_mva
    }

