# Constants for mapping between values


# long grade names >> short grade names
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

# short grade names >> positions in grade list
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

# list positions >> short grade names
POSITION_GRADES = dict(reversed(item) for item in GRADE_POSITIONS.items())

# # RIDE's school classifications >> school classifications in Access database
# SCHOOL_TYPE_MAP = {
    
# }

# # Needed destinations:
# "Public School"
# "Independent Charter School"
# "State Operated School"
# "Regional Collaborative"
# "District Charter School"

# fields in Access database >> fields in dicts returned by web_scraper
VARIABLES_MAP = {
    "school_code": "code",
    "name_iwl": "name",
    "low_grade": "grade_min",
    "high_grade": "grade_max",
    "street1": "street1",
    "street2": "street2",
    "city": "city",
    "zip": "zip",
    "phone": "phone",
    "url": "url",
    "principal": "p_name",
    "principal_label": "p_title",
    "district_name": "dist",
    "nces_code": "nces"
}