# Function to make neighborhood

def make_neighborhood(v, blissi, actionsi, neighbors, n):
    neighborhood = []
    # Find distances of each neighbor's action to node's blissi
    actions = []
    for neighbor in neighbors:
        actions.append(actionsi[neighbor])
    distances = [(ind,abs(x - blissi[v])) for ind,x in enumerate(actions)]

    # Choose top n neighbors and add to neighborhood list
    sorteddist = sorted(distances, key=lambda x: x[1])

    for i in range(n):
        neighborhood.append(sorteddist[i][0])

    return neighborhood