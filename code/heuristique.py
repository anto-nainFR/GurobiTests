import numpy as np


def calculDemandeTotale(demande, nnodes, nbs):
    """
    Calcul de la demande totale pour chaque strate
    """
    # Calcul de la demande totale pour chaque strate
    demandeTotale = np.zeros(nbs)
    for s in range(nbs):
        for i in range(nnodes):
            demandeTotale[s] += demande[i,s]
    return demandeTotale

def calculCapacite(capaciteDonnee, nnodes, nbs, stratumCenter):
    """
    Calcul de la capacité de chaque noeud pour chaque strate
    """
    capacite = np.zeros((nnodes, nbs))
    for s in range(nbs):
        for i in range(nnodes):
            capacite[i, s] = capaciteDonnee[i, s] * stratumCenter[i,s]
    return capacite.tolist()
        
def ordonnancementPoints(capacite, demandeTotale, mins, reverse=False):
    """
    Ordonnancement des points en fonction de la capacité par rapport à la distance à l'origine
    """
    distancesOrigine = []
    origine = np.array(mins)

    for i in range(len(capacite)):
        point = np.array(capacite[i] / demandeTotale)
        D = np.linalg.norm(point-origine)
        distancesOrigine.append((i,D))

    points_tries = [i for i,_ in sorted(distancesOrigine, key=lambda x: x[1], reverse=reverse)]

    return points_tries

def choixCentre(demande, capaciteDonnee, nnodes, p, nbs, stratum, stratumCenter):
    """
    Choix de p centres en fonction de la demande totale et de la capacité
    """
    print("Calcul de la demande totale")
    demandeTotale = calculDemandeTotale(demande, nnodes, nbs)

    print("Calcul de la capacité")
    capacite = calculCapacite(capaciteDonnee, nnodes, nbs, stratumCenter)

    # minimum de la capacité pour chaque strate
    mins = np.zeros(nbs)
    maxs = np.zeros(nbs)
    for s in range(nbs):
        mins[s] = min([capacite[i][s] for i in range(nnodes)])
        maxs[s] = max([capacite[i][s] for i in range(nnodes)])

    print("Ordonnancement des points")
    points_tries = ordonnancementPoints(capacite, demandeTotale, mins, reverse=True)

    return points_tries

def getPcentres(demande, capacite, distance, nnodes, p, nbs, stratum, stratumCenter, alpha):

    points_tries = choixCentre(demande, capacite, nnodes, p, nbs, stratum, stratumCenter)
    centres = points_tries[:p]
    
    y = np.zeros(nnodes, dtype=bool)
    for i in centres:
        y[i] = True

    return y, points_tries
