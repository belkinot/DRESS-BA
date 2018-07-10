import math
import numpy as np
#from Base.helper_functions import *
from new_helper_functions import *
from sklearn.cluster import DBSCAN
#from dress_implementation import *


def subspace_processing(normalized_dataset, ml_constraints, nl_constraints):
    candidate_all = list(range(len(normalized_dataset[0])))  # Anzahl der Dimensionen
    quality_best = 0 # initiale Qualität
    result = create_1_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best)
    print('Ergebnis', result)
    #initiale 1 dimensionales ergebnis

    quality_best = result[0]
    subspace_best = result[1]
    candidate_all.remove(subspace_best)
    print('alle kandidaten', candidate_all)
    next_candidates = dolle_funktion(candidate_all, subspace_best)
    print('next candidates', next_candidates)
    # zweidimensionaler start - iterativ nun
    while True:
        result = create_m_dimensional_results(next_candidates, ml_constraints, nl_constraints, normalized_dataset, quality_best, subspace_best)
        quality_best = result[0]
        subspace_best = result[1]
        for i in subspace_best:
            if i in candidate_all:
                candidate_all.remove(i)
        next_candidates_len_previous = len(next_candidates)
        next_candidates = create_next_candidates(candidate_all, subspace_best)
        print('next candidates 2.', next_candidates)
        if len(next_candidates) == next_candidates_len_previous:
            break


    print(normalized_dataset[0])
    print(subspace_best)
    return normalized_dataset


def create_m_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best, best_subspace):
    candidate_i = best_subspace
    for i in candidate_all:  # erstelle reduzierte datasets
        dimensional_dataset = create_m_dimensional_datasets(normalized_dataset, i)
        minpts = round(math.log1p(len(normalized_dataset)))
        epsilon = 0.01  # crazy kneepoint methode
        current_numpy_dataset = np.array(dimensional_dataset, float)
        current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
        my_cluster_result = create_clustering_dict(current_numpy_dataset, epsilon, minpts)
        print(my_cluster_result)
        quality = subspace_quality_scoring(dimensional_dataset, my_cluster_result, ml_constraints, nl_constraints)
        print('Qualitätsmaß', quality)
        if quality > quality_best:
            quality_best = quality
            candidate_i = i
        print(quality_best)
        #print(candidate_i)
        res = quality_best, candidate_i
    return res


def create_1_dimensional_results(candidate_all, ml_constraints, nl_constraints, normalized_dataset, quality_best):
    candidate_i = -1
    for i in candidate_all:  # erstelle reduzierte datasets
        dimensional_dataset = create_1_dimensional_datasets(normalized_dataset, i)
        minpts = round(math.log1p(len(normalized_dataset)))
        epsilon = 0.01  # crazy kneepoint methode
        current_numpy_dataset = np.array(dimensional_dataset, float)
        current_numpy_dataset = current_numpy_dataset.reshape(-1, 1)
        my_cluster_result = create_clustering_dict(current_numpy_dataset, epsilon, minpts)
        #print(my_cluster_result)
        quality = subspace_quality_scoring(dimensional_dataset, my_cluster_result, ml_constraints, nl_constraints)
        #print('Qualitätsmaß', quality)
        if quality > quality_best:
            quality_best = quality
            candidate_i = i
        #print(quality_best)
        #print(candidate_i)
        res = [quality_best, candidate_i]
    return res


def create_clustering_dict(current_numpy_dataset, epsilon, minpts):
    """

    :param current_numpy_dataset:
    :param epsilon:
    :param minpts:
    :return:
    """
    clustering = DBSCAN(min_samples=minpts, eps=epsilon, metric=distance_heom_metric). \
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
        d_nl_avg += distance_heom_dbscan(dataset_with_n_features[value[0]],
                                  dataset_with_n_features[value[1]])
    d_nl_avg = d_nl_avg/len(nl_constraints)# Average Distanz des gesamten NL sets??

    for value in ml_constraints:
        d_ml_avg += distance_heom_dbscan(dataset_with_n_features[value[0]],
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

def distance_heom_dbscan(erster, zweiter):
    distance = 0
    counter = 0
    if isinstance(erster, list):
        for value in erster:
            if isinstance(value, str) or isinstance(zweiter[counter], str) and value != '?' and zweiter[counter] != '?':
                if value == zweiter[counter]:
                    distance += 0
                else:
                    distance += 1
            else:
                if isinstance(value, numbers.Number) and isinstance(zweiter[counter], numbers.Number):
                    distance += abs(value - zweiter[counter])
                else:
                    distance += 1
            counter += 1

    if isinstance(erster, str):
        if erster == zweiter and erster != '?' and zweiter != '?':
            distance += 0
        else:
            distance += 1
    else:
    # if continuous
        if isinstance(erster, numbers.Number) and isinstance(zweiter, numbers.Number):
            distance += abs(erster - zweiter)  # Prüfen ob absolut hier richtig ist
        else:
            distance += 1
    return distance


