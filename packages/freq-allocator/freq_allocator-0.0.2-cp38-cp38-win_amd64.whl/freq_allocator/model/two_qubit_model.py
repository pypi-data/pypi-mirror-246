
import numpy as np
from scipy.interpolate import interp1d, interpn
from scipy.special import erf

from .formula import lorentzain, f2phi

def twoq_T1_err(fWork, fidle, a, tq, t1_spectrum):
    step = 1000
    ft = twoq_pulse(fWork, fidle, tq, step)
    f_list = t1_spectrum['freq']
    t1_list = t1_spectrum['t1']
    func_interp = interp1d(f_list, t1_list, kind='linear')
    TtList = []
    for f in ft:
        try:
            error = a * tq / func_interp(f)
        except:
            error = 5e-4
        if error < 0:
            error = 5e-4
        TtList.append(error)
    return a * np.sum(TtList) * (tq / step)

def twoq_T2_err(fWork, fidle, a, tq, t2_spectrum: dict = None, ac_spectrum_paras: list = None):
    step = 1000
    ft = twoq_pulse(fWork, fidle, tq, step)
    TtList = []
    if t2_spectrum:
        freq_list = t2_spectrum['freq']
        t2_list = t2_spectrum['t2']
        func_interp = interp1d(freq_list, t2_list, kind='linear')
        for f in ft:
            TtList.append(func_interp(f))
    else:
        fq_max, Ec, d = (
            ac_spectrum_paras[0],
            ac_spectrum_paras[1],
            ac_spectrum_paras[-1],
        )
        for f in ft:
            df_dphi = 1 / (
                abs(f2phi(f, fq_max, Ec, d) - f2phi(f - 0.01, fq_max, Ec, d)) / 0.01
            )
            if np.isnan(df_dphi):
                TtList.append(5e-4)
            else:
                TtList.append(df_dphi)

    return a * np.sum(TtList) * (tq / step)

def twoq_xtalk_err(fi, fj, a, gamma, tq):
    step = 100
    fits = twoq_pulse(fi[0], fi[1], tq, step)
    fjts = twoq_pulse(fj[0], fj[1], tq, step)
    xtalkList = [lorentzain(fit, fjt, a, gamma) for (fit, fjt) in zip(fits, fjts)]
    return np.sum(xtalkList) * (tq / step)

def twoq_pulse_distort_err(fi, fj, a):
    return a * ((fi[0] - fi[1]) ** 2 + (fj[0] - fj[1]) ** 2)

def twoq_pulse(freqWork, freqMax, tq, step):
    if freqWork == freqMax:
        return [freqWork] * step
    else:
        pulseLen = tq
        tList = np.linspace(0, pulseLen, step)
        sigma = [1.5]
        flattop_start = 3 * sigma[0]
        flattop_end = pulseLen - 3 * sigma[0]
        freqList = (freqWork - freqMax) * 1 / 2 * (erf((tList - flattop_start) / (np.sqrt(2) * sigma[0])) - \
                                    erf((tList - flattop_end) / (np.sqrt(2) * sigma[0]))) + freqMax
        return freqList

def twoQ_err_model(frequencys, chip, xtalkG, reOptimizeQCQs, a):
    for qcq in reOptimizeQCQs:
        xtalkG.nodes[qcq]['frequency'] = frequencys[reOptimizeQCQs.index(qcq)]
    cost = 0
    for qcq in reOptimizeQCQs:
        if sum(qcq[0]) % 2:
            cost += twoq_T1_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency'], 
                                a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[0]]['T1 spectra'])
            cost += twoq_T1_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency'],
                                a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[1]]['T1 spectra'])
            cost += twoq_T2_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency'], 
                                a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[0]]['ac_spectrum'])
            cost += twoq_T2_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency'],
                                a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[1]]['ac_spectrum'])
            cost += twoq_pulse_distort_err([xtalkG.nodes[qcq]['frequency'] + chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency']], 
                                           [xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency']], 
                                           a[2])
        else:
            cost += twoq_T1_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency'], 
                                a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[0]]['T1 spectra'])
            cost += twoq_T1_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency'],
                                a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[1]]['T1 spectra'])
            cost += twoq_T2_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency'], 
                                a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[0]]['ac_spectrum'])
            cost += twoq_T2_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency'],
                                a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[1]]['ac_spectrum'])
            cost += twoq_pulse_distort_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency']], 
                                            [xtalkG.nodes[qcq]['frequency'] + chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency']], 
                                            a[2])

        for q in qcq:
            if sum(q) % 2:
                fWork = xtalkG.nodes[qcq]['frequency']
            else:
                fWork = xtalkG.nodes[qcq]['frequency'] - chip.nodes[q]['anharm']
            for neighbor in chip.nodes():
                if neighbor in qcq:
                    continue
                if neighbor in chip[q]:
                    cost += twoq_xtalk_err([fWork, chip.nodes[q]['frequency']], [chip.nodes[neighbor]['frequency'], chip.nodes[neighbor]['frequency']], 
                                        a[4], a[5], xtalkG.nodes[qcq]['two tq'])
                    cost += twoq_xtalk_err([fWork, chip.nodes[q]['frequency']], [chip.nodes[neighbor]['frequency'] + chip.nodes[neighbor]['anharm'], 
                                        chip.nodes[neighbor]['frequency'] + chip.nodes[neighbor]['anharm']], a[6], a[7], xtalkG.nodes[qcq]['two tq'])
                    
        for neighbor in xtalkG[qcq]:
            if xtalkG.nodes[neighbor].get('frequency', False):
                for q0 in qcq:
                    for q1 in neighbor:
                        if (q0, q1) in chip.edges:
                            cost += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], 
                                                   [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], 
                                                   a[8], a[9], xtalkG.nodes[qcq]['two tq'])
                            if sum(q0) % 2:
                                cost += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'] + chip.nodes[q0]['anharm'], chip.nodes[q0]['frequency'] + chip.nodes[q0]['anharm']], 
                                                    [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                cost += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], 
                                                    [xtalkG.nodes[neighbor]['frequency'] - chip.nodes[q1]['anharm'], chip.nodes[q1]['frequency'] - chip.nodes[q1]['anharm']], 
                                                    a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                            else:
                                cost += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'] - chip.nodes[q0]['anharm'], chip.nodes[q0]['frequency'] - chip.nodes[q0]['anharm']], 
                                                    [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                cost += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], 
                                                    [xtalkG.nodes[neighbor]['frequency'] + chip.nodes[q1]['anharm'], chip.nodes[q1]['frequency'] + chip.nodes[q1]['anharm']], 
                                                    a[10], a[11], xtalkG.nodes[qcq]['two tq'])
    # print(frequencys, cost / len(reOptimizeQCQs))
    return cost / len(reOptimizeQCQs)
