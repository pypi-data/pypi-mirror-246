
from copy import deepcopy
import random
from matplotlib import pyplot as plt
import matplotlib
from freq_allocator.dataloader.load_chip import gen_pos, max_Algsubgraph, twoQ_gen_pos, xtalk_G
import networkx as nx
from scipy.optimize import minimize

from freq_allocator.model.two_qubit_model import twoQ_err_model, twoq_T1_err, twoq_T2_err, twoq_xtalk_err

def twoq_alloc(chip, H, W, conflictNodeDict, conflictEdge, twoQForbiddenCoupler, a):
    removeQCQs = []
    for qcq in chip.edges:
        removeQCQ = False
        for q in qcq:
            if chip.nodes[q]['frequency'] < 3.75 or conflictNodeDict[q] == 'red':
                removeQCQ = True
                break
        if removeQCQ:
            removeQCQs.append(qcq)
            continue
        if (
            (qcq in conflictEdge)
            or (qcq[::-1] in conflictEdge)
            or (qcq in twoQForbiddenCoupler)
            or (qcq[::-1] in twoQForbiddenCoupler)
        ):
            removeQCQs.append(qcq)
            continue

    chip.remove_edges_from(removeQCQs)
    maxParallelCZs = max_Algsubgraph(chip)
    xtalkG = xtalk_G(chip)

    for level in range(len(maxParallelCZs)):
        couplerActivate = [[coupler, 'gray'] for coupler in chip.edges]
        for i in couplerActivate:
            if i[0] in maxParallelCZs[level]:
                i[1] = 'green'
        pos = gen_pos(chip)
        plt.figure(figsize=(4, 8))
        nx.draw_networkx_edges(
            chip,
            pos,
            edgelist=chip.edges,
            edge_color=list(dict(couplerActivate).values()),
            edge_cmap=plt.cm.Reds_r,
            width=8,
        )
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.Reds_r)
        plt.axis('off')
        plt.savefig('twoq chip ' + str(level) + '.pdf', dpi=300)
        plt.close()

    xtalkGs = []
    for level in range(len(maxParallelCZs)):
        print('level', level)
        if len(maxParallelCZs[level]) == 0:
            continue
        epoch = 0
        conflictQCQPercents = []
        conflictQCQDict = dict()
        xTalkSubG = deepcopy(xtalkG)
        for qcq in xtalkG.nodes:
            if qcq in maxParallelCZs[level]:
                conflictQCQDict[qcq] = 'gray'
        xTalkSubG.remove_nodes_from(
            set(xtalkG.nodes).difference(set(maxParallelCZs[level]))
        )

        distance = dict()
        for qcq in xTalkSubG:
            if nx.has_path(chip, qcq[0], (H // 2, W // 2)):
                distance[qcq] = nx.shortest_path_length(
                    chip, qcq[0], (H // 2, W // 2)
                ) + nx.shortest_path_length(chip, qcq[1], (H // 2, W // 2))
            else:
                distance[qcq] = 100000
        centertwoQ = sorted(distance.items(), key=lambda x: x[1])[0]
        centerConflictQCQ = centertwoQ[0]

        for _ in range(20):
            reOptimizeQCQs = [centerConflictQCQ]
            for qcq in xTalkSubG.nodes():
                if (
                    conflictQCQDict[centerConflictQCQ] == 'gray'
                    and not (qcq in reOptimizeQCQs)
                    and not (xTalkSubG.nodes[qcq].get('frequency', False))
                    and qcq in xTalkSubG[centerConflictQCQ]
                ):
                    reOptimizeQCQs.append(qcq)
                elif (
                    conflictQCQDict[centerConflictQCQ] == 'red'
                    and not (qcq in reOptimizeQCQs)
                    and qcq in xTalkSubG[centerConflictQCQ]
                    and distance[qcq] >= distance[centerConflictQCQ]
                    and conflictQCQDict[qcq] == 'red'
                ):
                    reOptimizeQCQs.append(qcq)

            reOptimizeQCQs = tuple(reOptimizeQCQs)
            bounds = []
            for qcq in reOptimizeQCQs:
                if chip.nodes[qcq[0]]['frequency'] > chip.nodes[qcq[1]]['frequency']:
                    qh, ql = qcq[0], qcq[1]
                else:
                    qh, ql = qcq[1], qcq[0]
                bounds.append(
                    (
                        max(
                            3.75,
                            chip.nodes[qh]['sweet point']
                            - 0.7
                            + chip.nodes[qh]['anharm'],
                        ),
                        chip.nodes[ql]['sweet point'],
                    )
                )
            ini_frequency = [(max(bound) + min(bound)) / 2 for bound in bounds]
            res = minimize(
                twoQ_err_model,
                ini_frequency,
                args=(chip, xTalkSubG, reOptimizeQCQs, a),
                method='L-BFGS-B',
                bounds=bounds,
                options={'maxiter': 200},
            )
            print('err estimate', res.fun)
            ini_frequency = res.x

            for qcq in reOptimizeQCQs:
                xTalkSubG.nodes[qcq]['frequency'] = round(
                    res.x[reOptimizeQCQs.index(qcq)], 3
                )

            newreOptimizeQCQs, conflictQCQEdge = twoQ_checkcoli(chip, H, W, xTalkSubG, a)

            conflictCount = dict()
            for edge in conflictQCQEdge:
                if edge[0] in conflictQCQDict:
                    if edge[0] in conflictCount:
                        conflictCount[edge[0]] += 1
                    else:
                        conflictCount[edge[0]] = 1
                if edge[1] in conflictQCQDict:
                    if edge[1] in conflictCount:
                        conflictCount[edge[1]] += 1
                    else:
                        conflictCount[edge[1]] = 1

            conflictQCQEdgeDict = dict()
            alreadyConflict = []
            for edge in xTalkSubG.edges:
                if edge in conflictQCQEdge:
                    conflictQCQEdgeDict[edge] = 'red'
                    if edge[0] in alreadyConflict:
                        if conflictQCQDict[edge[0]] == 'red':
                            conflictQCQDict[edge[1]] = 'green'
                            alreadyConflict.append(edge[1])
                        else:
                            conflictQCQDict[edge[1]] = 'red'
                            alreadyConflict.append(edge[1])
                    elif edge[1] in alreadyConflict:
                        if conflictQCQDict[edge[1]] == 'red':
                            conflictQCQDict[edge[0]] = 'green'
                            alreadyConflict.append(edge[0])
                        else:
                            conflictQCQDict[edge[0]] = 'red'
                            alreadyConflict.append(edge[0])
                    else:
                        if nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), edge[0][0], (H // 2, W // 2)
                        ) + nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), edge[0][1], (H // 2, W // 2)
                        ) > nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), edge[1][0], (H // 2, W // 2)
                        ) + nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), edge[1][1], (H // 2, W // 2)
                        ):
                            conflictQCQDict[edge[0]] = 'red'
                            conflictQCQDict[edge[1]] = 'green'
                        else:
                            conflictQCQDict[edge[1]] = 'red'
                            conflictQCQDict[edge[0]] = 'green'
                        alreadyConflict.append(edge[0])
                        alreadyConflict.append(edge[1])
                elif xTalkSubG.nodes[edge[0]].get(
                    'frequency', False
                ) and xTalkSubG.nodes[edge[1]].get('frequency', False):
                    conflictQCQEdgeDict[edge] = 'green'
                    if not (edge[0] in alreadyConflict):
                        conflictQCQDict[edge[0]] = 'green'
                    elif not (edge[1] in alreadyConflict):
                        conflictQCQDict[edge[1]] = 'green'
                else:
                    conflictQCQEdgeDict[edge] = 'gray'

            for qcq in xTalkSubG.nodes:
                if qcq in newreOptimizeQCQs:
                    conflictQCQDict[qcq] = 'red'
                if (
                    xTalkSubG.nodes[qcq].get('frequency', False)
                    and conflictQCQDict[qcq] == 'gray'
                ):
                    conflictQCQDict[qcq] = 'green'

            conflictQCQPercents.append(
                len([qcq for qcq in conflictQCQDict if conflictQCQDict[qcq] == 'red'])
                / len(
                    [
                        qcq
                        for qcq in conflictQCQDict
                        if conflictQCQDict[qcq] == 'red'
                        or conflictQCQDict[qcq] == 'green'
                    ]
                )
            )
            print('conflict percent', conflictQCQPercents[-1])

            pos = twoQ_gen_pos(chip, xTalkSubG)
            nx.draw_networkx_nodes(
                xTalkSubG,
                pos,
                nodelist=xTalkSubG.nodes,
                node_color=list(conflictQCQDict.values()),
                cmap=plt.cm.Reds_r,
            )
            nx.draw_networkx_edges(
                xTalkSubG,
                pos,
                edgelist=xTalkSubG.edges,
                edge_color=list(conflictQCQEdgeDict.values()),
                edge_cmap=plt.cm.Reds_r,
            )
            plt.axis('off')
            plt.savefig(
                str(level) + ' ' + str(epoch) + str(W) + str(H) + 'twoq conflict.pdf',
                dpi=300,
            )
            plt.close()

            reOptimizeQCQs = newreOptimizeQCQs
            emptyQCQ = dict(
                [
                    (
                        qcq,
                        nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), qcq[0], (H // 2, W // 2)
                        )
                        + nx.shortest_path_length(
                            nx.grid_2d_graph(H, W), qcq[1], (H // 2, W // 2)
                        ),
                    )
                    for qcq in xTalkSubG.nodes()
                    if not (xTalkSubG.nodes[qcq].get('frequency', False))
                ]
            )

            if len(emptyQCQ) > 0:
                centerConflictQCQ = list(sorted(emptyQCQ.items(), key=lambda x: x[1]))[
                    0
                ][0]
                # centerConflictQCQ = random.choices(list(emptyQCQ.keys()), weights=[1 / (distance + 1e-5) for distance in emptyQCQ.values()], k=1)[0]
            elif len(reOptimizeQCQs) > 0:
                centerConflictQCQ = random.choices(
                    list(reOptimizeQCQs.keys()),
                    weights=[
                        1 / (distance + 1e-5) for distance in reOptimizeQCQs.values()
                    ],
                    k=1,
                )[0]
            elif conflictQCQPercents[-1] == 0:
                break
            epoch += 1

        pos = gen_pos(chip)
        intList = []
        intDict = dict()
        for qcq in chip.edges:
            if qcq in xTalkSubG.nodes:
                intList.append(xTalkSubG.nodes[qcq]['frequency'])
                intDict[qcq] = xTalkSubG.nodes[qcq]['frequency']
            else:
                intList.append(4.0)
                intDict[qcq] = 4.0
        fig, ax = plt.figure(figsize=(8, 16))
        nx.draw_networkx_edges(
            chip,
            pos,
            edgelist=chip.edges,
            edge_color=intList,
            edge_cmap=plt.cm.Reds_r,
            width=8,
        )
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.Reds_r)
        nx.draw_networkx_edge_labels(
            chip, pos, intDict, font_size=10, font_color='black'
        )
        plt.axis('off')
        plt.colorbar(
            matplotlib.cm.ScalarMappable(
                norm=matplotlib.colors.Normalize(vmin=3.75, vmax=4.5),
                cmap=plt.cm.Reds_r,
            ),
            ax = ax
        )
        plt.savefig(
            str(level) + ' ' + str(epoch) + str(W) + str(H) + 'int freq.pdf', dpi=300
        )
        plt.close()
        xtalkGs.append(xTalkSubG)

    return xtalkGs


