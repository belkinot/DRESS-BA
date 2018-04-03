"""Implementation des DRESS-Algorithmus"""

import helper_functions
import math


"""
qcons ranked supspaces
qdist using HEOS

q(s)

dbscan auf subspace

"""



def merge_and_filter_subspaces(dataset, originalFeatureSet):

    subspaceClusters = set()
    candidateSubspaces = set()
    subspaceQualityValues = set()

    #for i in originalFeatureSet:
        #DBSCAN
        # store initial clusters
        # store subspace candidate
        # store subspace quality

def subspace_quality_scoring(dataset):
    #Liste mit Featuren, letzter Eintrag beinhaltet Clusterlabel
    # ml-satisfied ML constraint set
    ml_sat_set = list()
    nl_sat_set = list()

    ml = list()
    nl = list()

    q_cons = len(ml_sat_set) + len(nl_sat_set) / (len(ml) + len(nl))

    d_nl_avg = 0
    d_ml_avg = 0

    for count, _ in enumerate(nl_sat_set):
        for count2, _ in enumerate(nl_sat_set):
            d_nl_avg += distance_heom(nl_sat_set[count], nl_sat_set[count2])
    d_nl_avg = d_nl_avg/len(nl_sat_set) # Average Distanz des Satisfaction Sets oder des gesamten NL sets??

    for count, _ in enumerate(ml_sat_set):
        for count2, _ in enumerate(ml_sat_set):
            d_ml_avg += distance_heom(ml_sat_set[count], ml_sat_set[count2])
    d_ml_avg = d_ml_avg/len(ml_sat_set)


    q_dist = d_nl_avg - d_ml_avg

    quality = q_cons * q_dist

    return quality


def clustering_dress(dataset):
    minPts=round(math.log1p(len(dataset)))
    epsilon = 1
    #Distance of every point in our subspace to its m'th nearest neighbour and sort this list in ascending order
    #create an m-dist graph ?????? Nachfragen!!!



def subspace_processing_and_cluster_generation(dataset, setOfSubspaceClusters, setOfCandidateSubspaces,setOfSubspaceQualityValues):
    """erstellt die Subspaces und die Cluster"""
    """startet mit subspaces der größe 1
     setOfCandidateSubspaces hat alle Features (Dimensionen)
     Iteration 2 (Subspace der Größe 2) für jeden Supspace in C_i (Candidate)
     wird q(s) berechnet (nach dem Clustering)
     Wähle S_Best von c_all
     q(S_best) vereinige S_best mit allen noch vorhandenen Subspaces in C_all
    
     Vereinfachung: S_best vereinigt S, wobei S_best geschnitten S = Leere Menge
     S_dist = S_best wenn q_dist(S_best) >= q_dist(S*), sonst
     S_dist = S*
    
    S_new nur dann wenn:
    
    delta(d_nl_avg(S_new) - delta(d_ml_avg(S_new)) > 0 mit
    delta(d_nl_avg(S_new) = d_nl_avg(S_dist) - d_nl_avg(S_new)
    und delta(d_ml_avg(S_new) = d_ml_avg(S_dist) - d_ml_avg(S_new)
    
    
    Clustere in jedem Supspace S aus C_i und berechne q(S) 
    Es bleibt ein Subspace S aus C_i wenn und nur wenn q(S) > q_best
    Setze C_all = C_all Vereinigt mit C_i am ende von Iteration i
    
    Für jeden Subspace S_best vereinigt S* in C_i wird S* von C_all entfernt und dann S_best von C_all
    
    Iteration stoppt wenn C_all leer ist
    
    """

    return setOfSubspaceClusters


def calculate_subspace_quality():
    """Berechnet die Subspace Qualität"""
    subspace_quality = 0
    return subspace_quality


