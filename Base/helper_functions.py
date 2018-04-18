"""Hilfsfunktionen"""
import numbers
import numpy as np


def normalize_features(dataset):
    """normalisiere alle Features
        Bedenke letzten Eintrag im Dataset - Clusterzugehörigkeit? ML Constraint?"""

    normalized_dataset = dataset
    # for i in range(len(dataset[0])):
     # max_value = max(dataset, key=lambda x: x[i])
    max_value = list(dataset[0])
    # performanteres Maximum finden?
    for count, value in enumerate(dataset):
        for count2, value2 in enumerate(value):
            # Sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number) and max_value[count2] <= value2:
                # get my maximum value
                max_value[count2] = value2

    for count, value in enumerate(dataset):
        for count2, _ in enumerate(value):
            # erneut sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number):
                normalized_dataset[count][count2] = dataset[count][count2]/max_value[count2]
    return normalized_dataset


def normalize_features_numpy(dataset):
    """normalisiere alle Features
        Bedenke letzten Eintrag im Dataset - Clusterzugehörigkeit? ML Constraint?"""

    normalized_dataset = dataset
    max_value = dataset.max(0) #Krasse Numpy-Array Magic
    print(max_value, "max value")
    for count, value in enumerate(dataset):
        for count2, _ in enumerate(value):
            # erneut sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number):
                normalized_dataset[count][count2] = dataset[count][count2]/max_value[count2]
    return normalized_dataset

#Distanzfuntkionen


def distance_heom(erster, zweiter):
    """Berechne die Distanz nach dem HEOM-Maß: Input: x, y als Listen von Features
    sicherstellen dass x und y gleiche länge haben len(x) == len(y)
    features müssen normalisiert sein [0,1]"""
    distance = 0

    #numpy_64 float
    if isinstance(erster, str):
        if erster == zweiter:
            distance += 0
        else:
            distance += 1
    else:
        if isinstance(erster, numbers.Number) and isinstance(zweiter, numbers.Number):
            distance += abs(erster - zweiter)
        else:
            distance += 1

    """  
    for counter, value in enumerate(erster):
        # if nominal - true und false
        if isinstance(erster[counter], str):
            # distance += int(erster[counter] != zweiter[counter])
            if erster[counter] == zweiter[counter]:
                distance += 0
            else:
                distance += 1
        # if continuous
        else:
            if isinstance(erster[counter], numbers.Number) \
                    and isinstance(zweiter[counter], numbers.Number):
                distance += erster[counter] - zweiter[counter]
            else:
                distance += 1"""
    return distance


def k_nearest_neighbour_list(dataset, parameter_k):
    """Gibt eine Liste mit den Distanzen des k-ten Nachbars von jedem Punkt aus.
    Index der Liste bezeichnet den Punkt im Datensatz"""
    neighbours = list()
    neighbours_distances = list()
    for value in dataset:
        mydist = [[euclidean_distance(value, value2), count2] for count2, value2 in enumerate(dataset)]
        mydist.sort()
        neighbours.append(mydist[parameter_k])
    # ab hier Erweiterung um k-Dist-Graph erstellung zu ermöglichen
    # neighbours_distances.append([y[0] for y in mydist[parameter_k]])
    #neighbours = list(zip(neighbours_distances, neighbours))
    # sortiere Reverse um den K-Dist-Graph zu erstellen
    neighbours.sort(reverse=True)
    return neighbours


def draw_k_dist_line(list_of_elements):
    """Berechnet den Epsilon Parameter mithilfe der knee_point Methode"""
    list_of_elements_new = list()
    for value in list_of_elements:
        list_of_elements_new.append(value[0])
    point_b = list_of_elements_new[0]
    point_a = list_of_elements_new[-1] # letzter Eintrag
    # y = m*x+b
    steigung = (point_a-point_b)/len(list_of_elements)

    knee_point = list()
    for idx, value in enumerate(list_of_elements_new):
        my_idx = idx
        point_one = np.array([my_idx, value])
        y_coordinate = steigung * value + point_b
        point_two = np.array([my_idx, y_coordinate])
        knee_point.append((euclidean_distance(point_one, point_two), idx))

    knee_point.sort()
    epsilon = list_of_elements[knee_point[2][1]][0]
    print("EPSILON", epsilon)
    return epsilon


def euclidean_distance(point_one, point_two):
    """Berechnet die euklidische Distanz von zwei Punkten"""
    return np.linalg.norm(point_one-point_two)

#TODO: Evaluierungsmetriken Sensitivity, specificity, accuracy, AUC, F-Measure"""


def eval_sensitivity(clustering):
    """Sensitivity"""
    return clustering
