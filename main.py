"""Main-Klasse"""

import time
import numbers
import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn import preprocessing
from Base.helper_functions import normalize_features_numpy, normalize_features, format_dataset
from dress_implementation import subspace_processing_dress




if __name__ == '__main__':

    START_TIME = time.time()

    irisdataset = load_iris()



    X = irisdataset.data
    Y = irisdataset.target

    print("Anzahl der Datensätze", len(X))
    print("Anzah der Dimensionen", len(X[0]))

    # print(X[0], "X an stelle 0")

    normalized_X_self = normalize_features(X)
    #normalized_X = preprocessing.normalize(X, 'max', 0)
    #normalized_X_self_numpy = normalize_features_numpy(X)

    # for i in range(len(normalized_X)):
    #    print(normalized_X_self_numpy[i] - normalized_X[i])

    ml_constraint = [(1, 2), (140, 141), (30, 31)]
    nl_constraint = [(1, 140), (2, 83)]

    #print()
    subspace_processing_dress(normalized_X_self, ml_constraint, nl_constraint)

    """
    
    f = "ship.csv"
    #data = np.array(np.empty(), )
    data = []
    with open(f, 'r') as file:
        for line in file.readlines():
            #temp = eval(line)
            temp = line.split(",")
            temp1 = temp[3:4]
            temp2 = temp[145:148]
            #temp2 = temp[145:201]
            #temp3 = temp[395:400]
            templist = temp1+temp2#+temp3
            data.append(templist)



    format_dataset(data)

    print(data[0])
    print(len(data), "Datenpunkte")
    print(len(data[0]), "Dimensionen")

    #normalized_X = preprocessing.normalize(data, 'max', 0)
    max_data = data[0][1]
    print(max_data)
    for value in data:
        if isinstance(value[1], numbers.Number) and max_data < value[1]:
            print(value[1])
            max_data = value[1]

    normalized_X = normalize_features(data)

    print(normalized_X[0])
    subspace_processing_dress(normalized_X, ml_constraint, nl_constraint)
    """
    print("My Programm took", time.time()-START_TIME, "to run")
