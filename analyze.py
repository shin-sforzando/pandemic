from pprint import pprint

import networkx as nx
import pandas as pd


def main():
    G = nx.Graph()
    cities = pd.read_csv('data/city.csv')
    for idx, row in cities.iterrows():
        gviz_attr = {
            'color': row['Color'],
            'fillcolor': row['Color'],
            'fontcolor': 'grey',
            'fontname': 'monospaced',
            'shape': 'hexagon',
            'style': 'filled',
            'width': 1.5, 'height': 1.5
        }
        G.add_node(row['Name'], **gviz_attr)
    edges = pd.read_csv('data/edge.csv')
    for idx, row in edges.iterrows():
        G.add_edge(row['Source'], row['Target'])
    pprint(nx.single_source_shortest_path(G, source='Atlanta'))
    nx.nx_agraph.view_pygraphviz(G, prog='fdp')


if __name__ == "__main__":
    main()
