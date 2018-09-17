"""Main-Klasse"""

import time
import numbers
from sklearn.datasets import load_iris# , load_wine
#from sklearn import preprocessing
from Base.helper_functions import normalize_features, normalize_features_numpy, format_dataset, distance_heom
#from dress_implementation import subspace_processing_dress, create_m_dimensional_dataset
from new_dress_implementation import subspace_processing



if __name__ == '__main__':

    START_TIME = time.time()
    ML_CONSTRAINT = [(1, 2), (140, 141), (30, 31), (1000,2583)]
    NL_CONSTRAINT = [(1, 140), (2, 83), (1001,2584), (50,250)]

    IRIS_DATASET = load_iris()

    X = IRIS_DATASET.data
    Y = IRIS_DATASET.target

    print("Anzahl der Datensätze", len(X))
    print("Anzah der Dimensionen", len(X[0]))

    # print(X[0], "X an stelle 0")

    #NORMALIZED_X_SELF = normalize_features(X)
    #normalized_X = preprocessing.normalize(X, 'max', 0)
    normalized_x_self_numpy = normalize_features_numpy(X)


    #for i in range(len(normalized_X)):
     #   print(NORMALIZED_X_SELF[i] - normalized_X[i])
    #print()
    #subspace_processing(normalized_X_self_numpy, ML_CONSTRAINT, NL_CONSTRAINT)
    #subspace_processing_dress(normalized_X_self_numpy, ML_CONSTRAINT, NL_CONSTRAINT)


    f = "ship.csv"
    #data = np.array(np.empty(), )
    data = []
    with open(f, 'r') as file:
        for line in file.readlines():
            #temp = eval(line)
            temp = line.split(",")
            temp1 = temp[3:4]
            #temp2 = temp[145:185]
            temp2 = temp[145:201]
            temp3 = temp[395:400]
            templist = temp1+temp2+temp3
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
            #print(value[1])
            max_data = value[1]

    normalized_X = normalize_features(data)

    print(normalized_X[0], 'EINS')

    #subspace_processing_dress(normalized_X, ML_CONSTRAINT, NL_CONSTRAINT)
    subspace_processing(normalized_X, ML_CONSTRAINT, NL_CONSTRAINT)

    print("My Programm took", time.time()-START_TIME, "to run")
