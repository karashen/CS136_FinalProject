import random
import math
import matplotlib.pyplot as plt

numnodes = 500
q = 3

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

def calculate_degrees(graph):
	for i in xrange(numnodes):
		degrees[i] = sum(graph[i])

def mean(degrees):
	return float(sum(degrees))/float(numnodes)

def median(degrees):
	sorted_degrees = sorted(degrees)
	return float(degrees[249]+degrees[250])/2.

create_graph(graph)
calculate_degrees(graph)

# print degrees
# print "sum = " + str(mean(degrees))
# print "median = " + str(median(degrees))
# print "max = " + str(max(degrees))
# print "min = " + str(min(degrees))

def distribution(degrees):
	distr = [0.0 for node in xrange(max(degrees))]
	for i in xrange(max(degrees)):
		distr[i] = float(degrees.count(i))/float(numnodes)
	return distr

def poisson(degrees):
  distr = [0.0 for node in xrange(max(degrees))]
  for i in xrange(max(degrees)):
      distr[i] = math.exp(-1. * mean(degrees)) * ( math.pow(mean(degrees), i ) / float(math.factorial(i)) )
  return distr

plt.plot(range(max(degrees)), distribution(degrees), 'r-')
# plt.plot(range(max(degrees)), poisson(degrees), 'b-')
plt.xscale('log')
plt.yscale('log')
plt.xlim([3, max(degrees)+1])
plt.show()