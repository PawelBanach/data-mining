import copy
from itertools import combinations

import igraph
import pandas as pd
from lxml import etree

xml = 'dblp.xml'
#xml = 'displays.xml'

index = 0
authors_list = set()
graph_edges = []
title = ''
authorship = {}
print_communities_details = True
print_graph = False


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
        the_most_popular_journals.append([journal, len(journal_writers[journal]), journal_writers[journal]])

    the_most_popular_journals.sort(reverse=True, key=lambda x: x[0])
    print('The most popular journals: ')
    #print(the_most_popular_journals[:number])

    journals = []
    for i, journal in enumerate(the_most_popular_journals[:200]):
        journals.append(journal[0])
    df = pd.DataFrame(data=[journals])
    with open('authors.csv', 'a') as f:
        df.to_csv(f, sep=';', encoding='utf-8', header=None, index=False)

    authors_in_journals = []
    for i, author in enumerate(the_most_popular_journals[:200]):
        authors_in_journals.append(author[1])

    df1 = pd.DataFrame(data=[authors_in_journals])
    with open('authors.csv', 'a') as f1:
        df1.to_csv(f1, sep=';', encoding='utf-8', header=None, index=False)


def show_community_size(community):
    print('Community size: ')
    print(len(community))


def show_big_communities(communites, authors, authorship):
    ten_biggest_communities = get_biggest_communities(communites, 200)

    for i, community in enumerate(ten_biggest_communities):
        print('DETAILED INFO - COMMUNITY ', i)
        show_community_size(community)
        show_the_most_popular_journals(community, authors, authorship, 5)


authors = []
i = 0
max_authors = 0
for event, elem in etree.iterparse(source=xml, dtd_validation=False,
                                   load_dtd=True):  # ET.iterparse(xml, events=('start', 'end', 'start-ns', 'end-ns')):
    if i % 100000 == 0:
        print(i / 1000000, len(graph_edges), max_authors)
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

if print_communities_details:
    show_big_communities(p, graph_vertices, authorship)

