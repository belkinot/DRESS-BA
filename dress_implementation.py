"""Implementation des DRESS-Algorithmus"""

import math
from Base.helper_functions import distance_heom, k_nearest_neighbour_list, draw_k_dist_line
from sklearn.cluster import DBSCAN
from itertools import combinations
import numpy as np

"""
ML constraints low distance
NL constraints have high distance to each other - search for subspaces

Dress generiert potential candidate subspaces (select best subspace)
Add Features to the subspace - Candidate Subspaces(merging step)
Filtering - dann errechne quality scores durch clustering
Cleaning - candidate subspaces
"""

"""
Pseudocode
Start subspace mit Mächtigkeit 1 (1 Feature) C_all enthält alle features
berechne q(S) = q_const(S) * q_dist(S) 
Choose S_best von C_all --> q(S_best) = q_best
Vereinige S_best mit jedem Subspace von C_all --> neue Candidatsubspaces C_i
Vereinfachung: 
S_dist = S_best wenn q_dist(S_best) >= q_dist(S*), sonst S*
S_new nur wenn d_nl_avg(S_dist) - d_nl_avg(S_new) und
               d_ml_avg(S_dist) - d_nl_avg(S_new)

Clustere jeden Subspace mit DBSCAN
Errechne q(S) 
Subspace bleibt erhalten, wenn q(S) > q_best (q(S_best))
C_all vereinigt mit C_i am ende der Iteration i

S* und S_best werden von C_all entfernt, neue Iteration beginnt


"""


def merge_and_filter_subspaces(dataset, originalFeatureSet):
    """test"""
    subspaceClusters = set()
    candidateSubspaces = set()
    subspaceQualityValues = set()

    #for i in originalFeatureSet:
        #DBSCAN
        # store initial clusters
        # store subspace candidate
        # store subspace quality

    return subspaceClusters

def subspace_quality_scoring(dataset_with_n_features, clustering, ml_constraints, nl_constraints):
    """Scores Quality of our Subspace"""
    # ml-constraints (Tupel von Indizes die verbunden sein müssen)


    #Prüfe ob ml constraints in einem Cluster sind
    ml_sat = check_ml_constraints_in_clustering(ml_constraints, clustering)
    #Prüfe ob nl_constraints in verschiedenen Clustern sind
    nl_sat = check_nl_constraints_in_clustering(nl_constraints, clustering)

    q_cons = (ml_sat + nl_sat) / (len(ml_constraints) + len(nl_constraints))

    d_nl_avg = 0
    d_ml_avg = 0

    for _, value in enumerate(nl_constraints):
        # Indizes 0 und 1 für das korrekte Ansprechen der Tupelpaare
        d_nl_avg += distance_heom(dataset_with_n_features[value[0]], dataset_with_n_features[value[1]])
    d_nl_avg = d_nl_avg/len(nl_constraints)# Average Distanz des gesamten NL sets??

    for _, value in enumerate(ml_constraints):
        d_ml_avg += distance_heom(dataset_with_n_features[value[0]], dataset_with_n_features[value[1]])
    d_ml_avg = d_ml_avg/len(ml_constraints)

    q_dist = d_nl_avg - d_ml_avg
    #Errechne Qualität
    quality = q_cons * q_dist

    return quality


def check_nl_constraints_in_clustering(constraints, clustering):
    """Prüft wie viele NL-Constraints erfüllt sind"""
    # Annahme: Clustering ist eine Liste von Listen mit Indizes ((1,2,5), (3,4), (6,9), (7,8))
    constraint_sat = 0

    for constraint in constraints:
        for key in clustering:
            if constraint[0] in clustering[key]:
                if constraint[1] not in clustering[key]:
                    constraint_sat += 1

    return constraint_sat


def check_ml_constraints_in_clustering(constraints, clustering):
    """Prüft wie viele ML-Constraints erfüllt sind"""
    # Annahme: Clustering ist eine Liste von Listen mit Indizes ((1,2,5), (3,4), (6,9), (7,8))
    constraint_sat = 0

    for constraint in constraints:
        for key in clustering:
            if constraint[0] in clustering[key]:
                if constraint[1] in clustering[key]:
                    constraint_sat += 1

    return constraint_sat


