import pdb
import networkx as nx
import igraph
import xml.etree.ElementTree as ET
from itertools import combinations
import copy

# tree = ET.parse('displays.xml')
# root = tree.getroot()
# index = 0
# authors_list = []
# graph_edges = []
#
#
# def add_authors_to_list(new_authors):
#     for author in new_authors:
#         if not author in authors_list:
#             authors_list.append(author)
#
#
# def add_edges_to_list(new_edges):
#     for edge in new_edges:
#         graph_edges.append(copy.deepcopy(edge))
#
#
# for article in root:
#     authors = list(map(lambda author: author.text, article.findall('author')))
#     add_authors_to_list(authors)
#     edges = combinations(authors, 2)
#     add_edges_to_list(edges)

# G = nx.Graph()
# G.add_edges_from(graph_edges)
edgess = [('Paweł', 'Viola'), ('Viola', 'Mateusz'), ('Mateusz', 'Kuba'), ('Kuba', 'Karolina'), ('Kuba', 'Paweł'),
          ('Viola', 'Kuba'), ('Radek', 'Alek')]
g = igraph.Graph()

vertex = []
for edge in edgess:
    vertex.extend(edge)

g.add_vertices(list(set(vertex)))  # add a list of unique vertices to the graph
g.add_edges(edgess)  # add the edges to the graph.

p = g.community_multilevel()
print(p)

q = g.modularity(p)
print(q)
# pdb.set_trace()
igraph.plot(p)
# community_optimal_modularity = g.community_optimal_modularity()
# print(community_optimal_modularity)
# pdb.set_trace()
