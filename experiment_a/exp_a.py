import random
import networkx as nx
from collections import defaultdict
import copy
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import to_networkx
from helper_task07 import weisfeiler_lehman_hash_structural, find_isomorphic_groups_structural



def get_largest_iso_group(dataset):
    isomorphic_groups = find_isomorphic_groups_structural(dataset)
    largest_groups = max(isomorphic_groups.values(), key=len, default=[])
    return largest_groups


def perturb_graph(G):
    # randomy perturbs by either adding and edge or removing and edge

    G_perturbed = copy.deepcopy(G)

    perturbation_type = random.choice(['add', 'remove'])
    perturbation_info = {}

    if perturbation_type == 'add':
        nodes = list(G.nodes())
        possible_edges = [(u,v) for u in nodes for v in nodes if u<v] 
        existing_edges = list(G.edges())
        non_existing_edges = [edge for edge in possible_edges if edge not in existing_edges]
        
        if not non_existing_edges:
            perturbation_type = 'remove'
        else:
            new_edge = random.choice(non_existing_edges)
            G_perturbed.add_edge(*new_edge)
            perturbation_info = {
                'type': 'add',
                'edge': new_edge
                }
            return G_perturbed, perturbation_info
        
    if perturbation_type == 'remove':
        edge_to_remove = random.choice(list(G.edges()))
        G_perturbed.remove_edge(*edge_to_remove)
        perturbation_info = {
            'type': 'remove',
            'edge': edge_to_remove
        }
        
        return G_perturbed, perturbation_info # returns a tuple