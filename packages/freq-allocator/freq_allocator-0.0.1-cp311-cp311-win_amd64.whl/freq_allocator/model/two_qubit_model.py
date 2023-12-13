
import numpy as np
from scipy.interpolate import interp1d, interpn
from scipy.special import erf

from .formula import lorentzain
from .single_qubit_model import MUTHRESHOLD

def twoq_T1_err(fWork, fidle, fMax, a, tq, T1Spectra):
    step = 1000
    ft = twoq_pulse(fWork, fidle, tq, step)
    fList = np.linspace(3.75, fMax, step)
    func_interp = interp1d(fList, T1Spectra, kind='cubic')
    TtList = func_interp(ft)
    return a * (1 - np.exp(-np.sum(TtList) * (tq / step)))
    # return a * np.sum(TtList) * (tq / step)


def twoq_T2_err(fWork, fidle, fMax, a, tq, df_dphiList):
    step = 1000
    ft = twoq_pulse(fWork, fidle, tq, step)
    fList = np.linspace(3.75, fMax, step)
    func_interp = interp1d(fList, df_dphiList, kind='cubic')
    TtList = func_interp(ft)
    return a * (1 - np.exp(-np.sum(TtList) * (tq / step)))
    # return a * np.sum(TtList) * (tq / step)


def twoq_xy_err(anharm, fq, fn, mu, fxy, a, twotq):
    anharms, detunes, mus = fxy[0], fxy[1], fxy[2]
    step = 100
    fqts = twoq_pulse(fq[0], fq[1], twotq, step)
    xtalkList = []
    for fqt in fqts:
        xtalkList.append(
            interpn((anharms, detunes, mus), fxy[3], np.array([anharm, fqt - fn, mu]))
        )
    return a * np.sum(xtalkList) * (twotq / step)


def twoq_xtalk_err(fi, fj, a, gamma, tq):
    step = 100
    fits = twoq_pulse(fi[0], fi[1], tq, step)
    fjts = twoq_pulse(fj[0], fj[1], tq, step)
    xtalkList = [lorentzain(fit, fjt, a, gamma) for (fit, fjt) in zip(fits, fjts)]
    return np.sum(xtalkList) * (tq / step)


def twoq_pulse_distort_err(fi, fj, a):
    return a * (fi - fj) ** 2


def twoq_pulse(freqWork, freqMax, tq, step):
    if freqWork == freqMax:
        return [freqWork] * step
    else:
        pulseLen = tq
        tList = np.linspace(0, pulseLen, step)
        sigma = [1.5]
        flattop_start = 3 * sigma[0]
        flattop_end = pulseLen - 3 * sigma[0]
        freqList = (freqWork - freqMax) * 1 / 2 * (
            erf((tList - flattop_start) / (np.sqrt(2) * sigma[0]))
            - erf((tList - flattop_end) / (np.sqrt(2) * sigma[0]))
        ) + freqMax
        return freqList


