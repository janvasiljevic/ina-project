import igraph as ig


def to_graphml(path):
    print(f"Converting {path}")
    g = ig.read(path)

    if "name_" in g.vs.attribute_names():
        for v in g.vs:
            v["name"] = v["name_"]
        del g.vs["name_"]

    del g.vs["x"]
    del g.vs["y"]
    del g.vs["shape"]
    del g.es["weight"]

    g.write_graphml(path.replace(".net", ".graphml"))


to_graphml("../../networks/python-dependencies.net")
to_graphml("../../networks/crates_io.net")
to_graphml("../../networks/npm_graph_full.net")
