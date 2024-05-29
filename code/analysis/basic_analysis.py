import igraph as ig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from igraph import Graph, plot
import random



def analyze_graph(graph):
    results = {}
    results['nodes'] = graph.vcount()
    results['edges'] = graph.ecount()
    results['density'] = graph.density()

    degrees = graph.degree()
    results['avg_degree'] = np.mean(degrees)
    results['std_degree'] = np.std(degrees)
    distribution = graph.degree_distribution()
    results['degree_distribution'] = distribution

    results['diameter'] = graph.diameter()
    results['avg_path_length'] = graph.average_path_length()

    results['avg_clustering'] = graph.transitivity_avglocal_undirected(mode='zero')
    results['transitivity'] = graph.transitivity_undirected()

    components = graph.components()
    # results['components'] = components
    results['n_components'] = components[0]
    results['largest_component_size'] = components.giant().vcount()

    betweenness = graph.betweenness()
    # results['betweenness'] = betweenness
    results['avg_betweenness'] = np.mean(betweenness)

    return results

def visualize_graph(g, path):
    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_label"] = g.vs['id']
    visual_style["edge_width"] = 1
    visual_style["layout"] = g.layout("kk")  # Kamada-Kawai layout
    plot(g, target=path, **visual_style)
    

def random_walk_sampling(g, start_node, walk_length):
    visited = set([start_node])
    current_node = start_node
    
    for _ in range(walk_length):
        neighbors = g.neighbors(current_node)
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        visited.add(next_node)
        current_node = next_node
    
    subgraph = g.induced_subgraph(list(visited))
    return subgraph




g_crates = ig.Graph.Read_GraphML("../../networks/crates_io.graphml")
g_crates = g_crates.simplify()
g_crates = random_walk_sampling(g_crates, 0, 100000)

results = analyze_graph(g_crates)
print(results)

g_npm = ig.Graph.Read_GraphML("../../networks/npm_graph_full.graphml")
# g_npm = g_npm.simplify()
g_npm = random_walk_sampling(g_npm, 0, 100000)

results_npm = analyze_graph(g_npm)
print(results_npm)

g_python = ig.Graph.Read_GraphML("../../networks/python-dependencies.graphml")
g_python = g_python.simplify()
g_python = random_walk_sampling(g_python, 0, 100000)

results_python = analyze_graph(g_python)
print(results_python)

results_df = pd.DataFrame([results, results_npm, results_python], index=['crates', 'npm', 'python'])
results_df.to_csv('results.csv')
