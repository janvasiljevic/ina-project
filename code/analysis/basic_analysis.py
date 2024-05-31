import random

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from igraph import Graph, plot


def analyze_graph(graph):
    results = {}
    results["nodes"] = graph.vcount()
    results["edges"] = graph.ecount()
    results["density"] = graph.density()

    degrees = graph.degree()
    results["avg_degree"] = np.mean(degrees)
    results["std_degree"] = np.std(degrees)
    # distribution = graph.degree_distribution()
    # results['degree_distribution'] = distribution

    # results["diameter"] = graph.diameter()
    # results["avg_path_length"] = graph.average_path_length()

    results["avg_clustering"] = graph.transitivity_avglocal_undirected(mode="zero")
    # results["transitivity"] = graph.transitivity_undirected()

    components = graph.components(mode="weak")
    # results["components"] = components
    results["n_components"] = len(components)
    results["isolated_nodes"] = components.sizes().count(1)
    results["isolated_percent"] = results["isolated_nodes"] / graph.vcount()

    largest = components.giant()
    results["largest_component_size"] = largest.vcount()
    results["largest_component_percent"] = largest.vcount() / graph.vcount()

    # betweenness = graph.betweenness()
    # results["betweenness"] = betweenness
    # results["avg_betweenness"] = np.mean(betweenness)

    return results


def visualize_graph(g, path):
    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_label"] = g.vs["id"]
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


for type in ["", "_lcc"]:
    g_crates = ig.Graph.Read_GraphML(f"../../networks/crates_io{type}.graphml")
    results = analyze_graph(g_crates)

    g_npm = ig.Graph.Read_GraphML(f"../../networks/npm{type}.graphml")
    results_npm = analyze_graph(g_npm)

    g_npm_prod = ig.Graph.Read_GraphML(f"../../networks/npm_prod{type}.graphml")
    results_npm_prod = analyze_graph(g_npm_prod)

    g_python = ig.Graph.Read_GraphML(f"../../networks/pypi{type}.graphml")
    results_python = analyze_graph(g_python)

    results_df = pd.DataFrame(
        [results, results_npm, results_npm_prod, results_python],
        index=["crates", "npm", "npm_prod", "python"],
    )
    results_df.to_csv(f"../results/basic_analysis{type}.csv")
