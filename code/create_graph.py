import json
from base64 import b64decode

import networkx as nx
import pandas as pd

data = []
G = nx.Graph()
data = pd.read_csv("pypi-deps.csv", sep="\t", header=None, encoding="unicode_escape")
data.columns = ["name", "deps"]
data["deps"] = data["deps"].apply(lambda x: json.loads(b64decode(x).decode("utf-8")))

for ex in data.iterrows():
    name = ex[1]["name"]
    deps = ex[1]["deps"]
    G.add_node("%s" % (name))
    for dep in deps:
        if not "#" in dep:
            G.add_edge("%s" % (name), dep.replace('"', ""))


nx.write_gml(G, "test.gml")
