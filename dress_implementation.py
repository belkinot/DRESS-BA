"""Implementation des DRESS-Algorithmus"""
import math
import numpy as np
from sklearn.cluster import DBSCAN
from Base.helper_functions import distance_heom, k_nearest_neighbour_list, draw_k_dist_line, distance_heom_dbscan

def subspace_processing_dress(dataset, ml_constraints, nl_constraints):
    """erstellt die Subspaces und die Cluster"""
    q_best = 0  # initiales q_best
    best_subspace = 0  # initialer bester subspace
    candidate_all = list(range(len(dataset[0])))  # Anzahl der Dimensionen

    # erstelle 1-Dimensionalen Datensatz - noch auslagerbar in eine Funktion?(
    q_best = create_1_dimensional_result(dataset, candidate_all, q_best, ml_constraints, nl_constraints)
    # entferne besten Subspace aus der Liste C_all1
    print(best_subspace, "bester supspace 1 Dimension")
    candidate_all.remove(best_subspace)
    print(candidate_all, "Initial Candidate all")
    # merge mit bestem subspace:
    candidate_i = dolle_funktion(candidate_all, best_subspace)
    # ab hier 2 bis n - Dimensionale Datensätze - rekursiv
    best_subspace, candidate_i = dress_iteration(best_subspace, candidate_all, candidate_i, dataset,
                                                 ml_constraints, nl_constraints, q_best)

    return best_subspace

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
Für jeden Subspace S_best vereinigt S* in C_i wird S* von C_all entfernt und 
dann S_best von C_all
Iteration stoppt, wenn C_all leer ist"""


def create_1_dimensional_result(dataset, candidate_all, q_best, ml_constraints, nl_constraints):
    """ Berechnet das Qualitätsmaß für die erste Iteration (1-Dimensional)  """
    for i in candidate_all:
        current_dataset = list()
        for value in dataset:
            if value[i] != '?':
                current_dataset.append(value[i])
            else:
                current_dataset.append(9999)
        current_numpy_dataset = np.array(current_dataset, float)
        current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
        # Cluster DBSCAN
        minpts = round(math.log1p(len(dataset)))
        epsilon = draw_k_dist_line(k_nearest_neighbour_list(current_numpy_dataset, minpts))
        my_clustering = create_clustering_dict(current_numpy_dataset, minpts, epsilon)
        # Berechne q(s) und speichere diesen Wert
        q_s = subspace_quality_scoring(current_dataset, my_clustering,
                                       ml_constraints=ml_constraints, nl_constraints=nl_constraints)
        print(q_s, "Qualitätsmaß")
        if q_s > q_best:
            q_best = q_s
            # best_subspace = i wozu?
    return q_best


def subspace_quality_scoring(dataset_with_n_features, clustering, ml_constraints, nl_constraints):
    """Scores Quality of our Subspace"""
    # ml-constraints (Tupel von Indizes die verbunden sein müssen)

    # Prüfe ob ml constraints in einem Cluster sind
    ml_sat = check_ml_constraints(ml_constraints, clustering)
    # Prüfe ob nl_constraints in verschiedenen Clustern sind
    nl_sat = check_nl_constraints(nl_constraints, clustering)

    q_cons = (ml_sat + nl_sat) / (len(ml_constraints) + len(nl_constraints))

    d_nl_avg = 0
    d_ml_avg = 0

    for value in nl_constraints:
        # Indizes 0 und 1 für das korrekte Ansprechen der Tupelpaare
        d_nl_avg += distance_heom_dbscan(dataset_with_n_features[value[0]],
                                  dataset_with_n_features[value[1]])
    d_nl_avg = d_nl_avg/len(nl_constraints)# Average Distanz des gesamten NL sets??

    for value in ml_constraints:
        d_ml_avg += distance_heom(dataset_with_n_features[value[0]],
                                  dataset_with_n_features[value[1]])
    d_ml_avg = d_ml_avg/len(ml_constraints)

    q_dist = d_nl_avg - d_ml_avg
    # Errechne Qualität

    quality = q_cons * q_dist

    return quality


def check_nl_constraints(constraints, clustering):
    """Prüft wie viele NL-Constraints erfüllt sind"""
    # Annahme: Clustering ist eine Liste von Listen mit Indizes ((1,2,5), (3,4), (6,9), (7,8))
    constraint_sat = 0

    for constraint in constraints:
        for key in clustering:
            if constraint[0] in clustering[key]:
                if constraint[1] not in clustering[key]:
                    constraint_sat += 1

    return constraint_sat


def check_ml_constraints(constraints, clustering):
    """Prüft wie viele ML-Constraints erfüllt sind"""
    # Annahme: Clustering ist eine Liste von Listen mit Indizes ((1,2,5), (3,4), (6,9), (7,8))
    constraint_sat = 0

    for constraint in constraints:
        for key in clustering:
            if constraint[0] in clustering[key]:
                if constraint[1] in clustering[key]:
                    constraint_sat += 1

    return constraint_sat


def dolle_funktion(canditate_all, wert_objekt):
    """ Erstelle eine Liste von Tupeln"""

    res = [(canditate,) + (wert_objekt,) for canditate in canditate_all]
    return res


def dress_iteration(best_subspace, candidate_all, candidate_i, dataset,
                    ml_constraints, nl_constraints, q_best):
    """Iteration von Dress - Rekursiv """
    q_old_best = q_best
    print(candidate_i, "Candidate i ")
    print("mehrdimensionale Datensätze")
    for candidate_value in candidate_i:
        my_clustering_temp, current_dataset = create_clustering(dataset, candidate_value)
        q_s = subspace_quality_scoring(current_dataset, my_clustering_temp,
                                       ml_constraints, nl_constraints)
        if q_s > q_best:
            q_best = q_s
            best_subspace = candidate_value
        # Abbruchkriterum - Candidates sind so mächtig wie die Anzahl der Dimensionen -
        # Entspricht Clustering auf dem gesamtem Datensatz
        print(best_subspace, "Bester Subspace")

        # TODO: schmiert hier ab, wenn kein 2 Dimensionaler besserer Subspace gefunden wird...
    if len(candidate_i[0]) != len(dataset[0]):
        for i in best_subspace:
            if i in candidate_all:
                candidate_all.remove(i)
            else:
                if q_old_best == q_best:
                    return best_subspace, candidate_i
        if candidate_all: # vorher len(candidate_all) > 0
            candidate_i = create_candidate_i(candidate_all, best_subspace)
            print(best_subspace, "Best Subspace")
            print(candidate_all, "Candidate_all")
            print(candidate_i, "Candidates")
            return dress_iteration(best_subspace, candidate_all, candidate_i, dataset,
                                   ml_constraints, nl_constraints, q_best)
    else:
        return best_subspace, candidate_i



def create_m_dimensional_dataset(dataset_n_dimensions, candidate_i):
    """Erstellt ein m-Dimensionales Dataset aus einem n-Dimensionalen m < n"""
    dataset_with_m_dimensions = [[] for _ in range(dataset_n_dimensions.shape[0])]
    for value in candidate_i:
        for idx, _ in enumerate(dataset_n_dimensions):
            dataset_with_m_dimensions[idx].append(dataset_n_dimensions[idx][value])

    return dataset_with_m_dimensions


def create_candidate_i(candidate_all, best_subspace):
    """ erstellt die Kandidatenliste"""
    candidate_i = list()
    for i in candidate_all:
        temp_d = best_subspace + (i,)
        candidate_i += (temp_d,)
    return candidate_i


def create_clustering(dataset, candidate_i_value):
    """Erstelle aus dem ursprünglichen Datensatz und dem Kandidaten einen neuen Datensatz
     und clustere diesen"""

    current_dataset = create_m_dimensional_dataset(dataset, candidate_i_value)
    current_numpy_dataset = np.array(current_dataset, float)
    current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
    minpts = round(math.log1p(len(dataset)))
    epsilon = draw_k_dist_line(k_nearest_neighbour_list(current_numpy_dataset, minpts))
    my_clustering = create_clustering_dict(current_numpy_dataset, epsilon, minpts)

    return my_clustering, current_dataset


def create_clustering_dict(current_numpy_dataset, epsilon, minpts):
    """

    :param current_numpy_dataset:
    :param epsilon:
    :param minpts:
    :return:
    """
    clustering = DBSCAN(min_samples=minpts, eps=epsilon, metric=distance_heom_dbscan). \
        fit_predict(current_numpy_dataset)

    my_clustering = dict()
    for idx, value2 in enumerate(clustering):
        if not value2 in my_clustering.keys():
            my_clustering[value2] = []
        my_clustering[value2].append(idx)
    return my_clustering
