from sko.PSO import PSO
import os
import geatpy as ea
import numpy as np
from copy import deepcopy
import random
from matplotlib import pyplot as plt
import matplotlib
from freq_allocator.dataloader.load_chip import gen_pos, max_Algsubgraph, xtalk_G
import networkx as nx
from freq_allocator.model.two_qubit_model import twoQ_err_model, twoq_T1_err, twoq_T2_err, twoq_xtalk_err, twoq_pulse_distort_err

def two_alloc(chip, a):
    originXtalkG = xtalk_G(chip)
    maxParallelCZs = max_Algsubgraph(chip)
    xtalkG = xtalk_G(chip)

    for level in range(len(maxParallelCZs)):
        couplerActivate = [[coupler, 'gray'] for coupler in chip.edges]
        for i in couplerActivate:
            if i[0] in maxParallelCZs[level]:
                i[1] = 'green'
        pos = gen_pos(chip)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=list(dict(couplerActivate).values()), edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.savefig('results\\' + 'twoq chip ' + str(level) + '.pdf', dpi=300)
        plt.close()

    for level in range(len(maxParallelCZs)):
        print('level', level)
        if len(maxParallelCZs[level]) == 0:
            continue
        epoch = 0
        xTalkSubG = deepcopy(xtalkG)
        xTalkSubG.remove_nodes_from(set(xtalkG.nodes).difference(set(maxParallelCZs[level])))

        centerConflictQCQ = list(xTalkSubG.nodes)[0]
        newreOptimizeQCQs = []
        avgErrEpoch = []
        jumpToEmpty = False
        hisReOptimizeQCQs = []
        hisXtalkG = []

        while len([xTalkSubG.nodes[qcq]['all err'] for qcq in xTalkSubG.nodes if xTalkSubG.nodes[qcq].get('all err', False)]) < len(xTalkSubG.nodes) or \
            (len([xTalkSubG.nodes[qcq]['all err'] for qcq in xTalkSubG.nodes if xTalkSubG.nodes[qcq].get('all err', False)]) == len(xTalkSubG.nodes) and not(jumpToEmpty)):
            reOptimizeQCQs = [centerConflictQCQ]
            for qcq in xTalkSubG.nodes():
                if centerConflictQCQ in newreOptimizeQCQs and not(qcq in reOptimizeQCQs) and \
                    qcq in newreOptimizeQCQs:
                    reOptimizeQCQs.append(qcq)
                elif not(xTalkSubG.nodes[centerConflictQCQ].get('frequency', False)) and not(qcq in reOptimizeQCQs) and \
                    not(xTalkSubG.nodes[qcq].get('frequency', False)) and \
                    nx.has_path(xTalkSubG, qcq, centerConflictQCQ) and nx.shortest_path_length(xTalkSubG, qcq, centerConflictQCQ) == 1:
                    reOptimizeQCQs.append(qcq)
            print('optimize gates: ', reOptimizeQCQs)

            reOptimizeQCQs = tuple(reOptimizeQCQs)
            bounds = []
            for qcq in reOptimizeQCQs:
                if chip.nodes[qcq[0]]['ac_spectrum'][0] > chip.nodes[qcq[1]]['ac_spectrum'][0]:
                    qh, ql = qcq[0], qcq[1]
                else:
                    qh, ql = qcq[1], qcq[0]
                bound = (3500, min(chip.nodes[ql]['ac_spectrum'][0], chip.nodes[qh]['ac_spectrum'][0] + chip.nodes[qh]['anharm']))
                bounds.append(bound)

            @ea.Problem.single
            def err_model_fun(frequencys):
                return twoQ_err_model(frequencys, chip, xTalkSubG, reOptimizeQCQs, a)

            problem = ea.Problem(
                name='two q err model',
                M=1,  # 初始化M（目标维数）
                maxormins=[1],  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
                Dim=len(reOptimizeQCQs),  # 决策变量维数
                varTypes=[0] * len(reOptimizeQCQs),  # 决策变量的类型列表，0：实数；1：整数
                lb=[b[0] for b in bounds],  # 决策变量下界
                ub=[b[1] for b in bounds],  # 决策变量上界
                evalVars=err_model_fun
            )

            algorithm = ea.soea_DE_best_1_bin_templet(
                problem,
                ea.Population(Encoding='RI', NIND=40),
                MAXGEN=40,
                logTras=1,
                # trappedValue=1e-10,
                # maxTrappedCount=20
            )
            algorithm.mutOper.F = 1
            algorithm.recOper.XOVR = 1

            # algorithm.run()

            freq_bset = None
            res = ea.optimize(
                algorithm,
                prophet=freq_bset,
                seed=np.random.randint(10),
                # prophet=np.array(self.experiment_options.FIR0),
                verbose=True, drawing=0, outputMsg=True,
                drawLog=False, saveFlag=True, dirName='results\\'
            )
            freq_bset = res['Vars'][0]

            for qcq in reOptimizeQCQs:
                xTalkSubG.nodes[qcq]['frequency'] = freq_bset[reOptimizeQCQs.index(qcq)]

            newreOptimizeQCQs, conflictGatePairs, conflictSpectator = twoQ_checkcoli(chip, xTalkSubG, a)
            hisXtalkG.append(xTalkSubG)
            hisReOptimizeQCQs.append(set(newreOptimizeQCQs))
            ocqc = [len(h) for h in hisReOptimizeQCQs]

            if len(hisReOptimizeQCQs) > 10 or min(ocqc) == 0:
                on = [len(h) for h in hisReOptimizeQCQs]
                xTalkSubG = hisXtalkG[on.index(min(on))]
                print('jump', on, on.index(min(on)), 'is the xtalk subGraph with smallest conflict qubits.')  
                jumpToEmpty = True
            else:
                print('no jump')
                jumpToEmpty = False      

            avgErrEpoch.append(sum([xTalkSubG.nodes[qcq]['all err'] for qcq in xTalkSubG.nodes if xTalkSubG.nodes[qcq].get('all err', False)]) / 
                                len([xTalkSubG.nodes[qcq]['all err'] for qcq in xTalkSubG.nodes if xTalkSubG.nodes[qcq].get('all err', False)]))
            print('avg err estimate', avgErrEpoch)
            if len([xTalkSubG.nodes[qcq]['all err'] for qcq in xTalkSubG.nodes if xTalkSubG.nodes[qcq].get('all err', False)]) == len(xTalkSubG.nodes):
                for qcq in chip.edges:
                    if qcq in xTalkSubG.nodes:
                        xtalkG.nodes[qcq]['frequency'] = xTalkSubG.nodes[qcq]['frequency']
                        xtalkG.nodes[qcq]['spectator err'] = xTalkSubG.nodes[qcq]['spectator err']
                        xtalkG.nodes[qcq]['parallel err'] = xTalkSubG.nodes[qcq]['parallel err']
                        xtalkG.nodes[qcq]['T err'] = xTalkSubG.nodes[qcq]['T err']
                        xtalkG.nodes[qcq]['distort err'] = xTalkSubG.nodes[qcq]['distort err']
                        xtalkG.nodes[qcq]['all err'] = xTalkSubG.nodes[qcq]['all err']
                        conflictGatePairFinal = conflictGatePairs
                        conflictSpectatorFinal = conflictSpectator

            pos = gen_pos(chip)
            labelDict = dict([(i, i) for i in chip.nodes])
            errList = []
            for i in chip.edges:
                if i in xTalkSubG.nodes:
                    errList.append(np.log10(xTalkSubG.nodes[i].get('all err', 1e-5)))
                else:
                    errList.append(np.log10(1e-5))
            errLow = min(errList)
            errHigh = max(errList)
            plt.figure(figsize=(8, 8))
            nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
            nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
            nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
            plt.axis('off')
            plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
            plt.savefig('results\\' + str(epoch) + 'chip CZ err.pdf', dpi=300)
            plt.close()
            
            reOptimizeQCQsDict = dict([(qcq, nx.shortest_path_length(originXtalkG, qcq, centerConflictQCQ)) for qcq in newreOptimizeQCQs])
            emptyQCQDict = dict([(qcq, nx.shortest_path_length(originXtalkG, qcq, centerConflictQCQ)) for qcq in xTalkSubG 
                                 if not(xTalkSubG.nodes[qcq].get('frequency', False))])

            if len(reOptimizeQCQsDict) > 0 and not(jumpToEmpty):
                print('reoptimize qcq distance', reOptimizeQCQsDict)
                centerConflictQCQ = random.choices(list(reOptimizeQCQsDict.keys()), weights=[1 / max(0.5, distance) for distance in reOptimizeQCQsDict.values()], k=1)[0]
            elif len(emptyQCQDict) > 0:
                hisReOptimizeQCQs = []
                hisXtalkG = []
                jumpToEmpty = False
                print('empty qcq distance', emptyQCQDict)
                centerConflictQCQ = list(sorted(emptyQCQDict.items(), key=lambda x : x[1]))[0][0]
            epoch += 1

        print('ave', avgErrEpoch)
        plt.plot(avgErrEpoch, label='err epoch')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig('results\\' + 'CZ err.pdf', dpi=300)
        plt.close()

        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        freqList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                freqList.append(round(xtalkG.nodes[qcq]['frequency']))
            else:
                freqList.append(3000)
        freqLow = min(freqList)
        freqHigh = max(freqList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=freqList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=freqLow, vmax=freqHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz freq.pdf', dpi=300)
        plt.close()
        
        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        errList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                errList.append(xtalkG.nodes[qcq]['spectator err'])
            else:
                errList.append(1e-5)
        errList = np.log10(errList)
        errLow = min(errList)
        errHigh = max(errList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz spectator err.pdf', dpi=300)
        plt.close()

        
        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        errList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                errList.append(xtalkG.nodes[qcq]['parallel err'])
            else:
                errList.append(1e-5)
        errList = np.log10(errList)
        errLow = min(errList)
        errHigh = max(errList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz parallel err.pdf', dpi=300)
        plt.close()

        
        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        errList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                errList.append(xtalkG.nodes[qcq]['T err'])
            else:
                errList.append(1e-5)
        errList = np.log10(errList)
        errLow = min(errList)
        errHigh = max(errList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz t1 t2 err.pdf', dpi=300)
        plt.close()

        
        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        errList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                errList.append(xtalkG.nodes[qcq]['distort err'])
            else:
                errList.append(1e-5)
        errList = np.log10(errList)
        errLow = min(errList)
        errHigh = max(errList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz dist err.pdf', dpi=300)
        plt.close()
        
        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])

        errList = []
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                errList.append(xtalkG.nodes[qcq]['all err'])
            else:
                errList.append(1e-5)
        errList = np.log10(errList)
        errLow = min(errList)
        errHigh = max(errList)

        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        plt.savefig('results\\' + str(level) + 'best' + 'cz all err.pdf', dpi=300)
        plt.close()

    labelList = list(xtalkG.nodes)
    errList = [xtalkG.nodes[qcq]['spectator err'] for qcq in labelList]
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'cz spectator err scatter.pdf', dpi=300)
    plt.close()

    labelList = list(xtalkG.nodes)
    errList = [xtalkG.nodes[qcq]['parallel err'] for qcq in labelList]
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'cz parallel err scatter.pdf', dpi=300)
    plt.close()

    labelList = list(xtalkG.nodes)
    errList = [xtalkG.nodes[qcq]['T err'] for qcq in labelList]
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'cz decoherence err scatter.pdf', dpi=300)
    plt.close()

    labelList = list(xtalkG.nodes)
    errList = [xtalkG.nodes[qcq]['distort err'] for qcq in labelList]
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'cz dist err scatter.pdf', dpi=300)
    plt.close()

    labelList = list(xtalkG.nodes)
    errList = [xtalkG.nodes[qcq]['all err'] for qcq in labelList]
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'cz all err scatter.pdf', dpi=300)
    plt.close()

    with open('results\\cz err.txt', 'w') as fp:
        for qubit in xtalkG.nodes:
            fp.write(str(qubit) + ' frequency: ' + str(round(xtalkG.nodes[qcq]['frequency'])) +
                     ', spectator error: ' + str(round(xtalkG.nodes[qcq]['spectator err'], 7)) +
                     ', parallel error: ' + str(round(xtalkG.nodes[qcq]['parallel err'], 7)) +
                     ', T error: ' + str(round(xtalkG.nodes[qcq]['T err'], 7)) +
                     ', distort error: ' + str(round(xtalkG.nodes[qcq]['distort err'], 7)) +
                     ', all error: ' + str(round(xtalkG.nodes[qcq]['all err'], 7)) +
                      + '\n')
    with open('results\\conflict spectator dict.txt', 'w') as fp:
        for qcq in conflictSpectatorFinal:
            fp.write(str(qcq) + ': ')
            for neighbor in conflictSpectatorFinal[qcq]:
                fp.write(str(neighbor) + ' ')
            fp.write('\n')

    with open('results\\conflict gate pair.txt', 'w') as fp:
        for pair in conflictGatePairFinal:
            fp.write(str(pair) + '\n')

    return xtalkG

