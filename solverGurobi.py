import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pprint as pprint
import sys


def setParameters(modele):
    modele.setParam('Threads', 1)
    # modele.setParam("OutputFlag", 0)  # Désactive complètement la sortie
    modele.setParam("TimeLimit", 3600)  # Limite de temps en secondes
    modele.setParam("MIPGap", 1e-10)  # Tolérance sur l'écart MIP

    # model.setParam("SolutionLimit", 1)  # Arrête après 1 solution faisable trouvée
    # modele.setParam("Presolve", 0)
    return modele

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
                f.write(f"{int(capacity[i,s]/2)} ")
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

def displayInstances(maxDist, distances, capacity, demand, stratum, stratumCenter):
    print("maxDist = ", maxDist)
    print("distances = \n", distances)
    print("capacity = \n", capacity)
    print("demand = \n", demand)
    print("stratum = \n", stratum)
    print("stratumCenter = \n", stratumCenter)


def createModel(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction):

    modele = gp.Model("pcentre strates,pannes,capacités")

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, nnodes, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(nnodes): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[i, s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    x = modele.addVars(nbVariables, vtype=GRB.BINARY, name="x") # premier niveau
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau
    y = modele.addVars(nnodes, vtype=GRB.BINARY, name="y")      # assignation des centres

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    # Fonction objectif

    if objectiveFunction == "AB":
        modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "B":
        modele.setObjective(gp.quicksum(Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "A":
        modele.setObjective(gp.quicksum(As[s] for s in range(nbS)), GRB.MINIMIZE)

    # Contraintes
    # contraintes nombres de centres
    expr = gp.LinExpr()
    for j in range(nnodes):
        expr += y[j]
    modele.addConstr(expr == p, "nbCentres")


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(x[mapping[s,j,i]] <= y[j], f"assignationCentre1_{s}_{i}_{j}")
                    modele.addConstr(w[mapping[s,j,i]] <= y[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(x[mapping[s,j,i]] + w[mapping[s,j,i]]<= 1, f"assignationCentre2_{s}_{i}_{j}")


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]] - distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[j,s] *y[j])

    return modele, x, w, y, As, Bs


def createModel_surcharge(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha):

    modele = gp.Model("pcentre strates,pannes,capacités")

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, nnodes, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(nnodes): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[i, s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    x = modele.addVars(nbVariables, vtype=GRB.BINARY, name="x") # premier niveau
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau
    y = modele.addVars(nnodes, vtype=GRB.BINARY, name="y")      # assignation des centres

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    # Fonction objectif

    if objectiveFunction == "AB":
        modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "B":
        modele.setObjective(gp.quicksum(Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "A":
        modele.setObjective(gp.quicksum(As[s] for s in range(nbS)), GRB.MINIMIZE)

    # Contraintes
    # contraintes nombres de centres
    expr = gp.LinExpr()
    for j in range(nnodes):
        expr += y[j]
    modele.addConstr(expr == p, "nbCentres")


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(x[mapping[s,j,i]] <= y[j], f"assignationCentre1_{s}_{i}_{j}")
                    modele.addConstr(w[mapping[s,j,i]] <= y[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(x[mapping[s,j,i]] + w[mapping[s,j,i]]<= 1, f"assignationCentre2_{s}_{i}_{j}")


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]] - distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)

    # for s in range(nbS):
    #     for j in range(nnodes):
    #         if stratumCenter[j,s] == 1:
    #             expr = gp.LinExpr()
    #             for i in range(nnodes):
    #                 if stratum[i,s] == 1:
    #                     expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
    #             modele.addConstr( expr <= capacity[j,s] *y[j])

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[j,s] *y[j])

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[j,s] *y[j])

    return modele, x, w, y, As, Bs

def createModel_surcharge_pmedian(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha):

    modele = gp.Model("pcentre strates,pannes,capacités")

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, nnodes, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(nnodes): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[i, s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    x = modele.addVars(nbVariables, vtype=GRB.BINARY, name="x") # premier niveau
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau
    y = modele.addVars(nnodes, vtype=GRB.BINARY, name="y")      # assignation des centres

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    # Fonction objectif

    if objectiveFunction == "AB":
        modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "B":
        modele.setObjective(gp.quicksum(Bs[s] for s in range(nbS)), GRB.MINIMIZE)
    elif objectiveFunction == "A":
        modele.setObjective(gp.quicksum(As[s] for s in range(nbS)), GRB.MINIMIZE)

    # Contraintes
    # contraintes nombres de centres
    expr = gp.LinExpr()
    for j in range(nnodes):
        expr += y[j]
    modele.addConstr(expr == p, "nbCentres")


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(x[mapping[s,j,i]] <= y[j], f"assignationCentre1_{s}_{i}_{j}")
                    modele.addConstr(w[mapping[s,j,i]] <= y[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(x[mapping[s,j,i]] + w[mapping[s,j,i]]<= 1, f"assignationCentre2_{s}_{i}_{j}")


    # for s in range(nbS):
    #     for i in range(nnodes):
    #         if stratum[i,s] == 1:
    #             expr = gp.LinExpr()
    #             for j in range(nnodes):
    #                 if stratumCenter[j,s] == 1:
    #                     expr += distances[i,j] * x[mapping[s,j,i]]
    #             modele.addConstr(expr <= As[s])

    # for s in range(nbS):
    #     for i in range(nnodes):
    #         if stratum[i,s] == 1:
    #             expr = gp.LinExpr()
    #             for j in range(nnodes):
    #                 if stratumCenter[j,s] == 1:
    #                     expr += distances[i,j] * w[mapping[s,j,i]]
    #             modele.addConstr(expr <= Bs[s])

    nbPerS = np.zeros(nbS)
    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                nbPerS[s] += 1
    print("Nombre de client par strate : ",nbPerS)

    for s in range(nbS):
        expr = gp.LinExpr()
        for i in range(nnodes):
            if stratum[i,s] == 1:
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]]
        modele.addConstr(As[s] == expr / nbPerS[s])

    for s in range(nbS):
        expr = gp.LinExpr()
        for i in range(nnodes):
            if stratum[i,s] == 1:
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * w[mapping[s,j,i]]
        modele.addConstr(Bs[s] == expr / nbPerS[s])

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]] - distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)


    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[j,s] *y[j])

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[j,s] *y[j])

    return modele, x, w, y, As, Bs