def twoQ_checkcoli(chip, H, W, xtalkG, a):
    distance = dict()
    reOptimizeQCQs = dict()
    conflictEdge = []
    for qcq in xtalkG:
        distance[qcq] = nx.shortest_path_length(
            nx.grid_2d_graph(H, W), qcq[0], (H // 2, W // 2)
        ) + nx.shortest_path_length(nx.grid_2d_graph(H, W), qcq[1], (H // 2, W // 2))
    centertwoQ = sorted(distance.items(), key=lambda x: x[1])[0][0]
    for qcq in xtalkG.nodes:
        if xtalkG.nodes[qcq].get('frequency', False):
            if sum(qcq[0]) % 2:
                T1Cost1 = twoq_T1_err(
                    xtalkG.nodes[qcq]['frequency'],
                    chip.nodes[qcq[0]]['frequency'],
                    chip.nodes[qcq[0]]['sweet point'],
                    a[0],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[0]]['t1_spectrum'],
                )
                T1Cost2 = twoq_T1_err(
                    xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'],
                    chip.nodes[qcq[1]]['frequency'],
                    chip.nodes[qcq[1]]['sweet point'],
                    a[0],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[1]]['t1_spectrum'],
                )
                T2Cost1 = twoq_T2_err(
                    xtalkG.nodes[qcq]['frequency'],
                    chip.nodes[qcq[0]]['frequency'],
                    chip.nodes[qcq[0]]['sweet point'],
                    a[1],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[0]]['df/dphi'],
                )
                T2Cost2 = twoq_T2_err(
                    xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[1]]['anharm'],
                    chip.nodes[qcq[1]]['frequency'],
                    chip.nodes[qcq[1]]['sweet point'],
                    a[1],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[1]]['df/dphi'],
                )
            else:
                T1Cost1 = twoq_T1_err(
                    xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'],
                    chip.nodes[qcq[0]]['frequency'],
                    chip.nodes[qcq[0]]['sweet point'],
                    a[0],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[0]]['t1_spectrum'],
                )
                T1Cost2 = twoq_T1_err(
                    xtalkG.nodes[qcq]['frequency'],
                    chip.nodes[qcq[1]]['frequency'],
                    chip.nodes[qcq[1]]['sweet point'],
                    a[0],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[1]]['t1_spectrum'],
                )
                T2Cost1 = twoq_T2_err(
                    xtalkG.nodes[qcq]['frequency'] - chip.nodes[qcq[0]]['anharm'],
                    chip.nodes[qcq[0]]['frequency'],
                    chip.nodes[qcq[0]]['sweet point'],
                    a[1],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[0]]['df/dphi'],
                )
                T2Cost2 = twoq_T2_err(
                    xtalkG.nodes[qcq]['frequency'],
                    chip.nodes[qcq[1]]['frequency'],
                    chip.nodes[qcq[1]]['sweet point'],
                    a[1],
                    xtalkG.nodes[qcq]['two tq'],
                    chip.nodes[qcq[1]]['df/dphi'],
                )
            if (
                T1Cost1 / a[0] > 1e-2
                or T1Cost2 / a[0] > 1e-2
                or T2Cost1 / a[1] > 3e-1
                or T2Cost2 / a[1] > 3e-1
            ):
                print(
                    qcq,
                    't1 t2',
                    T1Cost1 / a[0],
                    T1Cost2 / a[0],
                    T2Cost1 / a[1],
                    T2Cost2 / a[1],
                )
                if not (qcq in reOptimizeQCQs):
                    if nx.has_path(xtalkG, qcq, centertwoQ):
                        reOptimizeQCQs[qcq] = nx.shortest_path_length(
                            xtalkG, qcq, centertwoQ
                        )
                    else:
                        reOptimizeQCQs[qcq] = 1000

            # twoqxyCost = 0
            twoqidleCost = 0
            for q in qcq:
                if sum(q) % 2:
                    fWork = xtalkG.nodes[qcq]['frequency']
                else:
                    fWork = xtalkG.nodes[qcq]['frequency'] - chip.nodes[q]['anharm']
                for neighbor in chip.nodes():
                    if neighbor in qcq:
                        continue
                    # if chip.nodes[neighbor]['xy_crosstalk_coef'][q] > MUTHRESHOLD:
                    #     twoqxyCost += twoq_xy_err(chip.nodes[q]['anharm'], [fWork, chip.nodes[q]['frequency']],
                    #                     chip.nodes[neighbor]['frequency'], chip.nodes[neighbor]['xy_crosstalk_coef'][q],
                    #                     chip.nodes[q]['xy xtalk'], a[2], xtalkG.nodes[qcq]['two tq'])
                    if neighbor in chip[q]:
                        twoqidleCost += twoq_xtalk_err(
                            [fWork, chip.nodes[q]['frequency']],
                            [
                                chip.nodes[neighbor]['frequency'],
                                chip.nodes[neighbor]['frequency'],
                            ],
                            a[3],
                            a[4],
                            xtalkG.nodes[qcq]['two tq'],
                        )
                        twoqidleCost += twoq_xtalk_err(
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
            # if twoqxyCost / a[2] > 1e-2 and not(qcq in reOptimizeQCQs):
            #     print(qcq, 'xy', twoqxyCost / a[2])
            #     reOptimizeQCQs[qcq] = nx.shortest_path_length(xtalkG, qcq, centertwoQ)
            if twoqidleCost > 3e-1 and not (qcq in reOptimizeQCQs):
                if nx.has_path(xtalkG, qcq, centertwoQ):
                    reOptimizeQCQs[qcq] = nx.shortest_path_length(
                        xtalkG, qcq, centertwoQ
                    )
                else:
                    reOptimizeQCQs[qcq] = 1000
                print(qcq, 'idle', twoqidleCost)

            for neighbor in xtalkG[qcq]:
                if xtalkG.nodes[neighbor].get('frequency', False):
                    for q0 in qcq:
                        for q1 in neighbor:
                            if (q0, q1) in chip.edges:
                                intCost = twoq_xtalk_err(
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
                                    intCost += twoq_xtalk_err(
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
                                    intCost += twoq_xtalk_err(
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
                                    intCost += twoq_xtalk_err(
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
                                    intCost += twoq_xtalk_err(
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
                                if (
                                    not (
                                        (qcq, neighbor) in conflictEdge
                                        or (neighbor, qcq) in conflictEdge
                                    )
                                    and intCost > 3e-1
                                ):
                                    print(qcq, neighbor, 'int', intCost)
                                    conflictEdge.append((qcq, neighbor))

    return reOptimizeQCQs, conflictEdge
