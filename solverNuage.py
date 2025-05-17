import sys
import numpy as np
import time

from code.heuristique import getPcentres
from code.instances import lectureInstances
from code.gurobi import createModel_surchargeYDReduit
from code.gurobi import setParameters


def calcul_mapping(nnodes, p, nbS, stratum, stratumCenter, yD):

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

    return mappingCentre, mapping


# calcul des distances entre les points et leurs centres attribués, pour chaque strate
def calcul_distances_strate(nnodes, p, nbS, stratum, stratumCenter, yD, x,w, distances, modele):
    """
    calcul des distances entre les points et leurs centres, pour chaque strate
    """
    mappingCentre, mapping = calcul_mapping(nnodes, p, nbS, stratum, stratumCenter, yD)

    distances_list = np.zeros((nnodes, nnodes))
    for i in range(nnodes):
        for j in range(nnodes):
            if i != j:
                distances_list[i,j] = distances[i,j]
            else:
                distances_list[i,j] = 0

                
    moy_distances = np.mean([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    min_distances = np.min([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    max_distances = np.max([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    med_distances = np.median([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    ecartType_distances = np.std([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    var_distances = np.var([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    covar_distances = np.cov([distances_list[i,j] for i in range(nnodes) for j in range(nnodes) if i != j])
    coef_variation = ecartType_distances/moy_distances
    # print("---"*40)
    # print("moy_distances : ", moy_distances)
    # print("min_distances : ", min_distances)
    # print("max_distances : ", max_distances)
    # print("med_distances : ", med_distances)
    # print("ecartType_distances : ", ecartType_distances)
    # print("var_distances : ", var_distances)
    # print("covar_distances : ", covar_distances)
    # print("coefficient de variation : ", coef_variation)
    # print("---"*40)

    distances_centre_x = np.zeros((nbS, nnodes))
    distances_centre_w = np.zeros((nbS, nnodes))

    val_x = modele.getAttr('X',x)
    val_w = modele.getAttr('X',w)

    for s in range(nbS):
        for i in range(p):
            for j in range(nnodes):
                if stratum[j,s] == 1 and stratumCenter[mappingCentre[i],s] == 1:
                    if val_x[mapping[s,i,j]] == 1:
                        distances_centre_x[s,j] = distances[mappingCentre[i],j]
                    if val_w[mapping[s,i,j]] == 1:
                        distances_centre_w[s,j] = distances[mappingCentre[i],j]
                else:
                    distances_centre_x[s,j] = -1
                    distances_centre_w[s,j] = -1


    # maximum de chaque strate
    maxX = np.zeros(nbS)
    maxW = np.zeros(nbS)
    # minimum de chaque strate
    minX = np.zeros(nbS)
    minW = np.zeros(nbS)
    # moyenne de chaque strate
    moyX = np.zeros(nbS)
    moyW = np.zeros(nbS)
    # médiane de chaque strate
    medX = np.zeros(nbS)
    medW = np.zeros(nbS)
    # écart-type de chaque strate
    ecartTypeX = np.zeros(nbS)
    ecartTypeW = np.zeros(nbS)
    # variance de chaque strate
    varX = np.zeros(nbS)
    varW = np.zeros(nbS)
    # covariance de chaque strate
    covarX = np.zeros(nbS)
    covarW = np.zeros(nbS)
    # coefficient de variation de chaque strate
    coef_variationX = np.zeros(nbS)
    coef_variationW = np.zeros(nbS)

    

    for s in range(nbS):

        valeurs_validesX = [distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1]
        valeurs_validesW = [distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1]

        if valeurs_validesX and valeurs_validesW:
        
            maxX[s] = max([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            maxW[s] = max([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            minX[s] = min([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            minW[s] = min([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            moyX[s] = np.mean([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            moyW[s] = np.mean([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            medX[s] = np.median([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            medW[s] = np.median([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            ecartTypeX[s] = np.std([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            ecartTypeW[s] = np.std([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            varX[s] = np.var([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            varW[s] = np.var([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            covarX[s] = np.cov([distances_centre_x[s,j] for j in range(nnodes) if distances_centre_x[s,j] != -1])
            covarW[s] = np.cov([distances_centre_w[s,j] for j in range(nnodes) if distances_centre_w[s,j] != -1])
            coef_variationX[s] = ecartTypeX[s]/moyX[s]
            coef_variationW[s] = ecartTypeW[s]/moyW[s]

    
        else : 
            maxX[s] = None
            maxW[s] = None
            minX[s] = None
            minW[s] = None
            moyX[s] = None
            moyW[s] = None
            medX[s] = None
            medW[s] = None
            ecartTypeX[s] = None
            ecartTypeW[s] = None
            varX[s] = None
            varW[s] = None
            covarX[s] = None
            covarW[s] = None
            coef_variationX[s] = None
            coef_variationW[s] = None

    # print("---"*40)
    # print(distances_centre_x)
    # print("--------------------")
    # print(distances_centre_w)
    # print("--------------------")
    # print("maxX : ", maxX)
    # print("maxW : ", maxW)
    # print("--------------------")
    # print("minX : ", minX)
    # print("minW : ", minW)
    # print("--------------------")
    # print("moyX : ", moyX)
    # print("moyW : ", moyW)
    # print("--------------------")
    # print("medX : ", medX)
    # print("medW : ", medW)
    # print("--------------------")
    # print("ecartTypeX : ", ecartTypeX)
    # print("ecartTypeW : ", ecartTypeW)
    # print("--------------------")
    # print("varianceX : ",varX)
    # print("varianceW : ",varW)
    # print("--------------------")
    # print("co-varianceX : ",covarX)
    # print("co-varianceW : ",covarW)
    # print("--------------------")
    # print("coefficient de variation : ", coef_variationX)
    # print("coefficient de variation : ", coef_variationW)
    # print("---"*40)


    # distances entre les centres
    distances_centre_to_centre = np.zeros((p, p))
    for i in range(p):
        for j in range(p):
            if i != j:
                distances_centre_to_centre[i,j] = distances[mappingCentre[i], mappingCentre[j]]
            else:
                distances_centre_to_centre[i,j] = 0

    # moyenne des distances entre les centres
    moy_distances_centre = np.mean([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    min_distances_centre = np.min([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    max_distances_centre = np.max([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    med_distances_centre = np.median([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    ecartType_distances_centre = np.std([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    var_distances_centre = np.var([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    covar_distances_centre = np.cov([distances_centre_to_centre[i,j] for i in range(p) for j in range(p) if i != j])
    coef_variation_distances_centre = ecartType_distances_centre/moy_distances_centre

    # print("---"*40)
    # print("distance_centre_to_centre : \n", distances_centre_to_centre)
    # print("--------------------")
    # print("moy_distances_centre : ", moy_distances_centre)
    # print("min_distances_centre : ", min_distances_centre)
    # print("max_distances_centre : ", max_distances_centre)
    # print("med_distances_centre : ", med_distances_centre)
    # print("ecartType_distances_centre : ", ecartType_distances_centre)
    # print("var_distances_centre : ", var_distances_centre)
    # print("covar_distances_centre : ", covar_distances_centre)
    # print("coefficient de variation : ", coef_variation_distances_centre)
    # print("---"*40)
 
    return min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre



def calcul_capacites_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele, demande, capacite, alpha):

    """
    calcul des distances entre les points et leurs centres, pour chaque strate
    """
    mappingCentre, mapping = calcul_mapping(nnodes, p, nbS, stratum, stratumCenter, centres_y)

    capacite_X_temoin = np.zeros((nbS, p))
    capacite_W_temoin = np.zeros((nbS, p))
    demande_cumulee_X = np.zeros((nbS, p))
    demande_cumulee_W = np.zeros((nbS, p))
    capacite_residuelle_X = np.zeros((nbS, p))
    capacite_residuelle_W = np.zeros((nbS, p))

    val_x = modele.getAttr('X',x)
    val_w = modele.getAttr('X',w)

    for s in range(nbS):
        for i in range(p):
            if stratumCenter[mappingCentre[i],s] == 1:
                capacite_X_temoin[s,i] = capacite[mappingCentre[i],s]
                demande_cumulee_X[s,i] = 0

                for j in range(nnodes):
                    if stratum[j,s] == 1 and val_x[mapping[s,i,j]] == 1:
                        demande_cumulee_X[s,i] += demande[j,s]
                
                capacite_W_temoin[s,i] = capacite[mappingCentre[i],s]*alpha[s] + (capacite[mappingCentre[i],s] - demande_cumulee_X[s,i])
                demande_cumulee_W[s,i] = 0
            
                for j in range(nnodes):
                    if stratum[j,s] == 1 and val_w[mapping[s,i,j]] == 1:
                        demande_cumulee_W[s,i] += demande[j,s]
    
    capacite_residuelle_X = capacite_X_temoin - demande_cumulee_X
    capacite_residuelle_W = capacite_W_temoin - demande_cumulee_W

    # print("--------------------")
    # print("capacite_X_temoin : \n", capacite_X_temoin)
    # print("capacite_W_temoin : \n", capacite_W_temoin)
    # print("--------------------")
    # print("demande_cumulee_X : \n", demande_cumulee_X)
    # print("demande_cumulee_W : \n", demande_cumulee_W)
    # print("--------------------")
    # print("capacite_residuelle_X : \n", capacite_residuelle_X)
    # print("capacite_residuelle_W : \n", capacite_residuelle_W)
    # print("--------------------")

    # capacite minimale de chaque strate
    min_capacite_X = np.zeros(nbS)
    min_capacite_W = np.zeros(nbS)
    # capacite maximale de chaque strate
    max_capacite_X = np.zeros(nbS)
    max_capacite_W = np.zeros(nbS)
    # capacite moyenne de chaque strate
    moy_capacite_X = np.zeros(nbS)
    moy_capacite_W = np.zeros(nbS)
    # capacite médiane de chaque strate
    med_capacite_X = np.zeros(nbS)
    med_capacite_W = np.zeros(nbS)
    # capacite écart-type de chaque strate
    ecartType_capacite_X = np.zeros(nbS)
    ecartType_capacite_W = np.zeros(nbS)
    # capacite variance de chaque strate
    var_capacite_X = np.zeros(nbS)
    var_capacite_W = np.zeros(nbS)
    # capacite covariance de chaque strate
    covar_capacite_X = np.zeros(nbS)
    covar_capacite_W = np.zeros(nbS)
    # pourcentage de capacité utilisée
    capacite_utilisee_X = np.zeros(nbS)
    capacite_utilisee_W = np.zeros(nbS)
    # pourcentage de capacité utilisée par centre
    capacite_utilisee_X_par_centre = np.zeros((nbS, p))
    capacite_utilisee_W_par_centre = np.zeros((nbS, p))
    # coefficient de variation de chaque strate
    coef_variation_capacite_X = np.zeros(nbS)
    coef_variation_capacite_W = np.zeros(nbS)

    for s in range(nbS):
        min_capacite_X[s] = min([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        min_capacite_W[s] = min([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        max_capacite_X[s] = max([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        max_capacite_W[s] = max([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        moy_capacite_X[s] = np.mean([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        moy_capacite_W[s] = np.mean([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        med_capacite_X[s] = np.median([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        med_capacite_W[s] = np.median([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        ecartType_capacite_X[s] = np.std([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        ecartType_capacite_W[s] = np.std([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        var_capacite_X[s] = np.var([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        var_capacite_W[s] = np.var([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])
        covar_capacite_X[s] = np.cov([capacite_X_temoin[s,i] for i in range(p) if capacite_X_temoin[s,i] != -1])
        covar_capacite_W[s] = np.cov([capacite_W_temoin[s,i] for i in range(p) if capacite_W_temoin[s,i] != -1])

        capacite_utilisee_X[s] = round((demande_cumulee_X[s].sum() / capacite_X_temoin[s].sum()) * 100,2)
        capacite_utilisee_W[s] = round((demande_cumulee_W[s].sum() / capacite_W_temoin[s].sum()) * 100,2)
        for i in range(p):
            capacite_utilisee_X_par_centre[s,i] = round((demande_cumulee_X[s,i] / capacite_X_temoin[s,i]) * 100,2)
            capacite_utilisee_W_par_centre[s,i] = round((demande_cumulee_W[s,i] / capacite_W_temoin[s,i]) * 100,2)

        coef_variation_capacite_X[s] = ecartType_capacite_X[s]/moy_capacite_X[s]
        coef_variation_capacite_W[s] = ecartType_capacite_W[s]/moy_capacite_W[s] 

    # print("--------------------")
    # print("min_capacite_X : ", min_capacite_X)
    # print("min_capacite_W : ", min_capacite_W)
    # print("--------------------")
    # print("max_capacite_X : ", max_capacite_X)
    # print("max_capacite_W : ", max_capacite_W)
    # print("--------------------")
    # print("moy_capacite_X : ", moy_capacite_X)
    # print("moy_capacite_W : ", moy_capacite_W)
    # print("--------------------")
    # print("med_capacite_X : ", med_capacite_X)
    # print("med_capacite_W : ", med_capacite_W)
    # print("--------------------")
    # print("ecartType_capacite_X : ", ecartType_capacite_X)
    # print("ecartType_capacite_W : ", ecartType_capacite_W)
    # print("--------------------")
    # print("var_capacite_X : ", var_capacite_X)
    # print("var_capacite_W : ", var_capacite_W)
    # print("--------------------")   
    # print("covar_capacite_X : ", covar_capacite_X)
    # print("covar_capacite_W : ", covar_capacite_W)
    # print("--------------------")
    # print("pourcentage capacite_utilisee_X : ", capacite_utilisee_X)
    # print("pourcentage capacite_utilisee_W : ", capacite_utilisee_W)
    # print("--------------------")
    # print("pourcentage capacite_utilisee_X_par_centre : \n", capacite_utilisee_X_par_centre)
    # print("pourcentage capacite_utilisee_W_par_centre : \n", capacite_utilisee_W_par_centre)
    # print("--------------------")

    return capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W


# fonction qui écrit dans un fichier les résultats
def write_results(titre, filename, nnodes, nbs, p, min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre, capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W, valeur_objective, temps_calcul, nb_solutions, nb_noeuds, faisability):
    """
    écrit les résultats dans un fichier
    """
    with open(f"{filename}_{titre}.txt", "a") as f:

        f.write("nombre de noeuds : " + str(nnodes) + "\n")
        f.write("nombre de strates : " + str(nbs) + "\n")
        f.write("nombre de centres : " + str(p) + "\n")
        f.write("titre : " + titre + "\n")
        f.write("instances : " + filename + "\n")
        f.write("temps de calcul : " + str(temps_calcul) + "\n")
        f.write("valeur objective : " + str(valeur_objective) + "\n")
        f.write("nombre de solutions : " + str(nb_solutions) + "\n")
        f.write("nombre de noeuds : " + str(nb_noeuds) + "\n")
        f.write("faisability : " + str(faisability) + "\n")
        if faisability == False:
            for i in range(nnodes):
                f.write("##########\t")
            return

        f.write("moy_distances :\t" + str(round(moy_distances,2)) + "\n")
        f.write("min_distances :\t" + str(min_distances) + "\n")
        f.write("max_distances :\t" + str(max_distances) + "\n")
        f.write("var_distances :\t" + str(var_distances) + "\n")
        f.write("covar_distances :\t" + str(covar_distances) + "\n")
        f.write("ecartType_distances :\t" + str(ecartType_distances) + "\n")
        f.write("coef_variation\t: " + str(coef_variation) + "\n")

        ########################################################
        f.write("distances_centre_x :\n")
        for s in range(nbs):
            for i in range(nnodes):
                f.write(str(distances_centre_x[s,i]) + "\t")
            f.write("\n")
        
        f.write("\n")

        ########################################################
        f.write("distances_centre_w :\n")
        for s in range(nbs):
            for i in range(nnodes):
                f.write(str(distances_centre_w[s,i]) + "\t")
            f.write("\n")
        
        f.write("\n")
        
        ########################################################
        f.write("maxX :\n")
        for s in range(nbs):
            f.write(str(maxX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("maxW :\n")
        for s in range(nbs):
            f.write(str(maxW[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("minX :\n")
        for s in range(nbs):
            f.write(str(minX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("minW :\n")
        for s in range(nbs):
            f.write(str(minW[s]) + "\t")
        f.write("\n\n")


        ########################################################
        f.write("moyX :\n")
        for s in range(nbs):
            f.write(str(moyX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("moyW :\n")
        for s in range(nbs):
            f.write(str(moyW[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("medX :\n")
        for s in range(nbs):
            f.write(str(medX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("medW :\n")
        for s in range(nbs):
            f.write(str(medW[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("ecartTypeX :\n")
        for s in range(nbs):
            f.write(str(ecartTypeX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("ecartTypeW :\n")
        for s in range(nbs):
            f.write(str(ecartTypeW[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("varX :\n")
        for s in range(nbs):
            f.write(str(varX[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("varW :\n")
        for s in range(nbs):
            f.write(str(varW[s]) + "\t")
        f.write("\n\n")

        ########################################################
        f.write("covarX :\n")
        for s in range(nbs):
            f.write(str(covarX[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("covarW :\n")
        for s in range(nbs):
            f.write(str(covarW[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("coef_variationX :\n")
        for s in range(nbs):
            f.write(str(coef_variationX[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("coef_variationW :\n")
        for s in range(nbs):
            f.write(str(coef_variationW[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("moy_distances_centre :\t" + str(moy_distances_centre) + "\n")
        f.write("min_distances_centre :\t" + str(min_distances_centre) + "\n")
        f.write("max_distances_centre :\t" + str(max_distances_centre) + "\n")
        f.write("med_distances_centre :\t" + str(med_distances_centre) + "\n")
        f.write("ecartType_distances_centre :\t" + str(ecartType_distances_centre) + "\n")
        f.write("var_distances_centre :\t" + str(var_distances_centre) + "\n")
        f.write("covar_distances_centre :\t" + str(covar_distances_centre) + "\n")
        f.write("coef_variation_distances_centre :\t" + str(coef_variation_distances_centre) + "\n")
        

        ########################################################
        f.write("capacite_X_temoin : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(capacite_X_temoin[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("capacite_W_temoin : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(capacite_W_temoin[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("demande_cumulee_X : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(demande_cumulee_X[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("demande_cumulee_W : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(demande_cumulee_W[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("capacite_residuelle_X : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(capacite_residuelle_X[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("capacite_residuelle_W : \n")
        for s in range(nbs):
            for i in range(p):
                f.write(str(capacite_residuelle_W[s,i]) + "\t")
            f.write("\n")
        f.write("\n")
        ########################################################
        f.write("min_capacite_X : \n")
        for s in range(nbs):
            f.write(str(min_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("min_capacite_W : \n")
        for s in range(nbs):
            f.write(str(min_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("max_capacite_X : \n")
        for s in range(nbs):
            f.write(str(max_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("max_capacite_W : \n")
        for s in range(nbs):
            f.write(str(max_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("moy_capacite_X : \n")
        for s in range(nbs):
            f.write(str(moy_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("moy_capacite_W : \n")
        for s in range(nbs):
            f.write(str(moy_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("med_capacite_X : \n")
        for s in range(nbs):
            f.write(str(med_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("med_capacite_W : \n")
        for s in range(nbs):
            f.write(str(med_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("ecartType_capacite_X : \n")
        for s in range(nbs):    
            f.write(str(ecartType_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("ecartType_capacite_W : \n")
        for s in range(nbs):
            f.write(str(ecartType_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("var_capacite_X : \n")
        for s in range(nbs):
            f.write(str(var_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("var_capacite_W : \n")
        for s in range(nbs):
            f.write(str(var_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("covar_capacite_X : \n")
        for s in range(nbs):
            f.write(str(covar_capacite_X[s]) + "\t")
        f.write("\n\n")
        ########################################################
        f.write("covar_capacite_W : \n")
        for s in range(nbs):
            f.write(str(covar_capacite_W[s]) + "\t")
        f.write("\n\n")
        ########################################################

        for i in range(nnodes):
            f.write("##########\t")









def suppressionCentre(distanceDonnee, centres, nnodes, p, nbs, stratum, stratumCenter, maxDist):
    """
    Choix du centre à supprimer parmi les p centres déjà placés, on prendra celui est le plus loin en termes de distance
    """

    distanceDonnee = np.array(distanceDonnee)
    stratum = np.array(stratum)
    stratumCenter = np.array(stratumCenter)
    
    indicateur = np.zeros((p, nbs))
    for s in range(nbs):
        for i in range(p):
            if stratumCenter[centres[i],s] == 1:
                client_indices = np.where(stratum[:,s] == 1)[0]
                indicateur[i,s] = np.round(np.max(distanceDonnee[centres[i],client_indices]), 2)
            elif stratumCenter[centres[i],s] == 0:
                indicateur[i,s] = maxDist

    # origine
    origine = np.zeros(nbs)
    distanceOrigine = []

    for i in range(p):
        point = np.array(indicateur[i])
        D = np.linalg.norm(point-origine)
        distanceOrigine.append((centres[i],D))

    points_tries = [i for i,_ in sorted(distanceOrigine, key=lambda x: x[1], reverse=True)]
    

    return points_tries[0]









def main(filename:str):
    result = lectureInstances(filename)
    if result is None:
        print(f"Erreur : impossible de lire le fichier {filename}")
        return
    
    nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha = result
    centres_y, points_tries = getPcentres(demand, capacity, distances, nnodes, p, nbS, stratum, stratumCenter, alpha)

    # récupération du nom du fichier sans arborescence et sans extension
    filename = filename.split("/")[-1].split(".")[0]






    feasability = False
    valeur_objective = 0
    temps_calcul = 0
    nb_solutions = 0
    nb_noeuds = 0

# ################# TEST
#     modele, x, w, As, Bs, _,_ = createModel_surchargeYDReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, centres_y)
#     modele = setParameters(modele)
#     modele.optimize()

#     # faisabilité
#     if modele.Status == 3 or modele.Status == 4 or modele.Status == 5:
#         print("Le modèle est infaisable ou unbounded")
#         feasability = False
#     elif modele.Status == 2 or modele.Status == 13:
#         print("Le modèle est faisable (voire optimal)")
#         feasability = True

#     valeur_objective = modele.ObjVal
#     temps_calcul = modele.Runtime
#     nb_solutions = modele.SolCount
#     nb_noeuds = modele.NodeCount

    
#     min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre = calcul_distances_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele)

#     capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W = calcul_capacites_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele, demand, capacity, alpha)

    
#     write_results("titre",filename,nnodes, nbS, p, min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre,capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W, valeur_objective, temps_calcul, nb_solutions, nb_noeuds, feasability)
    
    
    
    
    
    
    
    # print("Valeur objective : ", valeur_objective)
    # print("Temps de calcul : ", round(temps_calcul, 2))
    # print("Nombre de solutions : ", nb_solutions)
    # print("Nombre de noeuds : ", nb_noeuds)
################# FIN TEST

    
    for i in range(p+2):
        centres_y = np.zeros(nnodes, dtype=bool)
        centre = points_tries[i:i+p]
        
        for j in centre:
            centres_y[j] = True

        feasability = False
        valeur_objective = 0
        temps_calcul = 0
        nb_solutions = 0
        nb_noeuds = 0

        modele, x, w, As, Bs, _,_ = createModel_surchargeYDReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, centres_y)
        modele = setParameters(modele)
        modele.optimize()

        # faisabilité
        if modele.Status == 3 or modele.Status == 4 or modele.Status == 5:
            print("Le modèle est infaisable ou unbounded")
            feasability = False
        elif modele.Status == 2 or modele.Status == 13:
            print("Le modèle est faisable (voire optimal)")
            feasability = True

        if feasability == True:
            valeur_objective = modele.ObjVal
            temps_calcul = modele.Runtime
            nb_solutions = modele.SolCount
            nb_noeuds = modele.NodeCount

            
            min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre = calcul_distances_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele)

            capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W = calcul_capacites_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele, demand, capacity, alpha)

            
            write_results("fenetre",filename,nnodes, nbS, p, min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre,capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W, valeur_objective, temps_calcul, nb_solutions, nb_noeuds, feasability)






    
    centre = points_tries[:p]


    for i in range(p+2):
        centres_y = np.zeros(nnodes, dtype=bool) 
            
        for j in centre:
            centres_y[j] = True

        feasability = False
        valeur_objective = 0
        temps_calcul = 0
        nb_solutions = 0
        nb_noeuds = 0

        modele, x, w, As, Bs, _,_ = createModel_surchargeYDReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, centres_y)
        modele = setParameters(modele)
        modele.optimize()

        # faisabilité
        if modele.Status == 3 or modele.Status == 4 or modele.Status == 5:
            print("Le modèle est infaisable ou unbounded")
            feasability = False
        elif modele.Status == 2 or modele.Status == 13:
            print("Le modèle est faisable (voire optimal)")
            feasability = True

        if feasability == True:
            valeur_objective = modele.ObjVal
            temps_calcul = modele.Runtime
            nb_solutions = modele.SolCount
            nb_noeuds = modele.NodeCount

            
            try:

                min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre = calcul_distances_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele)

                capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W = calcul_capacites_strate(nnodes, p, nbS, stratum, stratumCenter, centres_y, x, w, distances, modele, demand, capacity, alpha)

            except:
                print("Erreur lors du calcul des distances")
                min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation = 0,0,0,0,0,0,0
                distances_centre_x = np.zeros((nbS, nnodes))
                distances_centre_w = np.zeros((nbS, nnodes))
                maxX = np.zeros(nbS)
                maxW = np.zeros(nbS)
                minX = np.zeros(nbS)
                minW = np.zeros(nbS)
                moyX = np.zeros(nbS)
                moyW = np.zeros(nbS)
                medX = np.zeros(nbS)
                medW = np.zeros(nbS)
                ecartTypeX = np.zeros(nbS)
                ecartTypeW = np.zeros(nbS)
                varX = np.zeros(nbS)
                varW = np.zeros(nbS)
                covarX = np.zeros(nbS)
                covarW = np.zeros(nbS)
                coef_variationX = np.zeros(nbS)
                coef_variationW = np.zeros(nbS)
                moy_distances_centre = 0
                min_distances_centre = 0
                max_distances_centre = 0
                med_distances_centre = 0
                ecartType_distances_centre = 0
                var_distances_centre = 0
                covar_distances_centre = 0
                coef_variation_distances_centre = 0
                
                print("Erreur lors du calcul des capacités")
                capacite_X_temoin = np.zeros((nbS, p))
                capacite_W_temoin = np.zeros((nbS, p))
                demande_cumulee_X = np.zeros((nbS, p))
                demande_cumulee_W = np.zeros((nbS, p))
                capacite_residuelle_X = np.zeros((nbS, p))
                capacite_residuelle_W = np.zeros((nbS, p))
                min_capacite_X = np.zeros(nbS)
                min_capacite_W = np.zeros(nbS)
                max_capacite_X = np.zeros(nbS)
                max_capacite_W = np.zeros(nbS)
                moy_capacite_X = np.zeros(nbS)
                moy_capacite_W = np.zeros(nbS)
                med_capacite_X = np.zeros(nbS)
                med_capacite_W = np.zeros(nbS)
                ecartType_capacite_X = np.zeros(nbS)
                ecartType_capacite_W = np.zeros(nbS)
                var_capacite_X = np.zeros(nbS)
                var_capacite_W = np.zeros(nbS)
                covar_capacite_X = np.zeros(nbS)
                covar_capacite_W = np.zeros(nbS)


            try:

                write_results("intelligent",filename,nnodes, nbS, p, min_distances, max_distances, moy_distances, var_distances, covar_distances, ecartType_distances, coef_variation, distances_centre_x, distances_centre_w, maxX, maxW, minX, minW, moyX, moyW, medX, medW, ecartTypeX, ecartTypeW, varX, varW, covarX, covarW, coef_variationX, coef_variationW ,moy_distances_centre, min_distances_centre, max_distances_centre, med_distances_centre, ecartType_distances_centre, var_distances_centre, covar_distances_centre, coef_variation_distances_centre,capacite_X_temoin, capacite_W_temoin, demande_cumulee_X, demande_cumulee_W, capacite_residuelle_X, capacite_residuelle_W, min_capacite_X, min_capacite_W, max_capacite_X, max_capacite_W, moy_capacite_X, moy_capacite_W, med_capacite_X, med_capacite_W, ecartType_capacite_X, ecartType_capacite_W, var_capacite_X, var_capacite_W, covar_capacite_X, covar_capacite_W, valeur_objective, temps_calcul, nb_solutions, nb_noeuds, feasability)
            except:
                print("Erreur lors de l'écriture des résultats")

        centreASupprimer = suppressionCentre(distances, centre, nnodes, p, nbS, stratum, stratumCenter, maxDist)
        centre.remove(centreASupprimer)
        centre.append(points_tries[p+i])








    # print("y = ", centres_y)

    # debut = time.time()
    # modele2, x2, w, As2, Bs2, nbVar2, nbConst2 = createModel_surchargeYDReduit(nnodes, p, nbS, maxDist, distances, capacity, demand, stratum, stratumCenter, alpha, centres_y)
    # modele2 = setParameters(modele2)
    # modele2.optimize()
    # fin = time.time()
    # val_As2 = modele2.getAttr('X', As2)
    # val_Bs2 = modele2.getAttr('X', Bs2)
    # tempsSurchageReduit = fin - debut


    # sumAs2 = 0
    # sumBs2 = 0
    # for i in range(nbS):
    #     sumAs2 += val_As2[i]
    #     sumBs2 += val_Bs2[i]
    # print("modèle surcharge réduit : ")
    # print("As : ", sumAs2)
    # print("Bs : ", sumBs2)
    # print("As + Bs : ", sumAs2 + sumBs2)
    # print("Temps de calcul : ", round(tempsSurchageReduit, 2))
    # print("nombre de variables : ", nbVar2)
    # print("nombre de contraintes : ", nbConst2)














































if __name__ == '__main__':
    assert(len(sys.argv) == 2), "Usage: python nuagePoints.py <filename>"   
    filename = sys.argv[1]
    main(filename)