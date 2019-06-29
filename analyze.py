import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from pprint import pprint

def main():
    Graph = nx.Graph()
    cities = pd.read_csv('data/city.csv')
    for idx, row in cities.iterrows():
        Graph.add_node(row['Id'], name=row['Label'], color=row['Color'])
    edges = pd.read_csv('data/edge.csv')
    for idx, row in edges.iterrows():
        Graph.add_edge(row['Source'], row['Target'])
    pprint(nx.single_source_shortest_path(Graph, source=0))
    nx.nx_agraph.view_pygraphviz(Graph, prog='fdp')


if __name__ == "__main__":
    main()
