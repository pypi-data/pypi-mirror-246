from pathlib import Path
import json
import networkx as nx

H = 8
W = 6

def load_chip_data_from_file(
    H = H, W = W,
    qubit_data_filename = r"./chipdata/qubit_data.json",
    xy_crosstalk_filename = r"./chipdata/xy_crosstalk_sim.json"    
):
    with open(qubit_data_filename, "r", encoding="utf-8") as file:
        content = file.read()
        chip_data_dic = json.loads(content)
        file.close()

    with open(xy_crosstalk_filename, "r", encoding="utf-8") as file:
        content = file.read()
        xy_crosstalk_sim_dic = json.loads(content)
        file.close()

    chip = nx.grid_2d_graph(H, W)

    # sweetPointArray = np.zeros((H, W))

    # 生成随机sweet point array
    # for i in range(H):
    #     for j in range(W):
    #         if (i + j) % 2:
    #             sweetPointArray[i, j] = (
    #                 max((4.0 + 0.4 * (np.random.random() - 0.5)), 3.751) * 1e3
    #             )
    #         else:
    #             sweetPointArray[i, j] = (4.5 + 0.4 * (np.random.random() - 0.5)) * 1e3
    unused_nodes = []
    for qubit in chip:
        qubit_name = f'q{qubit[0]*W+qubit[1]+1}'
        chip.nodes[qubit]['name'] = qubit_name
        if qubit_name in chip_data_dic:
            chip.nodes[qubit]['available'] = True
        else:
            # chip.nodes[qubit]['available'] = False
            unused_nodes.append(qubit)
            continue
        allow_freq = chip_data_dic[qubit_name]['allow_freq']
        # chip.nodes[qubit]['allow_freq'] = np.arange(min(allow_freq), max(allow_freq), 1)
        chip.nodes[qubit]['allow_freq'] = allow_freq
        chip.nodes[qubit]['bad_freq_range'] = chip_data_dic[qubit_name][
            'bad_freq_range'
        ]
        chip.nodes[qubit]['ac_spectrum'] = chip_data_dic[qubit_name]['ac_spectrum']
        chip.nodes[qubit]['sweet point'] = chip.nodes[qubit]['ac_spectrum'][0]
        chip.nodes[qubit]['t1_spectrum'] = chip_data_dic[qubit_name]['t1_spectrum']
        chip.nodes[qubit]['anharm'] = -230
        chip.nodes[qubit]['t_sq'] = 20
        chip.nodes[qubit]['xy_crosstalk_coef'] = {}
    chip.remove_nodes_from(unused_nodes)

    for qubit in chip.nodes():
        xy_crosstalk_dic = chip_data_dic['xy_crosstalk']
        xy_crosstalk = chip_data_dic['xy_crosstalk']['xy_crosstalk']
        qubit_idx = chip_data_dic['xy_crosstalk']['target_bit'].index(
            chip.nodes[qubit]['name']
        )
        for neighbor in chip.nodes():
            if not chip.nodes[neighbor]['available']:
                continue
            neighbor_idx = chip_data_dic['xy_crosstalk']['bias_bit'].index(
                chip.nodes[neighbor]['name']
            )
            chip.nodes[qubit]['xy_crosstalk_coef'][neighbor] = xy_crosstalk[qubit_idx][
                neighbor_idx
            ]

    return chip, xy_crosstalk_sim_dic

def gen_pos(chip):
    # wStep = 1
    # hStep = 1
    pos = dict()
    for qubit in chip:
        # pos[qubit] = [qubit[0] * wStep, qubit[1] * hStep]
        pos[qubit] = [qubit[1], -qubit[0]]
    return pos


def twoQ_gen_pos(chip, xtalkG):
    bitPos = gen_pos(chip)
    for bit in bitPos:
        bitPos[bit][0] *= 2
        bitPos[bit][1] *= 2
    pos = dict()
    for coupler in xtalkG:
        pos[coupler] = [
            (bitPos[coupler[0]][0] + bitPos[coupler[1]][0]) / 2,
            (bitPos[coupler[0]][1] + bitPos[coupler[1]][1]) / 2,
        ]
    return pos

def max_Algsubgraph(chip):
    dualChip = nx.Graph()
    dualChip.add_nodes_from(list(chip.edges))
    for coupler1 in dualChip.nodes:
        for coupler2 in dualChip.nodes:
            if coupler1 == coupler2 or set(coupler1).isdisjoint(set(coupler2)):
                continue
            else:
                dualChip.add_edge(coupler1, coupler2)
    maxParallelCZs = [[], [], [], []]
    for edge in chip.edges:
        if sum(edge[0]) < sum(edge[1]):
            start = edge[0]
            end = edge[1]
        else:
            start = edge[1]
            end = edge[0]
        if start[0] == end[0]:
            if sum(start) % 2:
                maxParallelCZs[0].append(edge)
            else:
                maxParallelCZs[2].append(edge)
        else:
            if sum(start) % 2:
                maxParallelCZs[1].append(edge)
            else:
                maxParallelCZs[3].append(edge)
    return maxParallelCZs

def xtalk_G(chip):
    xtalkG = nx.Graph()
    for coupler1 in chip.edges:
        if not (coupler1 in xtalkG.nodes):
            xtalkG.add_node(coupler1)
        if not (xtalkG.nodes[coupler1].get('two tq')):
            xtalkG.nodes[coupler1]['two tq'] = 60
        for coupler2 in chip.edges:
            if coupler1 == coupler2 or (coupler1, coupler2) in xtalkG.edges:
                continue
            distance = []
            for i in coupler1:
                for j in coupler2:
                    if nx.has_path(chip, i, j):
                        distance.append(nx.shortest_path_length(chip, i, j))
                    else:
                        distance.append(100000)
            if 1 in distance and not (0 in distance):
                xtalkG.add_edge(coupler1, coupler2)
    return xtalkG

