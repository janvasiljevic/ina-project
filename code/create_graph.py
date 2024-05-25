import json
from base64 import b64decode

import networkx as nx
import pandas as pd

def decode_deps(deps):
    # print(f'Deps: {deps}')
    deps = b64decode(deps)
    # print(f'Deps: {deps}')
    try:
        deps = deps.decode("utf-8")
    except:
        deps = "[]"
    deps = json.loads(deps)
    return deps

data = []
G = nx.DiGraph()
data = pd.read_csv("../networks/python-dependencies-downloads.csv", sep="\t", header=None, encoding="unicode_escape")
data.columns = ["name", "deps", "num_downloads"]
data["deps"] = data["deps"].apply(decode_deps)

for ex in data.iterrows():
    name = ex[1]["name"]
    deps = ex[1]["deps"]
    num_downloads = ex[1]["num_downloads"]

    # print(f'name: {name}, deps: {deps}')
    G.add_node("%s" % (name), downloads=str(num_downloads))
    for dep in deps:
        dep = dep.strip()
        dep = dep.replace('"', "")
        if '\n' in dep:
            nested_deps = dep.split('\n')
            new_dep = None
            for nested_dep in nested_deps:
                if not nested_dep.strip().startswith("#"):
                    new_dep = nested_dep.strip()
                    break
            if new_dep:
                dep = new_dep
            else:
                dep = ''
        
        if dep.startswith("#"):
            dep = ""
        dep = dep.split('#')[0]    
        
        dep = dep.split(">")[0]
        dep = dep.split('=')[0]
        dep = dep.split("<")[0]
        if dep and dep[0] == "#":
            print(f'found # in dep for package {name}: {dep}')
        if dep:
            # print(f'final dep: {dep}')
            G.add_edge("%s" % (name), dep.replace('"', ""))


print("Number of nodes: ", G.number_of_nodes())
print("Number of edges: ", G.number_of_edges())
print("Number of connected components: ", nx.number_weakly_connected_components(G))

nx.write_pajek(G, "python-dependencies.net")
