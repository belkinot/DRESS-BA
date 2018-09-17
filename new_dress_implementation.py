"""DRESS Implementierung"""
import math
#from Base.helper_functions import draw_k_dist_line
from new_helper_functions import * #dolle_funktion, create_1_dimensional_datasets, create_m_dimensional_datasets, draw_k_dist_line, k_nearest_neighbour, create_next_candidates
from sklearn.cluster import DBSCAN
#from dress_implementation import *


def subspace_processing(normalized_dataset, ml_constraints, nl_constraints):
    """DRESS Subspace Auswertung"""
    candidate_all = list(range(len(normalized_dataset[0])))  # Anzahl der Dimensionen
    quality_best = 0 # initiale Qualität
    result = create_1_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best)
    #print('Ergebnis', result)
    #initiale 1 dimensionales ergebnis

    quality_best = result[0]
    subspace_best = result[1]
    distance_matrices_sum = result[2]
    if subspace_best in candidate_all:
        candidate_all.remove(subspace_best)
    else:
        subspace_best = candidate_all[0]
        candidate_all.remove(subspace_best)
    print('alle kandidaten', candidate_all)
    next_candidates = dolle_funktion(candidate_all, subspace_best)
    print('next candidates', next_candidates)
    # zweidimensionaler start - iterativ nun
    while True:
        subspace_best_previous = subspace_best
        result = create_m_dimensional_results(next_candidates, ml_constraints, nl_constraints, normalized_dataset, quality_best, subspace_best, distance_matrices_sum)
        quality_best = result[0]
        subspace_best = result[1]
        if subspace_best == subspace_best_previous:
            print('Abbruchsergebnis', 'Beste Qualität', quality_best, subspace_best)
            break
        for i in subspace_best:
            if i in candidate_all:
                candidate_all.remove(i)
        next_candidates_len_previous = len(next_candidates)
        next_candidates = create_next_candidates(candidate_all, subspace_best)
        print('next candidates 2.', next_candidates)
        if len(next_candidates) == next_candidates_len_previous:
            break


    #print(normalized_dataset[0])
    print(subspace_best)
    return normalized_dataset


def create_m_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best, best_subspace, all_distance_matrices):
    """Erstelle M-Dimensionale Ergebnisse"""
    candidate_i = best_subspace
    for i in candidate_all:  # erstelle reduzierte datasets
        distance_matrix, dimensional_dataset = create_m_dimensional_datasets(normalized_dataset, i, all_distance_matrices)
        minpts = round(math.log1p(len(normalized_dataset)))
        epsilon = 0.01  # crazy kneepoint methode
        nearest_neighbour = k_nearest_neighbour(distance_matrix, minpts)
        print('NEAREST NACHBAR', nearest_neighbour)
        epsilon = draw_k_dist_line(nearest_neighbour)
        if epsilon == 0.0:
            epsilon = 0.01
        my_cluster_result = create_clustering_dict(distance_matrix, epsilon, minpts)
        print(my_cluster_result)
        quality = subspace_quality_scoring(distance_matrix, my_cluster_result, ml_constraints, nl_constraints)
        print('Qualitätsmaß', quality)
        if quality > quality_best:
            quality_best = quality
            candidate_i = i
        print(quality_best)
        #print(candidate_i)
    res = quality_best, candidate_i
    return res


def create_1_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best):
    """Erstelle 1-Dimensionale Ergebnisse"""
    candidate_i = -1
    all_distance_matrices = list()
    for i in candidate_all:  # erstelle reduzierte datasets
        distance_matrix, dimensional_dataset = create_1_dimensional_datasets(normalized_dataset, i)
        all_distance_matrices.append(distance_matrix)
        minpts = round(math.log1p(len(normalized_dataset)))
        epsilon = 0.01  # crazy kneepoint methode
        nearest_neighbor = k_nearest_neighbour(distance_matrix, minpts)
        print("NÄCHSTER NACHBAR 1 DIMENSION", nearest_neighbor)
        epsilon = draw_k_dist_line(nearest_neighbor)
        if epsilon == 0.0:
            epsilon = 0.01
        my_cluster_result = create_clustering_dict(distance_matrix, epsilon, minpts)
        #print(my_cluster_result)
        quality = subspace_quality_scoring(distance_matrix, my_cluster_result, ml_constraints, nl_constraints)
        print('Qualitätsmaß', quality)
        if quality > quality_best:
            quality_best = quality
            candidate_i = i
        #print(quality_best)
        #print(candidate_i)
    res = [quality_best, candidate_i, all_distance_matrices]
    return res


def create_clustering_dict(current_numpy_dataset, epsilon, minpts):
    """Erstelle Clusterergebnisse"""
    clustering = DBSCAN(min_samples=minpts, eps=epsilon, metric="precomputed"). \
        fit_predict(current_numpy_dataset)

    my_clustering = dict()
    for idx, value2 in enumerate(clustering):
        if not value2 in my_clustering.keys():
            my_clustering[value2] = []
        my_clustering[value2].append(idx)
    return my_clustering


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
        x_coordinate, y_coordinate = value
        #print(value, x, y, 'NL')
        #d_nl_avg += distance_heom_dbscan(dataset_with_n_features[value[0]], dataset_with_n_features[value[1]])
        d_nl_avg += dataset_with_n_features[x_coordinate][y_coordinate]
    d_nl_avg = d_nl_avg/len(nl_constraints)# Average Distanz des gesamten NL sets??

    for value in ml_constraints:
        x_coordinate, y_coordinate = value
        #d_ml_avg += distance_heom_dbscan(dataset_with_n_features[value[0]],
                                 # dataset_with_n_features[value[1]])
        d_ml_avg += dataset_with_n_features[x_coordinate][y_coordinate]
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
