import sys
from numpy import random
from pamodel import make_graph
from socialradius import find_neighbors
from neighborhood import make_neighborhood
from scipy import optimize

# Initialize parameters of the model
m = 800
rad = 3
gamma = 0.5
phi = 0.5
eps = 0.00000001
w = [0.5,0.5,0.5,0.5,1.0,1.0]
wN = [0.5,0.5,0.5]
wC = [0.5,0.5]
wM1 = [0.5,0.5]
wM2 = [0.5,0.5]
n = 10
q = 5
t = 30

# Make social network using PA model
network = make_graph(m, q)

# Initialize bliss points
blissi = [random.normal() for x in xrange(m)]
blissN = random.normal()
blissC = random.normal()
blissM1 = random.normal(-1)
blissM2 = random.normal(1)

# Initialize action history lists
ai = {}
ai[0] = blissi
aN = {}
aN[0] = blissN
aC = {}
aC[0] = blissC
aM1 = {}
aM1[0] = blissM1
aM2 = {}
aM2[0] = blissM2

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
        mediamean = (aM1[timestep-1] + aM2[timestep-1]) / 2
        return (-wC[0] * (x - blissC) ** 2 - wC[1] * (x - mean) ** 2 - phi * (x - mediamean) ** 2)
        # return (-wC[0] * (x - blissC) ** 2 - wC[1] * (x - mean) ** 2)
    aC[timestep] = optimize.fmin(lambda x: -UC(x), 0, disp=0)[0]
    
    # Utility maximization for non-central authority
    def UN(x): 
        mean = sum(ai[timestep-1]) / m
        mediamean = (aM1[timestep-1] + aM2[timestep-1]) / 2
        return (-wN[0] * (x - blissN) ** 2 - wN[1] * (x - mean) ** 2 - gamma * (x-aC[timestep]) ** 2 - wN[2] * (x - mediamean) ** 2)
    aN[timestep] = optimize.fmin(lambda x: -UN(x), 0, disp=0)[0]

    # Utility maximization for each agent
    def UI(x, node):
        actions = []
        for neighbor in neighborhoods[node]:
            actions.append(ai[timestep-1][neighbor])
        mean_neighbors = sum(actions) / len(neighborhoods[node])
        return (-w[0] * (x - blissi[node]) ** 2 - w[1] * (x - mean_neighbors) ** 2 - w[2] * (x-aN[timestep]) ** 2 - w[3] * (x - aC[timestep]) ** 2 - w[4] * (x-aM1[timestep-1]) - w[5] * (x-aM2[timestep-1]))

    for i in range(m):
        if i == 0:
            ai[timestep] = []
        ai[timestep].append(optimize.fmin(lambda x: -UI(x, i),0, disp=0)[0])
    
    # Utility maximization for each media agent
    def UM1(x): 
        mean = sum(ai[timestep]) / m
        return (-wM1[0] * (x - blissM1) ** 2 - wM1[1] * (x - mean) ** 2)
    aM1[timestep] = optimize.fmin(lambda x: -UM1(x), 0, disp=0)[0]

    def UM2(x): 
        mean = sum(ai[timestep]) / m
        return (-wM2[0] * (x - blissM2) ** 2 - wM2[1] * (x - mean) ** 2)
    aM2[timestep] = optimize.fmin(lambda x: -UM2(x), 0, disp=0)[0]

    return

# Keep statistics
citizensmeans = [sum(ai[0]) / m]
equilibrium_timestep = 100

for step in range(1,t+1):
    print "Step " + str(step)
    run_round(step)
    citizensmeans.append(sum(ai[step]) / m)
    difference = citizensmeans[step] - citizensmeans[step-1]
    print str(citizensmeans[step])
    print str(citizensmeans[step-1])
    print str(difference)
    if abs(difference) <= eps:
        equilibrium_timestep = step
        break;

end = min(t, step)
citizen_mean = sum(citizensmeans) / end
central_mean = sum(aC.values()) / end
noncentral_mean = sum(aN.values()) / end

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
print "Media 1's Actions"
print "Mean = " + str(sum(aM1.values()) / t)
print "Min = " + str(min(aM1.values()))
print "Max = " + str(max(aM1.values()))
print "Media 2's Actions"
print "Mean = " + str(sum(aM2.values()) / t)
print "Min = " + str(min(aM2.values()))
print "Max = " + str(max(aM2.values()))

def authority_citizen_discepancy():
    discrepancies = [0 for x in xrange(2)]
    discrepancies[0] = abs(aC[end] - (sum(ai[end]) / m))
    discrepancies[1] = abs(aN[end] - (sum(ai[end]) / m))
    return discrepancies

def preference_falsification():
    falsifications = [0 for x in xrange(5)]
    falsifications[0] = abs((sum(ai[end]) / m) - (sum(ai[0]) / m))
    falsifications[1] = abs(aC[end] - aC[0])
    falsifications[2] = abs(aN[end] - aN[0])
    falsifications[3] = abs(aM1[end] - aN[0])
    falsifications[4] = abs(aM2[end] - aN[0])
    return falsifications

print "equilibrium_timestep: " + str(equilibrium_timestep)
print "authority_citizen_discrepancy: " + str(authority_citizen_discepancy())
print "preference_falsification: " + str(preference_falsification())
