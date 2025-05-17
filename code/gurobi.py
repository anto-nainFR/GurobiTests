import numpy as np
import gurobipy as gp
from gurobipy import GRB


def setParameters(modele):
    modele.setParam('Threads', 1)
    modele.setParam("OutputFlag", 0)  # Désactive complètement la sortie
    modele.setParam("TimeLimit", 3600)  # Limite de temps en secondes
    modele.setParam("MIPGap", 1e-10)  # Tolérance sur l'écart MIP

    modele.setParam("MIPFocus",1)
    modele.setParam("MIPSepCuts",0)
    modele.setParam("Method",1)

    # modele.setParam("SolutionLimit", 1)  # Arrête après 1 solution faisable trouvée
    # modele.setParam("Presolve", 0)
    return modele


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


def createModel_surcharge(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha, method):

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

    if method == "LP" :
        # Variables de décision
        x = modele.addVars(nbVariables,  lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name="x") # premier niveau
        w = modele.addVars(nbVariables,  lb=0.0, ub=1, vtype=GRB.CONTINUOUS, name="w") # second niveau
        y = modele.addVars(nnodes,  lb=0.0, ub=1,vtype=GRB.CONTINUOUS, name="y")      # assignation des centres
    elif method == "MIP" :
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
    modele.addConstr(expr <= p, "nbCentres")


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


def ajoutContraintes(modele, x, w, y, As, Bs, nnodes, nbS, stratum, stratumCenter, distances, demand, capacity, alpha):
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

    # La capacité totale de chaque strate doit être supérieure à la somme des demandes

    # calcul sommes des demandes de chaque strate
    sommeDemandes = np.zeros(nbS)
    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                sommeDemandes[s] += demand[i,s]
    
    # ajout de la contrainte
    for s in range(nbS):
        expr = gp.LinExpr()
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr += capacity[j,s] * y[j]
        modele.addConstr(expr >= sommeDemandes[s], f"capacite_{s}")

    # La capacité totale de chaque strate (main + backup) doit être supérieure à 2x la somme des demandes
    for s in range(nbS):
        expr = gp.LinExpr()
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr += (capacity[j,s] * y[j]) * (1 + alpha[s])
        modele.addConstr(expr >= 2 * sommeDemandes[s], f"capacite_{s}_surcharge")

    # Il doit y avoir au moins 2 centres ouverts par strate
    for s in range(nbS):
        expr = gp.LinExpr()
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr += y[j]
        modele.addConstr(expr >= 2, f"nbCentres_{s}")

    return modele



def createModel_surchargeYD(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD):

    nbVar = 0
    nbConst = 0

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

    # x = modele.addVars(nbVariables, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="x") # premier niveau
    # w = modele.addVars(nbVariables, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="w") # second niveau
    # y = modele.addVars(nnodes, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="y")      # assignation des centres

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    nbVar = 2 * nbVariables + 2 * nbS

    # Fonction objectif

    modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(x[mapping[s,j,i]] <= yD[j], f"assignationCentre1_{s}_{i}_{j}")
                    modele.addConstr(w[mapping[s,j,i]] <= yD[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(x[mapping[s,j,i]] + w[mapping[s,j,i]]<= 1, f"assignationCentre2_{s}_{i}_{j}")
                    nbConst += 3

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]] - distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)
                nbConst += 1

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[j,s] *yD[j])
                nbConst += 1

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[j,s] *yD[j])
                nbConst += 1

    return modele, x, w, As, Bs, nbVar, nbConst

def createModel_surchargeYDReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD):

    nbVar = 0
    nbConst = 0

    modele = gp.Model("pcentre strates,pannes,capacités")

    mappingCentre = np.zeros(p, dtype=int)
    id = 0
    for i in range(nnodes):
        if yD[i] == True:
            mappingCentre[id] = i
            id += 1

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, p, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(p): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[mappingCentre[i], s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    x = modele.addVars(nbVariables, vtype=GRB.BINARY, name="x") # premier niveau
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau

    # x = modele.addVars(nbVariables, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="x") # premier niveau
    # w = modele.addVars(nbVariables, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="w") # second niveau

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    nbVar = 2 * nbVariables + 2 * nbS

    # Fonction objectif
    modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(p):
                if stratum[i,s] == 1 and stratumCenter[mappingCentre[j],s] == 1:
                    # modele.addConstr(x[mapping[s,j,i]] <= y[j], f"assignationCentre1_{s}_{i}_{j}")
                    # modele.addConstr(w[mapping[s,j,i]] <= y[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(x[mapping[s,j,i]] + w[mapping[s,j,i]] <= 1, f"assignationCentre2_{s}_{i}_{j}")
                    nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * x[mapping[s,j,i]] - distances[i,mappingCentre[j]] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)
                nbConst += 1

    for s in range(nbS):
        for j in range(p):
            if stratumCenter[mappingCentre[j],s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[mappingCentre[j],s])
                nbConst += 1

    for s in range(nbS):
        for j in range(p):
            if stratumCenter[mappingCentre[j],s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[mappingCentre[j],s])
                nbConst += 1

    return modele, x, w, As, Bs, nbVar, nbConst

def createModel_surchargeYDAssignationX(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD):

    nbVar = 0
    nbConst = 0

    yD1 = np.zeros(nnodes)
    for i in range(nnodes):
        if yD[i] == True:
            yD1[i] = 1
        else:
            yD1[i] = 0

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

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")

    nbVar = nbVariables + nbS
    # Fonction objectif

    modele.setObjective(gp.quicksum(As[s] for s in range(nbS)), GRB.MINIMIZE)
    
    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1
    
    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(x[mapping[s,j,i]] <= yD1[j], f"assignationCentre1_{s}_{i}_{j}")
                    nbConst += 1

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[j,s] *yD1[j])
                nbConst += 1


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    return modele, x, As, nbVar, nbConst


