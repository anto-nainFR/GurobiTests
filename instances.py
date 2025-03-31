import numpy as np
import sys

# fonction qui écrit l'instance dans un autre fichier
def writeInstance(filename, nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha):
    with open(filename, 'w') as f:
        f.write(f"{nnodes} {p} {nbS}\n")
        
        for i in range(nnodes):
            for j in range(nnodes):
                f.write(f"{int(distances[i,j])} ")
                # f.write(f"{distances[i,j]} ")
            f.write("\n")

        for i in range(nnodes):
            for s in range(nbS):
                f.write(f"{int(capacity[i,s]*1.5)} ")
            f.write("\n")
        
        for i in range(nnodes):
            for s in range(nbS):
                f.write(f"{int(demand[i,s])} ")
            f.write("\n")

        for i in range(nnodes):
            for s in range(nbS):
                f.write(f"{int(stratum[i,s])} ")
            f.write("\n")

        for i in range(nnodes):
            for s in range(nbS):
                f.write(f"{int(stratumCenter[i,s])} ")
            f.write("\n")
        
        for s in range(nbS):
            f.write(f"{alpha[s]}\n")


def lectureInstances(filename):
    try:
        with open(filename, 'r') as f:            
            nnodes, p, nbS = map(int, f.readline().split())
            
            distances = np.zeros((nnodes, nnodes))
            maxDist = 0.0
            for i in range(nnodes):
                row = list(map(float, f.readline().split()))
                distances[i, :] = row
                maxDist = max(maxDist, max(row))
            
            capacity = np.zeros((nnodes, nbS))
            for i in range(nnodes):
                capacity[i, :] = list(map(float, f.readline().split()))
            
            demand = np.zeros((nnodes, nbS))
            for i in range(nnodes):
                demand[i, :] = list(map(float, f.readline().split()))
            
            stratum = np.zeros((nnodes, nbS))
            for i in range(nnodes):
                stratum[i, :] = list(map(float, f.readline().split()))
            
            stratumCenter = np.zeros((nnodes, nbS))
            for i in range(nnodes):
                stratumCenter[i, :] = list(map(float, f.readline().split()))

            alpha = np.zeros(nbS)
            #récupération de l'alpha pour chaque strate
            for s in range(nbS):
                alpha[s] = float(f.readline())
            
        return nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha
    except FileNotFoundError:
        return None
    
if __name__ == "__main__":
    assert(len(sys.argv) == 3), "Usage: python solver.py <filename> <filename_out>"

    # lecture de l'instance
    nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha = lectureInstances(sys.argv[1])

    writeInstance(sys.argv[2], nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha)