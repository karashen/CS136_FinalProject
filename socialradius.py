# Function to locate nodes of radius r away from start node v
from collections import deque

def find_neighbors(graph, v, r):

    def bfs_dists(graph, start, r):
        print "bfs_dists" + str(start)
        # maintain a queue of paths
        queue = []

        distance = [-1 for x in xrange(len(graph))]
        distance[start] = 0

        # push the first path into the queue
        queue.append(start)
        
        while queue:
            # get the first path from the queue
            current = queue.pop(0)

            # enumerate all adjacent nodes push it into the queue
            adjacents = []
            for ind, el in enumerate(graph[current]):
                if el == 1:
                    adjacents.append(ind)
            for adjacent in adjacents:
                if distance[adjacent] == -1:
                    distance[adjacent] = distance[current] + 1
                    if distance[adjacent] > r:
                        return distance
                    queue.append(adjacent)
        return distance

    neighbors = []
    m = len(graph)
    distances = bfs_dists(graph, v, r)

    for ind, distance in enumerate(distances):
        if distance > 0 and distance <= r:
            neighbors.append(ind)
    # for node in range(m):
    #     if node != v:
    #         print "Finding path from " + str(v) + " to " + str(node)
    #         shortest = bfs_paths(graph, v, node)
    #         distance = len(shortest)
    #         if distance <= r:
    #             neighbors.append(node)

    return neighbors