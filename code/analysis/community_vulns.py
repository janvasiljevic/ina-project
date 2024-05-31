from collections import Counter, defaultdict

import igraph as ig
import numpy as np
import pandas as pd
from tqdm import tqdm


def print_top_pacakges_by_metric(graph, metric, top_n=10):
    top_packages = sorted(
        [(graph.vs[i], metric[i]) for i in range(len(metric))],
        key=lambda x: x[1],
        reverse=True,
    )[:top_n]

    for package, value in top_packages:
        if "vuln_count" not in package.attributes():
            print(f"{package['name']}: {value}")
        else:
            print(f"{package['name']} ({package['vuln_count']}): {value}")


def vulnerabilities_per_community(graph, communities, vulns):
    vuln_communities = []
    community_vulns = defaultdict(list)
    for _, vuln in tqdm(
        vulns.iterrows(), desc="Enumerating vulnerabilities", total=len(vulns)
    ):
        try:
            vuln_id = graph.vs.find(name=vuln["package"]).index
            comm = communities.membership[vuln_id]
            vuln_communities.append(comm)
            community_vulns[comm].append(vuln["package"])
        except ValueError:
            # Package is not in the graph
            pass

    return Counter(vuln_communities), community_vulns


graph = ig.Graph.Read_GraphML("../../networks/npm_prod_lcc.graphml")
vulns = pd.read_csv("../vulnerability/npm_grouped.csv")

communities = graph.as_undirected().community_leiden(
    objective_function="modularity", n_iterations=-1
)
print(len(communities))

vulns_per_community, community_vulns = vulnerabilities_per_community(
    graph, communities, vulns
)

pr = np.array(graph.pagerank())
for comm, count in vulns_per_community.most_common(5):
    community = graph.subgraph(communities[comm])
    community_pr = pr[communities[comm]]

    print(f"Community {comm} ({count} vulns)")
    print_top_pacakges_by_metric(community, community_pr)
    print()
