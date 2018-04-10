"""Main-Klasse"""

import time
from sklearn.datasets import load_iris
from sklearn import preprocessing
from Base.helper_functions import normalize_features, normalize_features_numpy
from dress_implementation import *

if __name__ == '__main__':

    START_TIME = time.time()
    irisdataset = load_iris()

    X = irisdataset.data
    Y = irisdataset.target



    # print(X[0], "X an stelle 0")

    #normalized_X_self = normalize_features(X)
    normalized_X = preprocessing.normalize(X, 'max', 0)
    normalized_X_self_numpy = normalize_features_numpy(X)

    # for i in range(len(normalized_X)):
    #    print(normalized_X_self_numpy[i] - normalized_X[i])

    ml_constraint = [(1,2), (140,141), (30,31)]
    nl_constraint = [(1,140), (2,83)]

    #print(normalized_X_self_numpy)
    subspace_processing_and_cluster_generation(normalized_X_self_numpy, ml_constraint, nl_constraint)


    print("My Programm took", time.time()-START_TIME, "to run")
