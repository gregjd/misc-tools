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


# Classes

class SchoolOrDistrict():

    def __init__(self, dict_):

        self.code = dict_["schcode"]
        self.name = dict_["schname"]
        self.total = dict_["total"]
        self.enroll = [0]*14  # list with 14 slots, all with value of 0

        given_grades = ["GPK", "GPF", "GKG", "GKF", "G01", "G02", "G03",
            "G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11", "G12"]
        for grade in given_grades:
            new_grade_name = GRADES[grade]
            list_position = GRADE_POSITIONS[new_grade_name]
            count = int(dict_[grade])
            self.enroll[list_position] += count

    def getCode(self):

        return self.code

    def getName(self):

        return self.name

    def getTotal(self):

        return self.total

    def checkEnroll(self, grade_start, grade_end):
        """Checks a provided grade range against the actual enrollments."""

        if type(grade_start) == int:
            grade_start = str(grade_start)
        if type(grade_end) == int:
            grade_end = str(grade_end)
        if (type(grade_start) != str) or (type(grade_end) != str):
            raise TypeError("'grade_start' and 'grade_end' arguments " +
                "must be of type str.")

        try:
            start_index = GRADE_POSITIONS[grade_start]
            end_index = GRADE_POSITIONS[grade_end] + 1
        except KeyError:
            raise KeyError("One or both of the given grades is out of range.")

        # Check for grades missing students inside the given grade range:
        missing = []
        for i in range(start_index, end_index):
            if self.enroll[i] == 0:
                missing.append(POSITION_GRADES[i])

        # Check enrolled students outside the given grade range:
        extra = []
        for j in range(0, start_index):
            if self.enroll[j] != 0:
                extra.append(POSITION_GRADES[j])
        for k in range(end_index, len(self.enroll)):
            if self.enroll[k] != 0:
                extra.append(POSITION_GRADES[k])

        # Do the enrollments match the grade span provided?
        match = ((missing == []) and (extra == []))

        return {
            "match": match,
            "missing": missing,
            "extra": extra
        }

class School(SchoolOrDistrict):

    pass

class District(SchoolOrDistrict):

    pass


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
        if len(schcode) == 5:
            schools[schcode] = School(d)
        elif len(schcode) == 2:
            districts[schcode] = District(d)
        else:
            raise Exception("Variable 'schcode' can only be 2 or 5 " +
                "characters long. " + str(len(schcode)) +
                " characters found in code " + schcode + ".")

    return schools, districts


if __name__ == "__main__":

    sch_enrolls, dist_enrolls = main("enroll.csv")
