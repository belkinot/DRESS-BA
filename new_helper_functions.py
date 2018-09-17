"""Hilfsfunktionen"""
import numbers
import numpy as np


def distance_heom_metric(point_one, point_two):
    """Distanzmetrik HEOM"""
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


def k_nearest_neighbour(distance_matrix, parameter_k):
    """k-Nächster Nachbar"""
    nearest_neighbour_list = list()
    for i in distance_matrix:
        i.sort()
        nearest_neighbour_list.append(i[parameter_k])
    return nearest_neighbour_list


def draw_k_dist_line(list_of_elements):
    """m-Dist-Line für Knee-Point-Methode"""
    list_of_elements_new = list_of_elements
    list_of_elements_new.sort(reverse=True)
    point_b = list_of_elements_new[0]
    point_a = list_of_elements_new[-1]  # letzter Eintrag
    # y = m*x+b
    steigung = (point_a - point_b) / len(list_of_elements)

    knee_point = list()
    for idx, value in enumerate(list_of_elements_new):
        my_idx = idx
        point_one = np.array([my_idx, value])
        y_coordinate = steigung * idx + point_b
        point_two = np.array([my_idx, y_coordinate])
        knee_point.append((euclidean_distance(point_one, point_two), idx))
        #knee_point.append((distance_heom(point_one, point_two), idx))

    print("KNIEPUNKT", knee_point)
    knee_point.sort()
    print("KNIEPUNKT SORTIER", knee_point)
    epsilon = list_of_elements_new[knee_point[2][1]]
    print("EPSILON", epsilon)
    return epsilon


def euclidean_distance(point_one, point_two):
    """Berechnet die euklidische Distanz von zwei Punkten"""
    return np.linalg.norm(point_one-point_two)


def distance_heom(point_one, point_two):
    """nochmal distanzmaß HEOM?"""
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
    """Erstellt 1 Dimensionale Datensätze aus mehrdimensionalen"""
    current_dataset = list()
    for value in dataset:
        current_dataset.append(value[dimension])
    #create Distance matrix
    dim = str(dimension)
    if dimension > 65:
        x_quadratic_matrix = len(current_dataset)
        distance_matrix = np.zeros(shape=(x_quadratic_matrix, x_quadratic_matrix))
        for i, _ in enumerate(current_dataset):
            for j, _ in enumerate(current_dataset):
                if j <= i:
                    continue
                else:
                    distance_matrix[i][j] = distance_heom_dbscan(current_dataset[i], current_dataset[j])
                    distance_matrix[j][i] = distance_matrix[i][j]
        #print(distance_matrix, 'DISTANZMATRIX 1 Dimensional')
        dataname = 'Distanzmatrix/Distanzmatrix_Dimension_' + dim
        np.save(dataname, distance_matrix)
    else:
        dmat = np.load('Distanzmatrix/Distanzmatrix_Dimension_'+ dim + '.npy')
        distance_matrix = dmat
        del dmat
    print('1 dimensionale dimension', dimension)
    return distance_matrix, current_dataset


def create_m_dimensional_datasets(dataset, dimensions, distance_matrices_sum):
    """Erstellt m-dimensionale Datensätze aus mehrdimensionalen"""
    current_dataset = list()
    #for value in dataset:
    #    help_dataset = list()
    #    for i in dimensions:
    #        help_dataset.append(value[i])
    #    current_dataset.append(help_dataset)
    x_qudratic_matrix = len(dataset)
    distance_matrix = np.zeros(shape=(x_qudratic_matrix, x_qudratic_matrix))
    #for i, _ in enumerate(current_dataset):
    #    for j, _ in enumerate(current_dataset):
    #        if j <= i:
    #            continue
    #        else:
    #            distance_matrix[i][j] = distance_heom_dbscan(current_dataset[i], current_dataset[j])
    #            distance_matrix[j][i] = distance_matrix[i][j]
    for i in dimensions:
        print(i, 'dimensions', dimensions)
        dim = str(i)
        #print('distanzmatrix' , distance_matrices_sum)
        d_mat = np.load('Distanzmatrix/Distanzmatrix_Dimension_' + dim + '.npy')
        distance_matrix += d_mat
        del d_mat
        #distance_matrix += distance_matrices_sum[i]
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
    """Distanzmaß HEOM für DBSCAN von Sklearn"""
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
