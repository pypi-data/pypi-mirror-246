from copy import deepcopy
import os
import pickle
import time
import warnings
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from freq_allocator.dataloader import load_chip_data_from_file, gen_pos # , max_Algsubgraph, xtalk_G, gen_pos
import networkx as nx
from scipy.interpolate import interp1d, interp2d, interpn
from freq_allocator.model.single_qubit_model import single_err_model, singq_T1_err, singq_T2_err, singq_xtalk_err, singq_zz_err
from sko.PSO import PSO
import random

def checkcoli(chip, a, xy_sim):
    reOptimizeNodes = []
    for qubit in chip.nodes():
        if chip.nodes[qubit].get('frequency', False):
            t1Cost = singq_T1_err(a[0], chip.nodes[qubit]['sing tq'], chip.nodes[qubit]['frequency'], chip.nodes[qubit]['T1 spectra'])
            t2Cost = singq_T2_err(a[1], chip.nodes[qubit]['sing tq'], chip.nodes[qubit]['frequency'], ac_spectrum_paras=chip.nodes[qubit]['ac_spectrum'])
            xyCost = 0
            zzCost = 0
            for neighbor in chip.nodes():
                if chip.nodes[neighbor].get('frequency', False) and not(neighbor == qubit):
                    if chip.nodes[neighbor]['name'] in chip.nodes[qubit]['xy_crosstalk_coef']:
                        xyCost += singq_xtalk_err(a[2], chip.nodes[qubit]['anharm'], chip.nodes[neighbor]['frequency'] - chip.nodes[qubit]['frequency'], 
                                                chip.nodes[qubit]['xy_crosstalk_coef'][chip.nodes[neighbor]['name']], xy_sim)
                    if (qubit, neighbor) in chip.edges():
                        zzCost += singq_zz_err(a[3], a[4],                         
                                                chip.nodes[neighbor]['frequency'],
                                                chip.nodes[qubit]['frequency'],
                                                chip.nodes[neighbor]['anharm'],
                                                chip.nodes[qubit]['anharm'])
                        
                        for nNeighbor in chip[neighbor]:
                            if nNeighbor == qubit:
                                continue
                            elif chip.nodes[nNeighbor].get('frequency', False):
                                zzCost += singq_zz_err(a[6], a[7], 
                                                    chip.nodes[nNeighbor]['frequency'],
                                                    chip.nodes[qubit]['frequency'],
                                                    chip.nodes[nNeighbor]['anharm'],
                                                    chip.nodes[qubit]['anharm'])
                                
            allCost = t1Cost + t2Cost + xyCost + zzCost
            if allCost > 1e-2 and not(qubit in reOptimizeNodes):
                reOptimizeNodes.append(qubit)
                print(qubit, allCost, 'single qubit cost')
            chip.nodes[qubit]['xy err'] = xyCost
            chip.nodes[qubit]['zz err'] = zzCost
            chip.nodes[qubit]['t1 err'] = t1Cost
            chip.nodes[qubit]['t2 err'] = t2Cost
            chip.nodes[qubit]['all err'] = allCost
    print('check, large err', reOptimizeNodes)
    return reOptimizeNodes