def twoQ_checkcoli(chip, xtalkG, a):
    reOptimizeQCQs = []
    conflictSpectator = dict()
    conflictGatePairs = []
    for qcq in xtalkG.nodes:
        if xtalkG.nodes[qcq].get('frequency', False):
            if sum(qcq[0]) % 2:
                T1Err1 = twoq_T1_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency'],
                                    a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[0]]['T1 spectra'])
                T1Err2 = twoq_T1_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency'],
                                    a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[1]]['T1 spectra'])
                T2Err1 = twoq_T2_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency'],
                                    a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[0]]['ac_spectrum'])
                T2Err2 = twoq_T2_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency'],
                                    a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[1]]['ac_spectrum'])
                twoqDistErr = twoq_pulse_distort_err([xtalkG.nodes[qcq]['frequency'] + chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency']], 
                                           [xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency']], 
                                           a[2])
            else:
                T1Err1 = twoq_T1_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency'], 
                                    a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[0]]['T1 spectra'])
                T1Err2 = twoq_T1_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency'], 
                                    a[0], xtalkG.nodes[qcq]['two tq'], chip.nodes[qcq[1]]['T1 spectra'])
                T2Err1 = twoq_T2_err(xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'], chip.nodes[qcq[0]]['frequency'], 
                                    a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[0]]['ac_spectrum'])
                T2Err2 = twoq_T2_err(xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[1]]['frequency'], 
                                    a[1], xtalkG.nodes[qcq]['two tq'], ac_spectrum_paras=chip.nodes[qcq[1]]['ac_spectrum'])
                twoqDistErr = twoq_pulse_distort_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[qcq[0]]['frequency']], 
                                            [xtalkG.nodes[qcq]['frequency'] + chip.nodes[qcq[1]]['anharm'], chip.nodes[qcq[1]]['frequency']], 
                                            a[2])
                
            twoqSpectatorErr = 0
            
            for q in qcq:
                if sum(q) % 2:
                    fWork = xtalkG.nodes[qcq]['frequency']
                else:
                    fWork = xtalkG.nodes[qcq]['frequency'] - chip.nodes[q]['anharm']
                for neighbor in chip.nodes():
                    if neighbor in qcq:
                        continue  
                    if neighbor in chip[q]:
                        twoqSpectatorErr1 = twoq_xtalk_err([fWork, chip.nodes[q]['frequency']], [chip.nodes[neighbor]['frequency'], chip.nodes[neighbor]['frequency']], 
                                            a[4], a[5], xtalkG.nodes[qcq]['two tq'])
                        twoqSpectatorErr2 = twoq_xtalk_err([fWork, chip.nodes[q]['frequency']], [chip.nodes[neighbor]['frequency'] + chip.nodes[neighbor]['anharm'], 
                                            chip.nodes[neighbor]['frequency'] + chip.nodes[neighbor]['anharm']], a[6], a[7], xtalkG.nodes[qcq]['two tq'])
                        twoqSpectatorErr += twoqSpectatorErr1 + twoqSpectatorErr2
                        if twoqSpectatorErr1 + twoqSpectatorErr2 > 1e-2:
                            if conflictSpectator.get(qcq, False):
                                conflictSpectator[qcq].append(neighbor)
                            else:
                                conflictSpectator[qcq] = [neighbor]

            for neighbor in xtalkG[qcq]:
                if xtalkG.nodes[neighbor].get('frequency', False):
                    for q0 in qcq:
                        for q1 in neighbor:
                            if (q0, q1) in chip.edges:
                                parallelErr = twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], \
                                                        [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], \
                                                        a[8], a[9], xtalkG.nodes[qcq]['two tq'])
                                if sum(q0) % 2:
                                    parallelErr += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'] + chip.nodes[q0]['anharm'], chip.nodes[q0]['frequency'] + chip.nodes[q0]['anharm']], 
                                                        [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                    parallelErr += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], 
                                                        [xtalkG.nodes[neighbor]['frequency'] - chip.nodes[q1]['anharm'], chip.nodes[q1]['frequency'] - chip.nodes[q1]['anharm']], 
                                                        a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                else:
                                    parallelErr += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'] - chip.nodes[q0]['anharm'], chip.nodes[q0]['frequency'] - chip.nodes[q0]['anharm']], 
                                                        [xtalkG.nodes[neighbor]['frequency'], chip.nodes[q1]['frequency']], a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                    parallelErr += twoq_xtalk_err([xtalkG.nodes[qcq]['frequency'], chip.nodes[q0]['frequency']], 
                                                        [xtalkG.nodes[neighbor]['frequency'] + chip.nodes[q1]['anharm'], chip.nodes[q1]['frequency'] + chip.nodes[q1]['anharm']], 
                                                        a[10], a[11], xtalkG.nodes[qcq]['two tq'])
                                if parallelErr > 1e-2 and not((qcq, neighbor) in conflictGatePairs or (qcq, neighbor) in conflictGatePairs):
                                    conflictGatePairs.append((qcq, neighbor))

            allErr = twoqSpectatorErr + parallelErr + T1Err1 + T1Err2 + T2Err1 + T2Err2 + twoqDistErr
            xtalkG.nodes[qcq]['spectator err'] = twoqSpectatorErr
            xtalkG.nodes[qcq]['parallel err'] = parallelErr
            xtalkG.nodes[qcq]['T err'] = T1Err1 + T1Err2 + T2Err1 + T2Err2
            xtalkG.nodes[qcq]['distort err'] = twoqDistErr
            xtalkG.nodes[qcq]['all err'] = allErr
            if allErr > 2e-2 and not(qcq in reOptimizeQCQs):
                reOptimizeQCQs.append(qcq)
                print(qcq, xtalkG.nodes[qcq]['all err'], 'qcq err')
    print('check, large err', reOptimizeQCQs)
    return reOptimizeQCQs, conflictGatePairs, conflictSpectator
