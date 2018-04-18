"""Main-Klasse"""

import time
import numpy as np
from sklearn.datasets import load_iris, load_breast_cancer
from sklearn import preprocessing
from Base.helper_functions import normalize_features_numpy
from scipy.io import arff
from io import StringIO
from dress_implementation import subspace_processing_and_cluster_generation

if __name__ == '__main__':

    START_TIME = time.time()

    irisdataset = load_iris()



    X = irisdataset.data
    Y = irisdataset.target

    print("Anzahl der Datensätze", len(X))
    print("Anzah der Dimensionen", len(X[0]))

    # print(X[0], "X an stelle 0")

    #normalized_X_self = normalize_features(X)
    normalized_X = preprocessing.normalize(X, 'max', 0)
    #normalized_X_self_numpy = normalize_features_numpy(X)

    # for i in range(len(normalized_X)):
    #    print(normalized_X_self_numpy[i] - normalized_X[i])
    ml_constraint = [(1, 2), (140, 141), (30, 31)]
    nl_constraint = [(1, 140), (2, 83)]

    #print()
    subspace_processing_and_cluster_generation(normalized_X, ml_constraint, nl_constraint)

    """
    
    f = "ship.csv"
    #data = np.array(np.empty(), )
    data = []
    with open(f, 'r') as file:
        for line in file.readlines():
            #temp = eval(line)
            temp = line.split(',')
            temp = temp[3:]
            data.append(temp)

    print(data[0])
    print(data[0][4])
    """
    print("My Programm took", time.time()-START_TIME, "to run")
