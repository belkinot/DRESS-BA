import numbers
import numpy as np


def distance_heom_metric(point_one, point_two):
    distance = 0
    point_one = point_one[0]
    point_two = point_two[0]
    if isinstance(point_one, str) or isinstance(point_two, str):
        if point_one == point_two and point_one != '?' and point_two != '?':
            distance += 0
        else:
            distance += 1
    else:
        # if continuous
        if isinstance(point_one, numbers.Number) and isinstance(point_two, numbers.Number):
            distance += abs(point_one - point_two)  # Prüfen ob absolut hier richtig ist
        else:
            distance += 1

    return distance


def distance_heom(point_one, point_two):
    distance = 0
    if isinstance(point_one, str) or isinstance(point_two, str):
        if point_one == point_two and point_one != '?' and point_two != '?':
            distance += 0
        else:
            distance += 1
    else:
        # if continuous
        if isinstance(point_one, numbers.Number) and isinstance(point_two, numbers.Number):
            distance += abs(point_one - point_two)  # Prüfen ob absolut hier richtig ist
        else:
            distance += 1

    return distance

def create_1_dimensional_datasets(dataset, dimension):
    current_dataset = list()
    for value in dataset:
        current_dataset.append(value[dimension])
    #create Distance matrix
    x = len(current_dataset)
    distance_matrix = np.zeros(shape=(x, x))
    for i, _ in enumerate(current_dataset):
        for j, _ in enumerate(current_dataset):
            if j <= i:
                continue
            else:
                distance_matrix[i][j] = distance_heom_dbscan(current_dataset[i], current_dataset[j])
                distance_matrix[j][i] = distance_matrix[i][j]
    #print(distance_matrix, 'DISTANZMATRIX 1 Dimensional')
    print('1 dimensionale dimension', dimension)
    return distance_matrix, current_dataset


def create_m_dimensional_datasets(dataset, dimensions, distance_matrices_sum):
    current_dataset = list()
    #for value in dataset:
    #    help_dataset = list()
    #    for i in dimensions:
    #        help_dataset.append(value[i])
    #    current_dataset.append(help_dataset)
    x = len(dataset)
    distance_matrix = np.zeros(shape=(x, x))
    #for i, _ in enumerate(current_dataset):
    #    for j, _ in enumerate(current_dataset):
    #        if j <= i:
    #            continue
    #        else:
    #            distance_matrix[i][j] = distance_heom_dbscan(current_dataset[i], current_dataset[j])
    #            distance_matrix[j][i] = distance_matrix[i][j]
    for i in dimensions:
        print(i, 'dimensions', dimensions)
        #print('distanzmatrix' , distance_matrices_sum)
        distance_matrix += distance_matrices_sum[i]
    print('distanzmatrix', distance_matrix)
    return distance_matrix, current_dataset


def dolle_funktion(canditate_all, wert_objekt):
    """ Erstelle eine Liste von Tupeln"""

    res = [(canditate,) + (wert_objekt,) for canditate in canditate_all]
    return res

def create_next_candidates(candidate_all, best_subspace):
    """ erstellt die Kandidatenliste"""
    candidate_i = list()
    for i in candidate_all:
        temp_d = best_subspace + (i,)
        candidate_i += (temp_d,)
    return candidate_i

def distance_heom_dbscan(erster, zweiter):
    distance = 0
    counter = 0
    #print(type(erster), 'TYPE erster heom dbscan')
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

