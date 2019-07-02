from pprint import pprint

import networkx as nx
import pandas as pd

def visualize(graph):
    ''' Visualize '''
    nx.nx_agraph.view_pygraphviz(graph, prog='fdp')


if __name__ == '__main__':
    graph = nx.Graph()

    ''' import cities '''
    cities = pd.read_csv('data/city.csv')
    for idx, row in cities.iterrows():
        graphviz_attr = {
            'color': row['Color'],
            'fillcolor': row['Color'],
            'fontcolor': 'grey',
            'fontname': 'monospaced',
            'shape': 'hexagon',
            'style': 'filled',
            'width': 1.5, 'height': 1.5
        }
        graph.add_node(row['Name'], **graphviz_attr)

    ''' import edges '''
    edges = pd.read_csv('data/edge.csv')
    for idx, row in edges.iterrows():
        graph.add_edge(row['Source'], row['Target'])

    ''' print shortest path from Atlanta to each cities '''
    # print(nx.single_source_shortest_path(graph, source='Atlanta'))
    pprint(nx.single_source_shortest_path(graph, source='Teheran'))

    # print(graph.number_of_nodes())
    # print(graph.number_of_edges())
    # print(graph.number_of_selfloops())
    # print('Diameter', nx.diameter(graph))
    # print('Degree', nx.degree(graph))
    # pprint(nx.center(graph))
    # pprint(sorted(nx.betweenness_centrality(graph).items(), key=lambda x: x[1], reverse=True))
    # pprint(sorted(nx.eigenvector_centrality(graph, max_iter=200).items(), key=lambda x: x[1], reverse=True))
    # pprint(sorted(nx.closeness_centrality(graph).items(), key=lambda x: x[1], reverse=True))
    # pprint(sorted(nx.eccentricity(graph).items(), key=lambda x: x[1], reverse=True))
    # pprint(sorted(nx.pagerank(graph).items(), key=lambda x: x[1], reverse=True))

    visualize(graph)