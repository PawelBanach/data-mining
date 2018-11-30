import pdb
import networkx as nx
import igraph
from lxml import etree
from igraph import Graph, mean
from itertools import combinations
import copy

xml = 'dblp.xml'
#xml = 'displays.xml'

index = 0
authors_list = set()
graph_edges = []
title = ''


def add_authors_to_list(new_authors):
    for author in new_authors:
        authors_list.add(author)


def add_edges_to_list(new_edges):
    for edge in new_edges:
        graph_edges.append(copy.deepcopy(edge))


authors = []
i = 0
max_authors = 0
for event, elem in etree.iterparse(source=xml, dtd_validation=False,
                                   load_dtd=True):  # ET.iterparse(xml, events=('start', 'end', 'start-ns', 'end-ns')):
    if i % 20000 == 0:
        print(i, len(graph_edges), max_authors)
        max_authors = 0

    if event == 'end':
        i = i + 1

        if elem.tag == 'title':
            title = elem.text

        if elem.tag == 'article' or elem.tag == 'inproceedings' or elem.tag == 'incollection' or elem.tag == 'proceedings' or elem.tag == 'www' or elem.tag == 'phdthesis' or elem.tag == 'mastersthesis' or elem.tag == 'book':
            if len(authors) > 1:
                if elem.tag == 'article' or elem.tag == 'inproceedings' or elem.tag == 'incollection' or elem.tag == 'proceedings':
                    if len(authors) > max_authors:
                        max_authors = len(authors)
                    if len(authors) > 200:
                        print(len(authors), title)
                    add_authors_to_list(authors)
                    edges = combinations(authors, 2)
                    add_edges_to_list(edges)
                else:
                    authors = []
            authors = []
        if elem.tag == 'author' and elem.tag is not None:
            authors.append(elem.text)

    elem.clear()

g = igraph.Graph()

vertex = []
for edge in graph_edges:
    vertex.extend(edge)

g.add_vertices(list(set(vertex)))  # add a list of unique vertices to the graph
g.add_edges(graph_edges)  # add the edges to the graph.

print('Communities:')
p = g.community_multilevel()
print(p)

# print("Components")
# d = g.components('WEAK')
# a = d.giant()
# print()
#
#
# print("Decompose")
# d = g.decompose('WEAK', 122222222, 7)
#
# print(d)

print("Degree distribution")
i = igraph.Graph.degree_distribution(g)
print(i)

print("Average clustering coefficient")
i = igraph.GraphBase.transitivity_avglocal_undirected(g)
print(i)

print("Vertices")
i = g.vcount()
print(i)

print("Edges")
i = g.ecount()
print(i)

print('Modularity')
q = g.modularity(p)
print(q)

print("Average degree distribution")
i = mean(g.degree())
print(i)

print("Clique number")
i = g.clique_number()
print(i)

print("Density")
i = g.density()
print(i)

print("Max degree")
max_degree = g.maxdegree()
print(max_degree)

print("Person with max degree")
print([v.attributes()['name'] for v in g.vs(_degree_eq=max_degree)])

print("Eigenvector centrality")
i = mean(g.eigenvector_centrality())  # look at a combination of a nodes edges and the edges of that nodes neighbors.
# cares if you are a hub, but it also cares how many hubs you are connected to
print(i)

# print("Betweenness")
# between = mean(g.betweenness())  # looks at all the shortest paths that pass through a particular node
# print(between)

g.vs["label"] = g.vs["name"]

# layout = g.layout("mds")
layout = g.layout("graphopt")
igraph.plot(g, layout=layout, bbox=(10000, 10000), vertex_size=40, edge_width=1, label_size=10)
