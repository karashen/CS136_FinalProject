# Function to generate a small world graph
import random
import math
import matplotlib.pyplot as plt

def make_graph(numnodes, q):

    graph = [[0 for node in xrange(numnodes)] for node in xrange(numnodes)]
    degrees = [0 for node in xrange(numnodes)]

    def init_clique(graph, q):
        for i in xrange(2*q + 1):
            for j in xrange(2*q + 1):
                if i != j:
                    graph[i][j] = 1

    def add_vertex(graph, i):
        counter = 0
        while counter < q:
            vertex = random.randint(0, i)
            if vertex != i and graph[i][vertex] == 0 and graph[vertex][i] == 0:
                graph[i][vertex] = 1
                graph[vertex][i] = 1
                counter += 1

    def create_graph(graph):
        init_clique(graph, q)
        for i in xrange(2*q + 2, numnodes):
            add_vertex(graph, i)
        return graph

    return create_graph(graph)