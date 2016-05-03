import sys
from numpy import random
from pamodel import make_graph
from socialradius import find_neighbors
from neighborhood import make_neighborhood
from scipy import optimize

# Initialize parameters of the model
m = 500
rad = 2
gamma = 0.25
w = [0.5,0.5,0.5,0.5]
wN = [0.5,0.5]
wC = [0.5,0.5]
n = 5
q = 2
t = 10

# Make social network using PA model
network = make_graph(m, q)

# Initialize bliss points
blissi = [random.normal() for x in xrange(m)]
blissN = random.normal()
blissC = random.normal()

# Initialize action history lists
ai = {}
ai[0] = blissi
aN = {}
aN[0] = blissN
aC = {}
aC[0] = blissC

# Find neighbors of distance at most r from each node
neighbors = {}
for i in range(m):
    neighbors[i] = find_neighbors(network, i, rad)

print neighbors
neighborhoods = {}
def run_round(timestep):
    # Recreate the neighborhood for each node
    for i in range(m):
        neighborhoods[i] = make_neighborhood(i, blissi, ai[timestep-1], neighbors, n)

    # Utility maximization for central authority
    def UC(x): 
        mean = sum(ai[timestep-1]) / m
        return (-wC[0] * (x - blissC) ** 2 - wC[1] * (x - mean) ** 2)
    aC[timestep] = optimize.fmin(lambda x: -UC(x), 0, disp=0)[0]
    
    # Utility maximization for non-central authority
    def UN(x): 
        mean = sum(ai[timestep-1]) / m
        return (-wN[0] * (x - blissN) ** 2 - wN[1] * (x - mean) ** 2 - gamma * (x-aC[timestep]) ** 2)
    aN[timestep] = optimize.fmin(lambda x: -UN(x), 0, disp=0)[0]

    # Utility maximization for each agent
    def UI(x, node):
        actions = []
        for neighbor in neighborhoods[node]:
            actions.append(ai[timestep-1][neighbor])
        mean_neighbors = sum(actions) / len(neighborhoods[node])
        return (-w[0] * (x - blissi[node]) ** 2 - w[1] * (x - mean_neighbors) ** 2 - w[2] * (x-aN[timestep]) ** 2 - w[3] * (x - aC[timestep]) ** 2)

    for i in range(m):
        if i == 0:
            ai[timestep] = []
        ai[timestep].append(optimize.fmin(lambda x: -UI(x, i),0, disp=0)[0])

    return

# Keep statistics
citizensmeans = []

for step in range(1,t):
    print "Step " + str(step)
    run_round(step)
    citizensmeans.append(sum(ai[step]) / m)

print "Citizens' Actions"
print "Mean = " + str(sum(citizensmeans) / t)
print "Min = " + str(min(citizensmeans))
print "Max = " + str(max(citizensmeans))
print "Central Authority's Actions"
print "Mean = " + str(sum(aC.values()) / t)
print "Min = " + str(min(aC.values()))
print "Max = " + str(max(aC.values()))
print "Noncentral Authority's Actions"
print "Mean = " + str(sum(aN.values()) / t)
print "Min = " + str(min(aN.values()))
print "Max = " + str(max(aN.values()))