def twoQ_err_model(frequencys, chip, xtalkG, reOptimizeQCQs, a, parallelXY=[]):
    for qcq in reOptimizeQCQs:
        xtalkG.nodes[qcq]['frequency'] = frequencys[reOptimizeQCQs.index(qcq)]
    cost = 0
    for qcq in reOptimizeQCQs:
        if sum(qcq[0]) % 2:
            cost += twoq_T1_err(
                xtalkG.nodes[qcq]['frequency'],
                chip.nodes[qcq[0]]['frequency'],
                chip.nodes[qcq[0]]['sweet point'],
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[0]]['t1_spectrum'],
            )
            cost += twoq_T1_err(
                xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'],
                chip.nodes[qcq[1]]['frequency'],
                chip.nodes[qcq[1]]['sweet point'],
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[1]]['t1_spectrum'],
            )
            cost += twoq_T2_err(
                xtalkG.nodes[qcq]['frequency'],
                chip.nodes[qcq[0]]['frequency'],
                chip.nodes[qcq[0]]['sweet point'],
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[0]]['df/dphi'],
            )
            cost += twoq_T2_err(
                xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'],
                chip.nodes[qcq[1]]['frequency'],
                chip.nodes[qcq[1]]['sweet point'],
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[1]]['df/dphi'],
            )
        else:
            cost += twoq_T1_err(
                xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'],
                chip.nodes[qcq[0]]['frequency'],
                chip.nodes[qcq[0]]['sweet point'],
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[0]]['t1_spectrum'],
            )
            cost += twoq_T1_err(
                xtalkG.nodes[qcq]['frequency'],
                chip.nodes[qcq[1]]['frequency'],
                chip.nodes[qcq[1]]['sweet point'],
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[1]]['t1_spectrum'],
            )
            cost += twoq_T2_err(
                xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'],
                chip.nodes[qcq[0]]['frequency'],
                chip.nodes[qcq[0]]['sweet point'],
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[0]]['df/dphi'],
            )
            cost += twoq_T2_err(
                xtalkG.nodes[qcq]['frequency'],
                chip.nodes[qcq[1]]['frequency'],
                chip.nodes[qcq[1]]['sweet point'],
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qcq[1]]['df/dphi'],
            )
        for q in qcq:
            if sum(q) % 2:
                fWork = xtalkG.nodes[qcq]['frequency']
            else:
                fWork = xtalkG.nodes[qcq]['frequency'] - chip.nodes[q]['anharm']
            for neighbor in chip.nodes():
                if neighbor in qcq:
                    continue
                if (
                    chip.nodes[neighbor]['xy_crosstalk_coef'][q] > MUTHRESHOLD
                    and neighbor in parallelXY
                ):
                    cost += twoq_xy_err(
                        chip.nodes[q]['anharm'],
                        [fWork, chip.nodes[q]['frequency']],
                        chip.nodes[neighbor]['frequency'],
                        chip.nodes[neighbor]['xy_crosstalk_coef'][q],
                        chip.nodes[q]['xy xtalk'],
                        a[2],
                        xtalkG.nodes[qcq]['two tq'],
                    )
                if neighbor in chip[q]:
                    cost += twoq_xtalk_err(
                        [fWork, chip.nodes[q]['frequency']],
                        [
                            chip.nodes[neighbor]['frequency'],
                            chip.nodes[neighbor]['frequency'],
                        ],
                        a[3],
                        a[4],
                        xtalkG.nodes[qcq]['two tq'],
                    )
                    cost += twoq_xtalk_err(
                        [fWork, chip.nodes[q]['frequency']],
                        [
                            chip.nodes[neighbor]['frequency']
                            + chip.nodes[neighbor]['anharm'],
                            chip.nodes[neighbor]['frequency']
                            + chip.nodes[neighbor]['anharm'],
                        ],
                        a[5],
                        a[6],
                        xtalkG.nodes[qcq]['two tq'],
                    )

        for neighbor in xtalkG[qcq]:
            if xtalkG.nodes[neighbor].get('frequency', False):
                for q0 in qcq:
                    for q1 in neighbor:
                        if (q0, q1) in chip.edges:
                            cost += twoq_xtalk_err(
                                [
                                    xtalkG.nodes[qcq]['frequency'],
                                    chip.nodes[q0]['frequency'],
                                ],
                                [
                                    xtalkG.nodes[neighbor]['frequency'],
                                    chip.nodes[q1]['frequency'],
                                ],
                                a[7],
                                a[8],
                                xtalkG.nodes[qcq]['two tq'],
                            )
                            if sum(q0) % 2:
                                cost += twoq_xtalk_err(
                                    [
                                        xtalkG.nodes[qcq]['frequency']
                                        + chip.nodes[q0]['anharm'],
                                        chip.nodes[q0]['frequency']
                                        + chip.nodes[q0]['anharm'],
                                    ],
                                    [
                                        xtalkG.nodes[neighbor]['frequency'],
                                        chip.nodes[q1]['frequency'],
                                    ],
                                    a[9],
                                    a[10],
                                    xtalkG.nodes[qcq]['two tq'],
                                )
                                cost += twoq_xtalk_err(
                                    [
                                        xtalkG.nodes[qcq]['frequency'],
                                        chip.nodes[q0]['frequency'],
                                    ],
                                    [
                                        xtalkG.nodes[neighbor]['frequency']
                                        - chip.nodes[q1]['anharm'],
                                        chip.nodes[q1]['frequency']
                                        - chip.nodes[q1]['anharm'],
                                    ],
                                    a[9],
                                    a[10],
                                    xtalkG.nodes[qcq]['two tq'],
                                )
                            else:
                                cost += twoq_xtalk_err(
                                    [
                                        xtalkG.nodes[qcq]['frequency']
                                        - chip.nodes[q0]['anharm'],
                                        chip.nodes[q0]['frequency']
                                        - chip.nodes[q0]['anharm'],
                                    ],
                                    [
                                        xtalkG.nodes[neighbor]['frequency'],
                                        chip.nodes[q1]['frequency'],
                                    ],
                                    a[9],
                                    a[10],
                                    xtalkG.nodes[qcq]['two tq'],
                                )
                                cost += twoq_xtalk_err(
                                    [
                                        xtalkG.nodes[qcq]['frequency'],
                                        chip.nodes[q0]['frequency'],
                                    ],
                                    [
                                        xtalkG.nodes[neighbor]['frequency']
                                        + chip.nodes[q1]['anharm'],
                                        chip.nodes[q1]['frequency']
                                        + chip.nodes[q1]['anharm'],
                                    ],
                                    a[9],
                                    a[10],
                                    xtalkG.nodes[qcq]['two tq'],
                                )
    return cost

