import pdb
import networkx as nx
import igraph
from lxml import etree
from igraph import Graph, mean
from itertools import combinations
import copy

xml = 'displays.xml'
# xml = 'dblp.xml'
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


authors = []
for event, elem in etree.iterparse(source=xml, dtd_validation=True,
                                   load_dtd=True):
    if event == 'end':
        if elem.tag == 'article':
            if len(authors) > 0:
                add_authors_to_list(authors)
                edges = combinations(authors, 2)
                add_edges_to_list(edges)
            authors = []
        if elem.tag == 'author' and elem.tag is not None:
            authors.append(elem.text.encode('utf-8'))
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

print("Vertices")
i = g.vcount()
print(i)

print("Edges")
i = g.ecount()
print(i)

print('Modularity')
q = g.modularity(p)
print(q)

print("Average clustering coefficient")
i = igraph.GraphBase.transitivity_avglocal_undirected(g)
print(i)

print("Degree distribution")
i = igraph.Graph.degree_distribution(g)
print(i)

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

print("Betweenness")
between = mean(g.betweenness())  # looks at all the shortest paths that pass through a particular node
print(between)

g.vs["label"] = g.vs["name"]

# layout = g.layout("mds")
layout = g.layout("graphopt")
igraph.plot(p, layout=layout, bbox=(10000, 10000), vertex_size=40, edge_width=1, label_size=10)
