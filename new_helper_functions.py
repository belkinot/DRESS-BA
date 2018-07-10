import numbers

def distance_heom_metric(point_one, point_two):
    distance = 0
    point_one = point_one[0]
    point_two = point_two[0]
    if isinstance(point_one, str):
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
    #print(current_dataset)
    return current_dataset


def create_m_dimensional_datasets(dataset, dimensions):
    current_dataset = list()
    for value in dataset:
        help_dataset = list()
        for i in dimensions:
            help_dataset.append(value[i])
        current_dataset.append(help_dataset)
    return current_dataset


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