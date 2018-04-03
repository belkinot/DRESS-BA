"""Hilfsfunktionen"""
import numbers
import math


#Distanzfuntkionen



#sicherstellen dass x und y gleiche länge haben len(x) == len(y)
def distance_heom(erster, zweiter):
    """Berechne die Distanz nach dem HEOM-Maß: Input: x, y als Listen von Features"""
    distance = 0
    for counter, _ in enumerate(erster):
        #if nominal
        if isinstance(erster[counter], str):
            if erster[counter] == zweiter[counter]:
                distance += 0
            else:
                distance += 1
        #if continuous
        else:
            if isinstance(erster[counter], numbers.Number) \
                    and isinstance(zweiter[counter], numbers.Number):
                distance += erster[counter] - zweiter[counter]
            else:
                distance += 1
    return distance



def k_nearest_neighbour_list(dataset, parameter_k):
    """Gibt eine Liste mit den Distanzen des k-ten Nachbars von jedem Punkt aus.
    Index der Liste bezeichnet den Punkt im Datensatz"""
    neighbours = list()
    for _, value in enumerate(dataset):
        mydist = [[euclidean_distance(value, value2), count2] for count2, value2 in enumerate(dataset)]
        mydist.sort()
        neighbours.append([x[1] for x in mydist[parameter_k]])
    return neighbours


def euclidean_distance(point_one, point_two):
    """Berechnet die euklidische Distanz von zwei Punkten"""
    return math.sqrt(pow((point_one - point_two), 2))

#TODO: Evaluierungsmetriken Sensitivity, specificity, accuracy, AUC, F-Measure"""
