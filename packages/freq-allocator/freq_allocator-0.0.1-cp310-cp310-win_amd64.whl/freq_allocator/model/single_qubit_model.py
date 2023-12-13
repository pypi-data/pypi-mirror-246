
from copy import deepcopy
import time
import warnings
import numpy as np
from scipy.interpolate import interp1d, interp2d, interpn

from .formula import f2phi, lorentzain

MUTHRESHOLD = 0.01


def singq_T1_err(a, tq, f, t1_spectrum):
    '''Compute T1 error of a single qubit

    Args:
        a (float): hyperparameter
        tq (float): gate time
        f (float): allocate frequency
        t1_spectrum (list): T1 spectrum

    Returns:
        float: error
    '''

    f_list = t1_spectrum['freq']
    t1_list = t1_spectrum['t1']
    func_interp = interp1d(f_list, t1_list, kind='cubic')
    # return a * (1 - np.exp(-tq * func_interp(f)))
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
        func_interp = interp1d(freq_list, t2_list, kind='cubic')
        # return a * (1 - np.exp(-tq * func_interp(f)))
        return a * tq * func_interp(f)
    else:
        fq_max, Ec, d = (
            ac_spectrum_paras[0],
            ac_spectrum_paras[1],
            ac_spectrum_paras[-1],
        )
        df_dphi = 1 / (
            abs(f2phi(f, fq_max, Ec, d) - f2phi(f - 0.01, fq_max, Ec, d)) / 0.01
        )
        error = a * tq * df_dphi
        if np.isnan(error):
            return 5e-4
        else:
            return error

def singq_xtalk_err(a, anharm, detune, mu, xy_crosstalk_sim):
    alpha_list = xy_crosstalk_sim['alpha_list']
    mu_list = xy_crosstalk_sim['mu_list']
    detune_list = xy_crosstalk_sim['detune_list']
    error_arr = xy_crosstalk_sim['error_arr'][alpha_list.index(anharm)]

    try:
        error = a * interpn((mu_list, detune_list), error_arr, np.array([mu, detune]))
        # if error[0]<0:
        #     print(error[0])
        return error[0]
    except:
        return 0


def singq_zz_err(a, gamma, fi, fj):
    if lorentzain(fi, fj, a, gamma) < 0:
        print(lorentzain(fi, fj, a, gamma))
    return lorentzain(fi, fj, a, gamma)

def single_err_model(frequencys, inducedChip, targets, a, xy_crosstalk_sim):
    '''_summary_

    Args:
        frequencys (_type_): _description_
        inducedChip (_type_): _description_
        targets (_type_): _description_
        a (List[float]): Size 7, hyperparameter for the model
        xy_crosstalk_sim (_type_): _description_

    Returns:
        _type_: _description_
    '''
    # time_start = time.time()
    chip = deepcopy(inducedChip)
    # xy_input = []
    for target in targets:
        allow_freq = chip.nodes[target]['allow_freq']
        chip.nodes[target]['frequency'] = allow_freq[
            int(round(frequencys[targets.index(target)] * (len(allow_freq) - 1)))
        ]
        # xy_input.append((chip.nodes[target]['frequency'], chip.nodes[target]['anharm']))

    cost = 0
    for target in targets:
        if chip.nodes[target]['available']:
            if round(chip.nodes[target]['frequency']) not in chip.nodes[target]['allow_freq']:
                cost += 1
            T1_err = singq_T1_err(
                a[0],
                chip.nodes[target]['t_sq'],
                chip.nodes[target]['frequency'],
                chip.nodes[target]['t1_spectrum'],
            )
            if T1_err < 0:
                warnings.warn('有问题', category=None, stacklevel=1, source=None)
            cost += T1_err

            cost += singq_T2_err(
                a[1],
                chip.nodes[target]['t_sq'],
                chip.nodes[target]['frequency'],
                ac_spectrum_paras=chip.nodes[target]['ac_spectrum'],
            )
            for neighbor in chip.nodes():
                if (
                    chip.nodes[neighbor].get('frequency', False)
                    and not (neighbor == target)
                    and chip.nodes[neighbor]['xy_crosstalk_coef'][target] > MUTHRESHOLD
                ):  # 每次计算串扰误差的时候，计算所有已经分配的比特对target的串扰，而不是只计算分配区域内的
                    # if chip.nodes[neighbor]['xy_crosstalk_coef'][target] > MUTHRESHOLD and (
                    #     neighbor in targets
                    # ):
                    cost += singq_xtalk_err(
                        a[2],
                        chip.nodes[target]['anharm'],
                        chip.nodes[neighbor]['frequency'] - chip.nodes[target]['frequency'],
                        chip.nodes[target]['xy_crosstalk_coef'][neighbor],
                        xy_crosstalk_sim,
                    )
            # 遍历距离为1的比特，计算杂散耦合
            for neighbor in chip[target]:
                if chip.nodes[target]['available'] and chip.nodes[neighbor].get(
                    'frequency', False
                ):
                    cost += singq_zz_err(
                        a[3],
                        a[4],
                        chip.nodes[neighbor]['frequency'],
                        chip.nodes[target]['frequency'],
                    )
                # if (
                #     chip.nodes[target]['available']
                #     and chip.nodes[neighbor]['available']
                # ):
                #     cost += twoq_pulse_distort_err(
                #         chip.nodes[neighbor]['frequency'],
                #         chip.nodes[target]['frequency'],
                #         a[5],
                #     )
                for nNeighbor in chip[neighbor]:
                    if chip.nodes[target]['available']:
                        continue
                    if nNeighbor == target:
                        continue
                    elif chip.nodes[nNeighbor].get('frequency', False):
                        cost += singq_zz_err(
                            a[6],
                            a[7],
                            chip.nodes[nNeighbor]['frequency'],
                            chip.nodes[target]['frequency'],
                        )
    cost_average = cost / len(targets)
    #time_end = time.time()
    #print(
    #     f'running time: {time_start-time_end}, cost_average: {cost_average}, freq_list: {frequencys}'
    # )
    return cost_average



