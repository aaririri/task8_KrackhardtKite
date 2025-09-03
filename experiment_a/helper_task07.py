#!/usr/bin/env python3
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import to_networkx
import networkx as nx
import collections

def weisfeiler_lehman_hash_structural(graph):
    properties = nx.betweenness_centrality(graph)
    # continuous values into bins
    values = list(properties.values())
    if values:
        max_val, min_val = max(values), min(values)
        if max_val > min_val:
            bin_size = (max_val - min_val) / 10             # 10 bins
            properties = {node: int((val - min_val) / bin_size) if bin_size > 0 else 0  
                        for node, val in properties.items()}
        else:
            properties = {node: 0 for node in properties}
    
    # colors based on structural property
    colors = {node: properties.get(node, 0) for node in graph.nodes()}

    for _ in range(len(graph.nodes())):
        new_colors = {}
        for node in graph.nodes():
            neighbor_colors = sorted([colors[nbr] for nbr in graph.neighbors(node)])
            signature = (colors[node], tuple(neighbor_colors))
            new_colors[node] = hash(signature)

        if new_colors == colors:
            break
        colors = new_colors

    canonical_hash = str(sorted(colors.values()))
    return canonical_hash


def find_isomorphic_groups_structural(dataset):
    hashes = collections.defaultdict(list)

    for i, data in enumerate(dataset):
        g = to_networkx(data, node_attrs=['x'])

        if len(g) > 0:
            h = weisfeiler_lehman_hash_structural(g)
            hashes[h].append(i)

    isomorphic_groups = {h: indices for h, indices in hashes.items() if len(indices) > 1}
    return isomorphic_groups