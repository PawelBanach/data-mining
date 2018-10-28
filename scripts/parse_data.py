import pdb
import networkx as nx
import igraph
import xml.etree.ElementTree as ET
from itertools import combinations
import copy

tree = ET.parse('displays.xml')
root = tree.getroot()
index = 0
authors_list = []
graph_edges = []


def add_authors_to_list(new_authors):
    for author in new_authors:
        if author not in authors_list:
            authors_list.append(author)


def add_edges_to_list(new_edges):
    for edge in new_edges:
        graph_edges.append(copy.deepcopy(edge))


for article in root:
    authors = list(map(lambda author: author.text, article.findall('author')))
    add_authors_to_list(authors)
    edges = combinations(authors, 2)
    add_edges_to_list(edges)

g = igraph.Graph()

vertex = []
for edge in graph_edges:
    vertex.extend(edge)

g.add_vertices(list(set(vertex)))  # add a list of unique vertices to the graph
g.add_edges(graph_edges)  # add the edges to the graph.

print('Communities:')
p = g.community_multilevel()
print(p)

print('Modularity')
q = g.modularity(p)
print(q)


g.vs["label"] = g.vs["name"]

# layout = g.layout("mds")
layout = g.layout("graphopt")
igraph.plot(p, layout=layout, bbox=(10000, 10000), vertex_size=40, edge_width=1, label_size=10)