def clustering_dress(dataset):
    """Dress algorithmus"""
    minpts = round(math.log1p(len(dataset)))

    epsilon = draw_k_dist_line(k_nearest_neighbour_list(dataset, minpts))
    #Distance of every point in our subspace to its m'th nearest neighbour and sort this list in ascending order
    #create an m-dist graph ?????? Nachfragen!!!

    dataset.DBSCAN(epsilon, minpts)

    return 0


def dolle_funktion(canditate_all, wert_objekt):
    """ Erstelle eine Liste von Tupeln"""

    res = [(canditate,) + (wert_objekt,) for canditate in canditate_all]
    return res


def create_m_dimensional_dataset(dataset_n_dimensions, candidate_i):
    dataset_with_m_dimensions = [0 for _ in range(dataset_n_dimensions.shape[0])]
    for value in candidate_i:
        for idx, _ in enumerate(dataset_n_dimensions):
            dataset_with_m_dimensions[idx] += dataset_n_dimensions[idx][value]

    return dataset_with_m_dimensions


def subspace_processing_and_cluster_generation(dataset, ml_constraints, nl_constraints):
    """erstellt die Subspaces und die Cluster"""
    current_dataset = list()
    q_best = 0
    best_subspace = 0
    candidate_all = list(range(len(dataset[0])))  # Anzahl der Dimensionen

    # erstelle 1-Dimensionalen Datensatz
    for i in candidate_all:
        current_dataset = list()
        for value in dataset:
            current_dataset.append(value[i])
        current_numpy_dataset = np.array(current_dataset, float)
        current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
        # Cluster DBSCAN
        clustering = DBSCAN().fit_predict(X=current_numpy_dataset)
        my_clustering = dict()

        for idx, value in enumerate(clustering):
            if not value in my_clustering.keys():
                my_clustering[value] = []
            my_clustering[value].append(idx)
        # Berechne q(s) und speichere diesen Wert
        q_s = subspace_quality_scoring(current_dataset, my_clustering, ml_constraints=ml_constraints, nl_constraints=nl_constraints)
        if q_s > q_best:
            q_best = q_s
            best_subspace = i
        # Vergleiche alle q(s) und wähle q_best(S)

    # entferne besten Subspace aus der Liste C_all1
    candidate_all.remove(best_subspace)

    #candidate_all = [{a,} for a in candidate_all]
    #candidate_all = [set(candidate_all)]


    candidate_i = list()
    # merge mit bestem subspace:
    candidate_i = dolle_funktion(candidate_all, best_subspace)

    for value in candidate_i:
        current_dataset = create_m_dimensional_dataset(dataset, value)
        current_numpy_dataset = np.array(current_dataset, float)
        current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
        clustering = DBSCAN().fit_predict(current_numpy_dataset)
        my_clustering = dict()
        for idx, value2 in enumerate(clustering):
            if not value2 in my_clustering.keys():
                my_clustering[value2] = []
            my_clustering[value2].append(idx)
            # Berechne q(s) und speichere diesen Wert
        q_s = subspace_quality_scoring(current_dataset, my_clustering, ml_constraints=ml_constraints,
                                       nl_constraints=nl_constraints)

        if q_s > q_best:
            q_best = q_s
            best_subspace = value
    for i in best_subspace:
        if i in candidate_all:
            candidate_all.remove(i)
    print(best_subspace)
    candidate_i = dolle_funktion(candidate_all, best_subspace)
    print(candidate_i)
    print(candidate_all)



    #candidate_i = list()
    #for value2 in candidate_all:
     #   help_subspace.append(value2)# Problem von Listen in Listen - wie kann man dies umgehen?
      #  helplist = help_subspace
       # candidate_i.append(helplist)
      #  helplist = list()

    #Cluster DBSCAN mit neuem current dataset
    #TODO: Erstelle m-Dimensionalen Datensatz aus n-Dimensionalem (oder merke dir nur die genutzten Dimensionen im richtigen Datenformat) wobei m < n
    # Clustere zweidimensionale Räume, berechne q(s) sofort --> if q(s)>q_best, dann breche hier ab und vereinige Feature von q(s) mit allen anderen FEatures (3-Dimensionen nun)
    # tue dies so lange bis kein besseres q_s gefunden wurde ODER alle Features genutzt werden


    """startet mit subspaces der größe 1
     setOfCandidateSubspaces hat alle Features (Dimensionen)
     Iteration 2 (Subspace der Größe 2) für jeden Supspace in C_i (Candidate)
     wird q(s) berechnet (nach dem Clustering)
     Wähle S_Best von c_al
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
    return best_subspace



