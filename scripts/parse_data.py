import igraph
from lxml import etree
from igraph import Graph, mean
from itertools import combinations
import copy
import matplotlib.pyplot as plt
import numpy as np

xml = 'dblp.xml'
# xml = 'displays.xml'

index = 0
authors_list = set()
authors_in_the_biggest_communites = set()
graph_edges = []
title = ''
authorship = {}
print_communities_details = True
print_graph = False


def print_graph_details(graph, communities=None):
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
    degree = igraph.Graph.degree_distribution(graph)
    bins = degree._bins
    plot_histogram(bins)

    print("Average clustering coefficient")
    i = igraph.GraphBase.transitivity_avglocal_undirected(graph)
    print(i)

    print("Vertices")
    i = graph.vcount()
    print(i)

    print("Edges")
    i = graph.ecount()
    print(i)

    if communities:
        print('Modularity')
        q = graph.modularity(communities)
        print(q)

    print("Average degree distribution")
    i = mean(graph.degree())
    print(i)

    print("Clique number")
    i = graph.clique_number()
    print(i)

    print("Density")
    i = graph.density()
    print(i)

    print("Max degree")
    max_degree = graph.maxdegree()
    print(max_degree)

    print("Person with max degree")
    print([v.attributes()['name'] for v in graph.vs(_degree_eq=max_degree)])

    print("Eigenvector centrality")
    i = mean(
        graph.eigenvector_centrality())  # look at a combination of a nodes edges and the edges of that nodes neighbors.
    # cares if you are a hub, but it also cares how many hubs you are connected to
    print(i)

    # print("Betweenness")
    # between = mean(g.betweenness())  # looks at all the shortest paths that pass through a particular node
    # print(between)


def plot_histogram(x):
    plt.bar(np.arange(100), x[:100], width=1)
    plt.ylabel('Degree distribution')
    plt.show()


def add_authors_to_list(new_authors):
    for author in new_authors:
        authors_list.add(author)


def add_edges_to_list(new_edges):
    for edge in new_edges:
        graph_edges.append(copy.deepcopy(edge))


def add_to_journals_dictionary(journal, authors):
    for author in authors:
        if author not in authorship:
            authorship[author] = set()
        authorship[author].add(journal)


# number -> how many biggest communities you want
def get_biggest_communities(communities, number):
    list_communities = list(communities)
    list_communities.sort(reverse=True, key=len)
    return list_communities[:number]

# number -> how many the most popular journals you want
def show_the_most_popular_journals(community, authors, authorship, number):
    journal_writers = {}
    for member in community:
        author = authors[member]
        for journal in authorship[author]:
            if journal not in journal_writers:
                journal_writers[journal] = []
            journal_writers[journal].append(author)

    the_most_popular_journals = []
    for journal in journal_writers:
        the_most_popular_journals.append([journal, len(journal_writers[journal])])

    the_most_popular_journals.sort(reverse=True, key=lambda x: x[1])
    print('The most popular journals: ')
    print(the_most_popular_journals[:number])


def show_community_size(community):
    print('Community size: ')
    print(len(community))


def show_big_communities(g, communites, authors, authorship):
    ten_biggest_communities = get_biggest_communities(communites, 10)

    for i, community in enumerate(ten_biggest_communities):
        print('DETAILED INFO - COMMUNITY ', i)
        show_community_size(community)
        show_the_most_popular_journals(community, authors, authorship, 10)
        community_graph = g.subgraph(community)
        print_graph_details(community_graph)


authors = []
i = 0
max_authors = 0
journal = ''
for event, elem in etree.iterparse(source=xml, dtd_validation=False,
                                   load_dtd=True):  # ET.iterparse(xml, events=('start', 'end', 'start-ns', 'end-ns')):
    if i % 100000 == 0:
        print(i/1000000, len(graph_edges), max_authors)
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
                    if len(authors) > 200:  # Article with more than 200 authors
                        print(len(authors), title)
                    add_authors_to_list(authors)
                    edges = combinations(authors, 2)
                    add_edges_to_list(edges)
                    add_to_journals_dictionary(journal, authors)
                else:
                    authors = []
            authors = []
        if elem.tag == 'author' and elem.tag is not None:
            authors.append(elem.text)
        if elem.tag == 'journal' and elem.tag is not None:
            journal = elem.text

    elem.clear()

g = igraph.Graph()

vertex = []
for edge in graph_edges:
    vertex.extend(edge)
graph_vertices = list(set(vertex))
g.add_vertices(graph_vertices)  # add a list of unique vertices to the graph
g.add_edges(graph_edges)  # add the edges to the graph.

print('Communities:')
p = g.community_multilevel()
print(p)
print('Number of communities')
print(len(p))

if print_communities_details:
    show_big_communities(g, p, graph_vertices, authorship)

print_graph_details(g, p)

if print_graph:
    g.vs["label"] = g.vs["name"]
    # layout = g.layout("mds")
    layout = g.layout("graphopt")
    igraph.plot(g, layout=layout, bbox=(10000, 10000), vertex_size=40, edge_width=2, label_size=10)
