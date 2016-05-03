from __future__ import division

# Function to generate a small world graph
import random
import math
import matplotlib.pyplot as plt

def make_graph(numnodes, q):

    graph = [[0 for node in xrange(numnodes)] for node in xrange(numnodes)]
    degrees = [0 for node in xrange(numnodes)]
    vertices = []

    def init_clique(graph, q):
        for i in xrange(2*q + 1):
            for j in xrange(2*q + 1):
                if i != j:
                    graph[i][j] = 1
            vertices.append(i)
            degrees[i] = 2*q

    def add_vertex(graph, i, q):
        probs = [x / sum(degrees) for x in degrees]
        for t in range(q):

            def weighted_choice(choices):
               total = sum(w for c, w in choices)
               r = random.uniform(0, total)
               upto = 0
               for c, w in choices:
                  if upto + w >= r:
                     return c
                  upto += w

            distribution = [(x,y) for x, y in zip(vertices, probs)]
            neighbor = weighted_choice(distribution)
            graph[i][neighbor] = 1
            graph[neighbor][i] = 1
            degrees[i] += 1
            degrees[neighbor] += 1
        vertices.append(i)

    def create_graph(graph):
        init_clique(graph, q)
        for i in xrange(2*q + 1, numnodes):
            print "Adding vertex" + str(i)
            add_vertex(graph, i, q)
        return graph

    return create_graph(graph)