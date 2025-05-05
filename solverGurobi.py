import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pprint as pprint
import sys

from code.gurobi import ajoutContraintes
from code.gurobi import createModel_surcharge, setParameters
from code.instances import displayInstances
from code.instances import lectureInstances


def resultats(modele, resolution):
    if modele.status == GRB.INFEASIBLE:
        print("Problème infaisable")
        return
    elif modele.status == GRB.UNBOUNDED:
        print("Problème non borné")
        return
    elif modele.status == GRB.OPTIMAL:
        print("Solution optimale")
    elif modele.status == GRB.SUBOPTIMAL:
        print("Solution suboptimale/faisable")
    elif modele.status == GRB.TIME_LIMIT:
        print("Temps limite atteint")
    elif modele.status == GRB.SOLUTION_LIMIT:
        print("Nombre de solution atteint")
    else:
        print("Problème non résolu")
    print("Statut du modèle : ", modele.status)
    print("Nombre de noeuds explorés : ", modele.NodeCount)
    print("Temps de calcul : ", modele.Runtime, " secondes")
    print("Valeur de la fonction objectif : ", modele.ObjVal)
    print("Borne inférieure : ", modele.ObjBound)
    print("Borne supérieure : ", modele.ObjVal)
    print("Nombre de solutions trouvées : ", modele.SolCount)
    if resolution == "MIP":
        print("MIPGap : ", modele.MIPGap)