def createModel_surchargeYDAssignationW(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD, xD):

    nbVar = 0
    nbConst = 0

    yD1 = np.zeros(nnodes)
    for i in range(nnodes):
        if yD[i] == True:
            yD1[i] = 1
        else:
            yD1[i] = 0

    modele = gp.Model("pcentre strates,pannes,capacités")

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, nnodes, nnodes), dtype=int)
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
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau

    As= modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs= modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    nbVar = nbVariables + 2 * nbS

    modele.setObjective(gp.quicksum(As[s]+Bs[s] for s in range(nbS)), GRB.MINIMIZE)


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(nnodes):
                if stratum[i,s] == 1 and stratumCenter[j,s] == 1:
                    modele.addConstr(w[mapping[s,j,i]] <= yD1[j], f"assignationCentre2_{s}_{i}_{j}")
                    modele.addConstr(xD[mapping[s,j,i]] + w[mapping[s,j,i]]<= 1, f"assignationCentre2_{s}_{i}_{j}")
                    nbConst += 2

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * xD[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(nnodes):
                    if stratumCenter[j,s] == 1:
                        expr += distances[i,j] * xD[mapping[s,j,i]] - distances[i,j] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)
                nbConst += 1

    for s in range(nbS):
        for j in range(nnodes):
            if stratumCenter[j,s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (xD[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[j,s] *yD1[j])
                nbConst += 1

    return modele, w, As, Bs, nbVar, nbConst



def createModel_surchargeYDAssignationXReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD):


    nbVar = 0
    nbConst = 0

    modele = gp.Model("pcentre strates,pannes,capacités")

    mappingCentre = np.zeros(p, dtype=int)
    id = 0
    for i in range(nnodes):
        if yD[i] == True:
            mappingCentre[id] = i
            id += 1

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, p, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(p): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[mappingCentre[i], s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    x = modele.addVars(nbVariables, vtype=GRB.BINARY, name="x") # premier niveau

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")

    nbVar = nbVariables + nbS
    # Fonction objectif
    modele.setObjective(gp.quicksum(As[s] for s in range(nbS)), GRB.MINIMIZE)

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += x[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * x[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    for s in range(nbS):
        for j in range(p):
            if stratumCenter[mappingCentre[j],s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (x[mapping[s,j,i]])
                modele.addConstr( expr <= capacity[mappingCentre[j],s] * 1)
                nbConst += 1

    return modele, x, As, nbVar, nbConst



def createModel_surchargeYDAssignationWReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, yD, xD):

    nbVar = 0
    nbConst = 0

    modele = gp.Model("pcentre strates,pannes,capacités")

    mappingCentre = np.zeros(p, dtype=int)
    id = 0
    for i in range(nnodes):
        if yD[i] == True:
            mappingCentre[id] = i
            id += 1

    # Nombre de variables prises en compte
    nbVariables = 0
    mapping = np.zeros((nbS, p, nnodes))
    for s in range(nbS): # pour chaque strate
        for i in range(p): # pour chaque centre
            for j in range(nnodes): # pour chaque client
                if stratum[j, s] == 1 and stratumCenter[mappingCentre[i], s] == 1:
                    mapping[s, i, j] = nbVariables
                    nbVariables += 1
                else:
                    mapping[s, i, j] = -1

    # pprint.pprint(mapping)

    # Variables de décision
    w = modele.addVars(nbVariables, vtype=GRB.BINARY, name="w") # second niveau

    As = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="As")
    Bs = modele.addVars(nbS, lb=0.0, ub=maxDist, vtype=GRB.CONTINUOUS, name="Bs")

    nbVar = nbVariables + 2 * nbS
    # Fonction objectif
    modele.setObjective(gp.quicksum(As[s] + Bs[s] for s in range(nbS)), GRB.MINIMIZE)


    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += w[mapping[s,j,i]]
                modele.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            for j in range(p):
                if stratum[i,s] == 1 and stratumCenter[mappingCentre[j],s] == 1:
                    modele.addConstr(xD[mapping[s,j,i]] + w[mapping[s,j,i]] <= 1, f"assignationCentre2_{s}_{i}_{j}")
                    nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * xD[mapping[s,j,i]]
                modele.addConstr(expr <= As[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * w[mapping[s,j,i]]
                modele.addConstr(expr <= Bs[s])
                nbConst += 1

    for s in range(nbS):
        for i in range(nnodes):
            if stratum[i,s] == 1:
                expr = gp.LinExpr()
                for j in range(p):
                    if stratumCenter[mappingCentre[j],s] == 1:
                        expr += distances[i,mappingCentre[j]] * xD[mapping[s,j,i]] - distances[i,mappingCentre[j]] * w[mapping[s,j,i]]
                modele.addConstr(expr <= 0)
                nbConst += 1

    for s in range(nbS):
        for j in range(p):
            if stratumCenter[mappingCentre[j],s] == 1:
                expr = gp.LinExpr()
                for i in range(nnodes):
                    if stratum[i,s] == 1:
                        expr += demand[i,s] * (xD[mapping[s,j,i]]+w[mapping[s,j,i]])
                modele.addConstr( expr <= (1+alpha[s]) * capacity[mappingCentre[j],s] * 1) 
                nbConst += 1

    return modele, w, As, Bs, nbVar, nbConst