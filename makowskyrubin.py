import sys
from pamodel import make_graph

# Initialize parameters of the model
m = 10
r = 5
gamma = 0
w1 = 0.5
w2 = 0.5
w3 = 0.5
w4 = 0.5
wN1 = 0.5
wN2 = 0.5
wC1 = 0.5
wC2 = 0.5
n = 5
q = 1

# Make social network using PA model
network = make_graph(m, q)

