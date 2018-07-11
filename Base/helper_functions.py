"""Hilfsfunktionen"""
import numbers
import numpy as np


def normalize_features(dataset):
    """normalisiere alle Features
        Bedenke letzten Eintrag im Dataset - Clusterzugehörigkeit? ML Constraint?
        Input: dataset
        Return: dataset normalisiert """

    normalized_dataset = dataset
    # for i in range(len(dataset[0])):
     # max_value = max(dataset, key=lambda x: x[i])
    max_value = list(dataset[0])
    # performanteres Maximum finden?
    for count, value in enumerate(dataset):
        for count2, value2 in enumerate(value):
            # Sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number) and \
                    isinstance(value2, numbers.Number) and max_value[count2] <= value2:
                # get my maximum value
                max_value[count2] = value2

    for count, value in enumerate(dataset):
        for count2, _ in enumerate(value):
            # erneut sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number) and \
                    isinstance(dataset[count][count2], numbers.Number):
                normalized_dataset[count][count2] = dataset[count][count2]/max_value[count2]
    return normalized_dataset


def normalize_features_numpy(dataset):
    """normalisiere alle Features
        Bedenke letzten Eintrag im Dataset - Clusterzugehörigkeit? ML Constraint?"""

    #normalized_dataset = dataset
    normalized_dataset = np.array(dataset, dtype=float)
    max_value = dataset.max(0) #Krasse Numpy-Array Magic
    # print(max_value, "max value")
    for count, value in enumerate(dataset):
        for count2, _ in enumerate(value):
            # erneut sicherstellen, dass es Zahlenwerte sind
            if isinstance(max_value[count2], numbers.Number):
                normalized_dataset[count][count2] = dataset[count][count2]/max_value[count2]
    return normalized_dataset

#Distanzfuntkionen
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



def distance_heom(erster, zweiter):
    """Berechne die Distanz nach dem HEOM-Maß: Input: x, y als Listen von Features
    sicherstellen dass x und y gleiche länge haben len(x) == len(y)
    features müssen normalisiert sein [0,1]"""
    distance = 0
    counter = 0
    if type(erster) != np.ndarray:
        erster = np.asarray(erster, dtype=float)
    if type(zweiter) != np.ndarray:
        zweiter = np.asarray(zweiter, dtype=float)
    #print(type(erster), "erster type")
    #zweiter = list(zweiter)
    #print(erster.size, "Datentyp vom ersten Value")
    # numpy_64 float
    # if nominal - true and false
    # if len(erster) == len(zweiter):
    """if isinstance(erster, str):
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

    """

    if erster.size < 2:
        if isinstance(erster, str):
            if erster == zweiter:
                distance += 0
            else:
                distance += 1
        if isinstance(erster, numbers.Number) and isinstance(zweiter, numbers.Number):
            distance += erster - zweiter
        else:
            distance += 1
    else:
        for idx, _ in enumerate(erster):
            # if nominal - true und false
                if isinstance(erster[idx], str):
                # distance += int(erster[counter] != zweiter[counter])
                    if erster[idx] == zweiter[idx]:
                        distance += 0
                    else:
                        distance += 1
            # if continuous
                else:
                    if isinstance(erster[idx], numbers.Number) and isinstance(zweiter[idx], numbers.Number):
                        distance += erster[idx] - zweiter[idx]
                    else:
                        distance += 1
        #print(distance, 'distanz heom')
    return distance


def k_nearest_neighbour_list(dataset, parameter_k):
    """Gibt eine Liste mit den Distanzen des k-ten Nachbars von jedem Punkt aus.
    Index der Liste bezeichnet den Punkt im Datensatz"""
    neighbours = list()
    # neighbours_distances = list()
    for value in dataset:
        #if isinstance(value, numbers.Number): eigentlich kann ich doch nur continous werte clustern oder?
        # mydist = [[euclidean_distance(value, value2), count2] for count2, value2 in enumerate(dataset)]
        mydist = [[distance_heom(value, value2), count2] for count2, value2 in enumerate(dataset)]
        mydist.sort()
        neighbours.append(mydist[parameter_k])
    # ab hier Erweiterung um k-Dist-Graph erstellung zu ermöglichen
    # neighbours_distances.append([y[0] for y in mydist[parameter_k]])
    # neighbours = list(zip(neighbours_distances, neighbours))
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
        #knee_point.append((euclidean_distance(point_one, point_two), idx))
        knee_point.append((distance_heom(point_one, point_two), idx))


    knee_point.sort()
    epsilon = list_of_elements[knee_point[2][1]][0]
    print("EPSILON", epsilon)
    return epsilon


def euclidean_distance(point_one, point_two):
    """Berechnet die euklidische Distanz von zwei Punkten"""
    return np.linalg.norm(point_one-point_two)

def format_dataset(data):
    """Formatierte den SHIP-Datensatz
    Wandele Zahlenwerte in Floats um, den Rest behalte als String"""
    zahlenwerte = 0
    keine_zahlenwerte = 0
    for value in data:
        for idx, value2 in enumerate(value):
            try:
                float(value2)
                value[idx] = float(value2)
                zahlenwerte += 1
            except ValueError:
                keine_zahlenwerte += 1
                # if value2 == '?':
                #    value[idx] = float('inf')
                # else:
                value[idx] = value2.strip('\'')
                #if value[idx] == '?':
                 #   value[idx] = None
                """
                if value[idx] == 'J':
                    value[idx] = 1
                if value[idx] == 'N':
                    value[idx] = 0
                if isinstance(value[idx], str):
                    #print('string konvertieren und stunden')
                    if ':' in value[idx]:
                        temp = value[idx].split(':')
                        temp = int(temp[0])*60*60 + int(temp[1]) * 60 + int(temp[2])
                        value[idx] = temp
               """
    print(zahlenwerte, 'Digits', keine_zahlenwerte, 'keine digits')

#TODO: Evaluierungsmetriken Sensitivity, specificity, accuracy, AUC, F-Measure"""


def eval_sensitivity(clustering):
    """Sensitivity"""
    return clustering
