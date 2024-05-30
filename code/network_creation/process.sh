if [ -f ../../networks/npm_graph_full.net ]; then mv ../../networks/npm_graph_full.net ../../networks/npm.net; fi
if [ -f ../../networks/python-dependencies.net ]; then mv ../../networks/python-dependencies.net ../../networks/pypi.net; fi

if [ -f ../../networks/pypi.net.bak ]; then rm ../../networks/pypi.net; mv ../../networks/pypi.net.bak ../../networks/pypi.net; fi
if [ -f ../../networks/crates_io.net.bak ]; then rm ../../networks/crates_io.net; mv ../../networks/crates_io.net.bak ../../networks/crates_io.net; fi
if [ -f ../../networks/npm.net.bak ]; then rm ../../networks/npm.net; mv ../../networks/npm.net.bak ../../networks/npm.net; fi
if [ -f ../../networks/npm_prod.net.bak ]; then rm ../../networks/npm_prod.net; mv ../../networks/npm_prod.net.bak ../../networks/npm_prod.net; fi

python fix_pajek_igraph.py
python to_graphml.py
python to_lcc.py