"""Hilfsfunktionen"""
import numbers



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


"""TODO: Evaluierungsmetriken Sensitivity, specificity, accuracy, AUC, F-Measure"""
