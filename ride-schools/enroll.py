import csv


# Constants:

# map from given grade names to cleaner names
GRADES = {
    "GPK": "PK",
    "GPF": "PK",
    "GKG": "K",
    "GKF": "K",
    "G01": "1",
    "G02": "2",
    "G03": "3",
    "G04": "4",
    "G05": "5",
    "G06": "6",
    "G07": "7",
    "G08": "8",
    "G09": "9",
    "G10": "10",
    "G11": "11",
    "G12": "12"
}

# map from clean grade names to positions in list
GRADE_POSITIONS = {
    "PK": 0,
    "K": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    "10": 11,
    "11": 12,
    "12": 13
}

# map from list positions to their respective grades
POSITION_GRADES = dict(reversed(item) for item in GRADE_POSITIONS.items())


# Functions

def main(file_name):

    return mapData(readCSV(file_name))

def readCSV(file_name):

    print ("Opening: " + file_name)
    f = open(file_name, "r")
    raw_data = list(csv.DictReader(f))
    f.close()
    print ("Closed: " + file_name)

    return raw_data

def mapData(raw_data):

    given_grades = ["GPK", "GPF", "GKG", "GKF", "G01", "G02", "G03",
        "G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11", "G12"]
    schools = {}
    districts = {}
    for d in raw_data:
        schcode = d["schcode"]
        new_dict = {
            "code": schcode,
            "name": d["schname"],
            "total": d["total"],
            "enroll": [0]*14  # list with 14 slots, all with value of 0
        }
        for grade in given_grades:
            new_grade_name = GRADES[grade]
            list_position = GRADE_POSITIONS[new_grade_name]
            count = d[grade]
            new_dict["enroll"][list_position] += count
        if len(schcode) == 5:
            schools[schcode] = new_dict
        elif len(schcode) == 2:
            districts[schcode] = new_dict
        else:
            raise Exception("Variable 'schcode' can only be 2 or 5 " +
                "characters long. " + str(len(schcode)) +
                " characters found in code " + schcode + ".")

    return schools, districts

def check(code, grade_start, grade_end, dict_):

    ## add code!

    return {
        "match": ## bool,
        "missing": ## list,
        "extra": ## list
    }


# class School():

#     def __init__(self, dict_):

#         self.code = dict_["schcode"]
#         self.name = dict_["schname"]
#         self.total = dict_["total"]
#         self.enroll = {
#             "PK": 0,
#             "K": 0,
#             "1": 0,
#             "2": 0,
#             "3": 0,
#             "4": 0,
#             "5": 0,
#             "6": 0,
#             "7": 0,
#             "8": 0,
#             "9": 0,
#             "10": 0,
#             "11": 0,
#             "12": 0
#         }

#         for g in GRADES_MAP:
#             grade = GRADES_MAP[g]
#             num = dict_[g]
#             self.enroll[grade] = num

#     def getCode(self):

#         return self.code

#     def getName(self):

#         return self.name

#     def getEnroll(self, gr=None):

#         if gr == None:
#             return self.total
#         elif gr in self.enroll:
#             return self.enroll[gr]
#         else:
#             return None


if __name__ == "__main__":

    sch_enrolls, dist_enrolls = main()
