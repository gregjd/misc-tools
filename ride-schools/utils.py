import csv


def getDataFromCSV(file_name):

    f = open(file_name, "r")
    data = list(csv.DictReader(f))
    f.close()

    return data

def listToDict(list_of_dicts, key):

    dict_of_dicts = {}
    for d in list_of_dicts:
        dict_of_dicts[d[key]] = d

    return dict_of_dicts
