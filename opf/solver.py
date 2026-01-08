import numpy as np
import pandas as pd
from pypower.api import runopf, ppoption
from .parser import parse_matpower_file

def load_matpower_case(m_file_path: str):
    mpc_data = parse_matpower_file(m_file_path)
    
    mpc = {}
    mpc['baseMVA'] = mpc_data['baseMVA']
    mpc['bus'] = mpc_data['bus'].values
    mpc['gen'] = mpc_data['gen'].values
    mpc['gencost'] = mpc_data['gencost'].values
    mpc['branch'] = mpc_data['branch'].values
    mpc['bus_name'] = mpc_data.get('bus_name', [])
    
    return mpc

def modify_load_mpc(mpc, bus_num, new_load_mw):
    bus_indices = np.where(mpc['bus'][:, 0] == bus_num)[0]
    if len(bus_indices) > 0:
        mpc['bus'][bus_indices[0], 2] = new_load_mw

def run_opf_matpower(mpc):
    opt = ppoption()
    opt['VERBOSE'] = 0
    opt['OUT_ALL'] = 0
    opt['OPF_ALG'] = 560
    opt['OPF_VIOLATION'] = 0.01
    opt['PDIPM_GRADTOL'] = 1e-2
    opt['PDIPM_COMPTOL'] = 1e-2
    opt['PDIPM_COSTTOL'] = 1e-2
    opt['PDIPM_FEASTOL'] = 1e-2
    opt['PDIPM_MAX_IT'] = 100
    opt['ENFORCE_Q_LIM'] = 1
    opt['ENFORCE_P_LIM'] = 1
    
    result = runopf(mpc, opt)
    
    if not result['success']:
        return None
    
    bus_results = result['bus']
    if bus_results.ndim == 1:
        bus_results = bus_results.reshape(1, -1)
    
    lmps = bus_results[:, 13] if bus_results.shape[1] > 13 else np.zeros(bus_results.shape[0])
    
    bus_names_list = mpc.get('bus_name', [])
    num_buses = len(bus_results)
    if len(bus_names_list) < num_buses:
        bus_names_list.extend([f"Bus {int(bus_results[i, 0])}" for i in range(len(bus_names_list), num_buses)])
    bus_names = bus_names_list[:num_buses]
    
    results = pd.DataFrame({
        'Bus_Number': [int(bus[0]) for bus in bus_results],
        'Bus_Name': bus_names,
        'LMP_$/MWh': lmps,
        'Voltage_pu': bus_results[:, 7],
        'Angle_deg': bus_results[:, 8] * 180 / np.pi,
        'P_MW': bus_results[:, 2],
        'Q_Mvar': bus_results[:, 3]
    })
    
    gen_results = result['gen']
    if gen_results.ndim == 1:
        gen_results = gen_results.reshape(1, -1)
    
    gen_dispatch = []
    for gen in gen_results:
        gen_dispatch.append({
            'Bus_Number': int(gen[0]),
            'Generator': f"Gen {int(gen[0])}",
            'P_MW': gen[1],
            'Q_Mvar': gen[2] if len(gen) > 2 else 0,
            'Cost_$/MWh': 0.0
        })
    
    gen_df = pd.DataFrame(gen_dispatch)
    
    return results, gen_df