if __name__ == "__main__":
    assert(len(sys.argv) == 5), "Usage: python solver.py <filename> <objectiveFunction> <csv> <method : LP or MIP>"
    assert(sys.argv[2] == "AB" or sys.argv[2] == "A" or sys.argv[2] == "B"), "objectiveFunction must be AB, A or B"
    
    objectiveFunction = sys.argv[2]
    csv_file = sys.argv[3]

    # # lecture de l'instance
    nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha = lectureInstances(sys.argv[1])
    
    # displayInstances(maxDist, distances, capacity, demand, stratum, stratumCenter)

    modele, x, w, y, As, Bs = createModel_surcharge(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, objectiveFunction, alpha, sys.argv[4])
    
    modele = setParameters(modele)

    modele.optimize()

    try:
        LB_val_pre = modele.ObjBound
        UB_val_pre = modele.ObjVal
    except:
        LB_val_pre = "None"
        UB_val_pre = "None"


    print("--"*30)

    modele = ajoutContraintes(modele, x, w, y, As, Bs, nnodes, nbS, stratum, stratumCenter, distances, demand, capacity, alpha)

    modele.optimize()

    try:
        LB_val_post = modele.ObjBound
        UB_val_post = modele.ObjVal
    except:
        LB_val_post = "None"
        UB_val_post = "None"

    # écriture dans un fichier csv
    with open(csv_file, "a") as f:
        f.write(f"{sys.argv[1]}\t{nnodes}\t{p}\t{nbS}\t{modele.status}\t{modele.Runtime}\t{objectiveFunction}\t{LB_val_pre}\t{UB_val_pre}\t{LB_val_post}\t{UB_val_post}\n")




    # # résultats
    # if modele.status == GRB.INFEASIBLE:
    #     print("Problème infaisable")
    #     with open(csv_file, "a") as f:
    #         f.write(f"{sys.argv[1]}\t{objectiveFunction}\tINFEASIBLE\n")
    # elif modele.status == GRB.UNBOUNDED:
    #     print("Problème non borné")
    #     with open(csv_file, "a") as f:
    #         f.write(f"{sys.argv[1]}\t{objectiveFunction}\tUNBOUNDED\n") 
    # elif modele.status != GRB.OPTIMAL and modele.status != GRB.SUBOPTIMAL and modele.status != GRB.TIME_LIMIT:
    #     print("Problème non résolu")
    

    # print(f"Il y a eu {modele.NodeCount} noeuds explorés")
    # print(f"Temps de calcul : {modele.Runtime} secondes")

    # if modele.status == GRB.OPTIMAL:
    #     print("Solution optimale")
    #     feasibility = "Optimal"
    # elif modele.status == GRB.SUBOPTIMAL:
    #     print("Solution suboptimale")
    #     feasibility = "Suboptimal"
    #     print("Solution faisable ou suboptimal : ", modele.SolCount, " solutions trouvées")
    # elif modele.status == GRB.TIME_LIMIT:
    #     print("Temps limite atteint")
    #     feasibility = "TimeLimit"
    #     print("Solution faisable ou suboptimal : ", modele.SolCount, " solutions trouvées")
    # elif modele.status == GRB.SOLUTION_LIMIT:
    #     print("nombre de solution atteint")
    #     feasibility = "SolutionLimit"
    #     print("Solution faisable ou suboptimal : ", modele.SolCount, " solutions trouvées")

    # if modele.status == GRB.OPTIMAL or modele.status == GRB.SUBOPTIMAL or modele.status == GRB.TIME_LIMIT and modele.SolCount > 0 or modele.status == GRB.SOLUTION_LIMIT:
    #     val_x = modele.getAttr('X', x)
    #     val_w = modele.getAttr('X', w)

    #     # calcul des valeurs de As et Bs en fonction des x et w
    #     id = 0
    #     val_As = np.zeros(nbS)
    #     val_Bs = np.zeros(nbS)
    #     val_As_pmedian = np.zeros(nbS)
    #     val_Bs_pmedian = np.zeros(nbS)

    #     nbPerS = np.zeros(nbS)
    #     for s in range(nbS):
    #         for i in range(nnodes):
    #             if stratum[i,s] == 1:
    #                 nbPerS[s] += 1

    #     for s in range(nbS):
    #         for i in range(nnodes):
    #             for j in range(nnodes):
    #                 if stratum[j,s] == 1 and stratumCenter[i,s] == 1:
    #                     if val_As[s] < val_x[id] * distances[i,j]:
    #                         val_As[s] = distances[i,j] * val_x[id]
    #                     if val_Bs[s] < val_w[id] * distances[i,j]:
    #                         val_Bs[s] = distances[i,j] * val_w[id]

    #                     id += 1

    #     for s in range(nbS):
    #         val_As_pmedian[s] = round(val_As_pmedian[s] / nbPerS[s], 2)
    #         val_Bs_pmedian[s] = round(val_Bs_pmedian[s] / nbPerS[s], 2)


    #     print("VALEUR DE As :")
    #     pprint.pprint(val_As)

    #     print("VALEUR DE Bs :")
    #     pprint.pprint(val_Bs)

    #     print("VALEUR DE As pmedian :")
    #     pprint.pprint(val_As_pmedian)

    #     print("VALEUR DE Bs pmedian :")
    #     pprint.pprint(val_Bs_pmedian)

    #     print("Somme des As : ", sum(val_As))
    #     print("Somme des Bs : ", sum(val_Bs))
    #     print("Somme des As + Bs : ", sum(val_As) + sum(val_Bs))
    #     print("Somme des As2 : ", sum(val_As_pmedian))
    #     print("Somme des Bs2 : ", sum(val_Bs_pmedian))
    #     print("Somme des As2 + Bs2 : ", round(sum(val_As_pmedian) + sum(val_Bs_pmedian), 2))
        
    #     if objectiveFunction == "AB":
    #         objVal = sum(val_As) + sum(val_Bs)
    #         print("Valeur de la fonction objectif : ", sum(val_As) + sum(val_Bs))
    #     elif objectiveFunction == "A":
    #         objVal = sum(val_As)
    #         print("Valeur de la fonction objectif : ", sum(val_As))
    #     elif objectiveFunction == "B":
    #         objVal = sum(val_Bs)
    #         print("Valeur de la fonction objectif : ", sum(val_Bs))

    #     # Si LP 
    #     if sys.argv[4] == "LP":
    #         with open(csv_file, "a") as f:
    #             f.write(f"{sys.argv[4]}\t{sys.argv[1]}\t{nnodes}\t{p}\t{nbS}\t{feasibility}\t{modele.Runtime}\t{objectiveFunction}\t{sum(val_As)}\t{sum(val_Bs)}\t{sum(val_As) + sum(val_Bs)}\t{modele.NodeCount}\t{modele.ObjBound}\n")
    #     elif sys.argv[4] == "MIP":
    #         with open(csv_file, "a") as f:
    #             f.write(f"{sys.argv[4]}\t{sys.argv[1]}\t{nnodes}\t{p}\t{nbS}\t{feasibility}\t{modele.Runtime}\t{objectiveFunction}\t{sum(val_As)}\t{sum(val_Bs)}\t{sum(val_As) + sum(val_Bs)}\t{modele.NodeCount}\t{modele.ObjBound}\t{modele.MIPGap}\n")

    #         print("Borne inférieure : ", modele.ObjBound)
    #         print("Borne supérieure : ", modele.ObjVal)
        