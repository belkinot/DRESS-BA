"""Main-Klasse"""

import time
from sklearn.datasets import load_iris
from sklearn import preprocessing
from Base.helper_functions import normalize_features, normalize_features_numpy


if __name__ == '__main__':

    START_TIME = time.time()
    iris = load_iris()

    X = iris.data
    Y = iris.target

    print(X[0], "X an stelle 0")

    #normalized_X_self = normalize_features(X)
    normalized_X = preprocessing.normalize(X,'max',0)
    normalized_X_self_numpy = normalize_features_numpy(X)

    for i in range(len(normalized_X)):
        print(normalized_X_self_numpy[i]-normalized_X[i])




    print("My Programm took", time.time()-START_TIME, "to run")