def sigq_alloc(chip : nx.Graph, H, W, a, xy_crosstalk_sim, s: int = 1, optimizer = 'PSO'):
    epoch = 0
    # centerConflictNode = (6, 4)
    centerConflictNode = (5, 3)
    avgErrEpoch = []
    smallestAvgErr = np.inf
    newreOptimizeNodes = []
    hisReOptimizeNodes = []

    while len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) < len(chip.nodes):
        
        reOptimizeNodes = [centerConflictNode]
        for qubit in chip.nodes():
            if centerConflictNode in newreOptimizeNodes and not(qubit in reOptimizeNodes) and \
                qubit in newreOptimizeNodes:
                reOptimizeNodes.append(qubit)
            elif not(chip.nodes[centerConflictNode].get('frequency', False)) and not(qubit in reOptimizeNodes) and \
                not(chip.nodes[qubit].get('frequency', False)) and \
                np.abs(qubit[0] - centerConflictNode[0]) + np.abs(qubit[1] - centerConflictNode[1]) <= s:
                reOptimizeNodes.append(qubit)
        print('optimize qubits: ', reOptimizeNodes)
            
        hisReOptimizeNodes.append(set(reOptimizeNodes))

        bounds = []
        for qubit in reOptimizeNodes:
            bounds.append((0, 1))

        func = lambda x : single_err_model(x, chip, reOptimizeNodes, a, xy_crosstalk_sim)

        pso = PSO(func=func, dim=len(bounds), pop=60, max_iter=200, lb=[b[0] for b in bounds], ub=[b[1] for b in bounds])
        # pso = PSO(func=func, dim=len(bounds), pop=20, max_iter=50, lb=[b[0] for b in bounds], ub=[b[1] for b in bounds])
        pso.run()

        for qubit in reOptimizeNodes:
            chip.nodes[qubit]['frequency'] = (pso.gbest_x[reOptimizeNodes.index(qubit)], chip.nodes[qubit]['allow freq'])
            print(qubit, 'diff', chip.nodes[qubit]['allow freq'][-1][-1] - chip.nodes[qubit]['frequency'])

        newreOptimizeNodes = checkcoli(chip, a, xy_crosstalk_sim)

        if set(newreOptimizeNodes) in hisReOptimizeNodes:
            print('jump', newreOptimizeNodes, 'in history optimize node')
            jumpToEmpty = True
        else:
            print('no jump', newreOptimizeNodes, 'not in history optimize node')
            jumpToEmpty = False

        avgErrEpoch.append(sum([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) / 
                           len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]))
        print('avg err estimate', avgErrEpoch)
        if len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) == len(chip.nodes) and \
            avgErrEpoch[-1] < smallestAvgErr:
            smallestAvgErr = avgErrEpoch[-1]
            bestFreq = [chip.nodes[qubit]['frequency'] for qubit in chip.nodes]
            bestT1Err = [chip.nodes[qubit]['t1 err'] for qubit in chip.nodes]
            bestT2Err = [chip.nodes[qubit]['t2 err'] for qubit in chip.nodes]
            bestXyErr = [chip.nodes[qubit]['xy err'] for qubit in chip.nodes]
            bestZzErr = [chip.nodes[qubit]['zz err'] for qubit in chip.nodes]
            bestAllErr = [chip.nodes[qubit]['all err'] for qubit in chip.nodes]

        drawChip = deepcopy(chip)

        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in drawChip.nodes])
        errList = [np.log10(chip.nodes[i].get('all err', 1e-5)) for i in chip.nodes]
        errLow = min(errList)
        errHigh = max(errList)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
        plt.savefig(str(epoch) + 'chip err.pdf', dpi=300)
        plt.close()

        reOptimizeNodeDict = dict([(qubit, nx.shortest_path_length(chip, qubit, centerConflictNode)) for qubit in newreOptimizeNodes])
        emptyNodeDict = dict([(qubit, nx.shortest_path_length(chip, qubit, centerConflictNode)) for qubit in chip.nodes() if not(chip.nodes[qubit].get('frequency', False))])

        if len(reOptimizeNodeDict) > 0 and not(jumpToEmpty):
            print('reoptimize qubit and distance', reOptimizeNodeDict)
            centerConflictNode = random.choices(list(reOptimizeNodeDict.keys()), weights=[1 / max(0.5, distance) for distance in reOptimizeNodeDict.values()], k=1)[0]
        elif len(emptyNodeDict) > 0:
            print('empty qubit distance', emptyNodeDict)
            centerConflictNode = list(sorted(emptyNodeDict.items(), key=lambda x : x[1]))[0][0]
        epoch += 1

    print('ave', avgErrEpoch)
    plt.plot(avgErrEpoch, label='err epoch')
    plt.xlabel('epoch')
    plt.legend()
    plt.savefig('err.pdf', dpi=300)
    plt.close()

    for qubit in chip.nodes:
        chip.nodes[qubit]['frequency'] = bestFreq[list(chip.nodes).index(qubit)]

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in drawChip.nodes])
    errList = np.log10(bestT1Err)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('best' + 'chip t1 err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in drawChip.nodes])
    errList = np.log10(bestT2Err)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('best' + 'chip t2 err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in drawChip.nodes])
    errList = np.log10(bestXyErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('best' + 'chip xy err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in drawChip.nodes])
    errList = np.log10(bestZzErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('best' + 'chip zz err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in drawChip.nodes])
    errList = np.log10(bestAllErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('best' + 'chip all err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    freqList = [int(round(chip.nodes[qubit]['frequency'], 3)) for qubit in chip.nodes]
    qlow = min(freqList)
    qhigh = max(freqList)
    freqDict = dict([(i, int(round(chip.nodes[i]['frequency'], 3))) for i in chip.nodes])
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, freqDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=freqList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=qlow, vmax=qhigh), cmap='coolwarm'))
    plt.savefig('chip freq.pdf', dpi=300)
    plt.close()

    errList = bestXyErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('xy err scatter.pdf', dpi=300)
    plt.close()

    errList = bestZzErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('zz err scatter.pdf', dpi=300)
    plt.close()

    errList = bestAllErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('all err scatter.pdf', dpi=300)
    plt.close()

    errList = bestT1Err
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('t1 err scatter.pdf', dpi=300)
    plt.close()

    errList = bestT2Err
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('t2 err scatter.pdf', dpi=300)
    plt.close()

    with open('chip data.txt', 'w') as fp:
        for qubit in chip.nodes:
            fp.write('qubit frequency: ', str(round(bestFreq[list(chip.nodes).index(qubit)])),
                     ', t1 error: ', str(round(bestT1Err[list(chip.nodes).index(qubit)], 7)), 
                     ', t2 error: ', str(round(bestT2Err[list(chip.nodes).index(qubit)], 7)),
                     ', xy error: ', str(round(bestXyErr[list(chip.nodes).index(qubit)], 7)),
                     ', zz error: ', str(round(bestZzErr[list(chip.nodes).index(qubit)], 7)),
                     ', all error: ', str(round(bestAllErr[list(chip.nodes).index(qubit)], 7))
                      + '\n')
    return chip

