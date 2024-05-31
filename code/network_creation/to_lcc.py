import igraph as ig


def convert_to_lcc(path):
    print(f"Converting {path}")
    g = ig.read(path)

    components = g.components(mode="weak")
    largest = components.giant()

    print(f"Original: {g.vcount()} nodes, {g.ecount()} edges")
    print(f"LCC: {largest.vcount()} nodes, {largest.ecount()} edges")

    largest.write_graphml(path.replace(".graphml", "_lcc.graphml"))


convert_to_lcc("../../networks/pypi.graphml")
convert_to_lcc("../../networks/crates_io.graphml")
convert_to_lcc("../../networks/npm.graphml")
convert_to_lcc("../../networks/npm_prod.graphml")
