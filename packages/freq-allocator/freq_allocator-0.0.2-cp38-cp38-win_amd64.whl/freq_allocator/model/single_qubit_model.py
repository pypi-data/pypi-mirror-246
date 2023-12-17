from copy import deepcopy
import time
import warnings
import numpy as np
from scipy.interpolate import interp1d, interp2d, interpn
from .formula import f2phi, lorentzain

MUTHRESHOLD = 0.01

def singq_T1_err(a, tq, f, t1_spectrum):
    f_list = t1_spectrum['freq']
    t1_list = t1_spectrum['t1']
    func_interp = interp1d(f_list, t1_list, kind='linear')
    try:
        error = a * tq / func_interp(f)
    except:
        error = 5e-4
    if error < 0:
        error = 5e-4
    return error

def singq_T2_err(a, tq, f, t2_spectrum: dict = None, ac_spectrum_paras: list = None):
    if t2_spectrum:
        freq_list = t2_spectrum['freq']
        t2_list = t2_spectrum['t2']
        func_interp = interp1d(freq_list, t2_list, kind='linear')
        # return a * (1 - np.exp(-tq * func_interp(f)))
        return a * tq * func_interp(f)
    else:
        ac_spectrum_paras_sub = ac_spectrum_paras[:2] + ac_spectrum_paras[4:7]
        df_dphi = 1 / (
            abs(f2phi(f, *ac_spectrum_paras_sub) - f2phi(f - 0.01, *ac_spectrum_paras_sub)) / 0.01
        )
        error = a * tq * df_dphi
        if np.isnan(error):
            return 5e-4
        else:
            return error

def singq_xtalk_err(a, detune, mu, fxy):
    try:
        error = a * fxy(detune, mu)
        return error[0]
    except:
        return 0

def singq_residual_err(a, gamma, fi, fj, alpha_i, alpha_j):
    return lorentzain(fi, fj, a, gamma) + lorentzain(fi + alpha_i, fj, a, gamma) + lorentzain(fi, fj + alpha_j, a, gamma)

def single_err_model(frequencys, chip, targets, a):
    for target in targets:
        if frequencys.dtype == np.int32:
            chip.nodes[target]['frequency'] = chip.nodes[target]['allow freq'][frequencys[targets.index(target)]]
        else:
            chip.nodes[target]['frequency'] = chip.nodes[target]['allow freq'][int(round(frequencys[targets.index(target)] * (len(chip.nodes[target]['allow freq']) - 1)))]
    # for target in targets:
    #     chip.nodes[target]['frequency'] = int(round(freq_var_map(frequencys[targets.index(target)], chip.nodes[target]['allow freq'])))
        
    cost = 0
    for target in targets:
        cost += chip.nodes[target]['isolated_error'][frequencys[targets.index(target)]]
        # cost += chip.nodes[target]['isolated_error'](chip.nodes[target]['frequency'])
        for neighbor in chip.nodes():
            if chip.nodes[neighbor].get('frequency', False) and not(neighbor == target) and \
                chip.nodes[neighbor]['name'] in chip.nodes[target]['xy_crosstalk_coef'] and \
                chip.nodes[target]['xy_crosstalk_coef'][chip.nodes[neighbor]['name']] > MUTHRESHOLD:
                cost += singq_xtalk_err(a[2], chip.nodes[neighbor]['frequency'] - chip.nodes[target]['frequency'], 
                                        chip.nodes[target]['xy_crosstalk_coef'][chip.nodes[neighbor]['name']], chip.nodes[target]['xy_crosstalk_f'])
                if (target, neighbor) in chip.edges():
                    cost += singq_residual_err(a[3], a[4],                        
                                        chip.nodes[neighbor]['frequency'],
                                        chip.nodes[target]['frequency'],
                                        chip.nodes[neighbor]['anharm'],
                                        chip.nodes[target]['anharm'])       
                    for nNeighbor in chip[neighbor]:
                        if nNeighbor == target:
                            continue
                        elif chip.nodes[nNeighbor].get('frequency', False):
                            cost += singq_residual_err(a[6], a[7],
                                                chip.nodes[nNeighbor]['frequency'],
                                                chip.nodes[target]['frequency'],
                                                chip.nodes[nNeighbor]['anharm'],
                                                chip.nodes[target]['anharm']) / 2
    cost_average = cost / len(targets)
    return cost_average 