############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################




if __name__ == "__main__":
    assert(len(sys.argv) == 4), "Usage: python solver.py <filename> <objectiveFunction> <csv>"
    assert(sys.argv[2] == "AB" or sys.argv[2] == "A" or sys.argv[2] == "B"), "objectiveFunction must be AB, A or B"
    
    objectiveFunction = sys.argv[2]
    csv_file = sys.argv[3]

    # lecture de l'instance
    nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha = lectureInstances(sys.argv[1])
    

    print("nnodes = ", nnodes)
    print("p = ", p)
    print("nbS = ", nbS)

    # somme des demandes de la première strate
    total_demande = 0
    total_capacite = 0
    id = 0
    for i in range(nnodes):
        if stratum[i,0] == 1:
            total_demande += demand[i,0]
        if stratumCenter[i,0] == 1:
            total_capacite += capacity[i,0]
            id += 1
    print("Somme des demandes de la première strate : ", total_demande)
    print("Somme des capacités de la première strate : ", total_capacite)
    print("Moyenne des capacités de la première strate : ", total_capacite/id)
    print("facteur capacite/demande/id : ", total_capacite/id/total_demande)
    print("facteur capacite/demande : ", total_capacite/total_demande)
    print("id : ", id)
    

    pprint.pprint(alpha)

    # for s in range(nbS):
    #     alpha[s] = 0.1
    # writeInstance(f"instancesSurcharges/alpha0_1/{sys.argv[1]}", nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha)

    # for s in range(nbS):
    #     alpha[s] = 0.2
    # writeInstance(f"instancesSurcharges/alpha0_2/{sys.argv[1]}", nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha)

    # for s in range(nbS):
    #     alpha[s] = 0.3
    # writeInstance(f"instancesSurcharges/alpha0_3/{sys.argv[1]}", nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha)

    # # aléatoire alpha entre 0 et 0.3 jusqu'à 2 décimales près
    # for s in range(nbS):
    #     alpha[s] = round(np.random.uniform(0, 0.3), 2)
    # writeInstance(f"instancesSurcharges/alpha_aleatoire/{sys.argv[1]}", nnodes, p, nbS, distances, capacity, demand, stratum, stratumCenter, alpha)


    # affichage de l'instances
    # displayInstances(maxDist, distances, capacity, demand, stratum, stratumCenter)

    # création du modèle
    modele, x, w, y, As, Bs = createModel_surcharge(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha)
    # modele, x, w, y, As, Bs = createModel_surcharge_pmedian(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha)
    # modele, x, w, y, As, Bs = createModel_test(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction)
    # modele, x, w, y, As, Bs = createModel(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction)
    

    # paramétrage du modèle
    modele = setParameters(modele)

    # résolution du modèle
    modele.optimize()


    # résultats
    if modele.status == GRB.INFEASIBLE:
        print("Problème infaisable")
        with open(csv_file, "a") as f:
            f.write(f"{sys.argv[1]}\t{objectiveFunction}\tINFEASIBLE\n")
    elif modele.status == GRB.UNBOUNDED:
        print("Problème non borné")
        with open(csv_file, "a") as f:
            f.write(f"{sys.argv[1]}\t{objectiveFunction}\tUNBOUNDED\n") 
    elif modele.status != GRB.OPTIMAL and modele.status != GRB.SUBOPTIMAL and modele.status != GRB.TIME_LIMIT:
        print("Problème non résolu")
        

    # sauvegarde de la solution
    # modele.write("solution.sol")

    print(f"Il y a eu {modele.NodeCount} noeuds explorés")
    print(f"Temps de calcul : {modele.Runtime} secondes")
    # print(f"Gap : {modele.MIPGap * 100}%")

    # print(f"Borne inférieure : {modele.ObjBound}")
    # print(f"Borne supérieure : {modele.ObjVal}")

    if modele.status == GRB.OPTIMAL:
        print("Solution optimale")
    else:
        print("Solution faisable ou suboptimal : ", modele.SolCount, " solutions trouvées")


    val_x = modele.getAttr('X', x)
    val_w = modele.getAttr('X', w)

    print("VALEUR DE Y :")
    val_y = modele.getAttr('X', y)
    for i in range(nnodes):
        if val_y[i] == 1:
            print(f"y[{i}] = {val_y[i]}")

    print("VALEUR DE X :")
    id = 0
    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[j,s] == 1 and stratumCenter[i,s] == 1:
                    if val_x[id] == 1:
                        print(f"x[{s},{i},{j}] = {val_x[id]} | distance = {distances[i,j]} | demande = {demand[j,s]} | capacité = {capacity[i,s]}")
                    id += 1
    print("VALEUR DE W :")
    id = 0
    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[j,s] == 1 and stratumCenter[i,s] == 1:
                    if val_w[id] == 1:
                        print(f"w[{s},{i},{j}] = {val_w[id]} | distance = {distances[i,j]} | demande = {demand[j,s]} | capacité = {capacity[i,s]}")
                    id += 1


    # calcul des valeurs de As et Bs en fonction des x et w
    id = 0
    val_As = np.zeros(nbS)
    val_Bs = np.zeros(nbS)
    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[j,s] == 1 and stratumCenter[i,s] == 1:
                    if val_x[id] == 1 and val_As[s] < distances[i,j]:
                        val_As[s] = distances[i,j]
                    if val_w[id] == 1 and val_Bs[s] < distances[i,j]:
                        val_Bs[s] = distances[i,j]
                    id += 1

    val_As2 = np.zeros(nbS)
    val_Bs2 = np.zeros(nbS)

    nbPerS = np.zeros(nbS)
    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                nbPerS[s] += 1

    pprint.pprint(nbPerS)

    # id = 0
    # for s in range(nbS):
    #     expr = 0
    #     for i in range(nnodes):
    #         if stratum[i,s] == 1:
    #             for j in range(nnodes):
    #                 if stratumCenter[j,s] == 1:
    #                     expr += distances[i,j] * val_x[id]
    #                     id += 1
    #     val_As2[s] = round(expr / nbPerS[s], 2)

    id = 0
    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[j,s] == 1 and stratumCenter[i,s] == 1:
                    if val_x[id] == 1 :
                        val_As2[s] += distances[i,j]
                    if val_w[id] == 1 :
                        val_Bs2[s] += distances[i,j]
                    id += 1

    for s in range(nbS):
        val_As2[s] = round(val_As2[s] / nbPerS[s], 2)
        val_Bs2[s] = round(val_Bs2[s] / nbPerS[s], 2)
    

    # id = 0
    # for s in range(nbS):
    #     expr = 0
    #     for i in range(nnodes):
    #         if stratum[i,s] == 1:
    #             for j in range(nnodes):
    #                 if stratumCenter[j,s] == 1:
    #                     expr += distances[i,j] * val_w[id]
    #                     id += 1
    #     val_Bs2[s] = round(expr / nbPerS[s], 2)



    print("VALEUR DE As :")
    pprint.pprint(val_As)

    print("VALEUR DE Bs :")
    pprint.pprint(val_Bs)

    print("VALEUR DE As2 :")
    pprint.pprint(val_As2)

    print("VALEUR DE Bs2 :")
    pprint.pprint(val_Bs2)

    print("Somme des As : ", sum(val_As))
    print("Somme des Bs : ", sum(val_Bs))
    print("Somme des As + Bs : ", sum(val_As) + sum(val_Bs))
    print("Somme des As2 : ", sum(val_As2))
    print("Somme des Bs2 : ", sum(val_Bs2))
    print("Somme des As2 + Bs2 : ", round(sum(val_As2) + sum(val_Bs2), 2))
    
    if objectiveFunction == "AB":
        objVal = sum(val_As) + sum(val_Bs)
        print("Valeur de la fonction objectif : ", sum(val_As) + sum(val_Bs))
    elif objectiveFunction == "A":
        objVal = sum(val_As)
        print("Valeur de la fonction objectif : ", sum(val_As))
    elif objectiveFunction == "B":
        objVal = sum(val_Bs)
        print("Valeur de la fonction objectif : ", sum(val_Bs))



    # écriture des résultats dans un fichier au format csv (chaque ligne une instance)
    
    if modele.status == GRB.OPTIMAL or modele.status == GRB.SUBOPTIMAL:
        with open(csv_file, "a") as f:
            f.write(f"{sys.argv[1]}\t{objectiveFunction}\t{objVal}\t{modele.Runtime}\t{modele.NodeCount}\n")