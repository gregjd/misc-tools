import csv
import enroll
import utils


# School metadata; says whether each school is open or closed. Change this.
SLICE_FILE = "//TPPFILE/Data/WORK/iRide/Year Seven/Slice/00225.csv"

# Current school year. Change this.
SCHOOL_YEAR = "2015-2016"

# Enrollments file. (Currently references this file in the current folder.)
ENROLL_FILE = "enroll.csv"

# New file name. Will be saved in the current folder.
NEW_FILE = "statewide_stats.csv"

def main(NEW_FILE):
    """Calculates the stats, writes them to a CSV, returns them as a dict."""

    # List of all schools
    sch = [s for s in utils.getDataFromCSV(SLICE_FILE) if s["is_open"] == "Y"]

    # Enrollment figures for all schools and districts
    sch_enrolls, dist_enrolls = enroll.main(ENROLL_FILE)

    # Schools by type
    dist_schools = getSchoolsByType(sch, "Public School")
    dist_charters = getSchoolsByType(sch, "District Charter School")
    ind_charters = getSchoolsByType(sch, "Independent Charter School")
    state_schools = getSchoolsByType(sch, "State Operated School")
    reg_collabs = getSchoolsByType(sch, "Regional Collaborative")

    # Students in charters
    dist_ch_students = sum([int(d["num_students"]) for d in dist_charters])
    ind_ch_students = sum([int(i["num_students"]) for i in ind_charters])
    ch_students = dist_ch_students + ind_ch_students

    # Schools by grade configuration
    e = getSchoolsByConfig(sch, "Emh")
    m = getSchoolsByConfig(sch, "eMh")
    h = getSchoolsByConfig(sch, "emH")
    em = getSchoolsByConfig(sch, "EMh")
    mh = getSchoolsByConfig(sch, "eMH")
    emh = getSchoolsByConfig(sch, "EMH")

    # Summary stats
    # (Messy variable names are that way to match the names used in past yrs)
    summary = {
        "School_Year": SCHOOL_YEAR,
        "Students -Total #": dist_enrolls["00"].getTotal(),
        "Students-Public E": sum(dist_enrolls["00"].getEnrolls("PK", "5")),
        "Students-Public M": sum(dist_enrolls["00"].getEnrolls("6", "8")),
        "Students-Public H": sum(dist_enrolls["00"].getEnrolls("9", "12")),
        "Students - Charter District": dist_ch_students,
        "Students-Charter Independent": ind_ch_students,
        "Students - Charter Total #": ch_students,
        "Students-Chart Total %":
            toPct(float(ch_students) / float(dist_enrolls["00"].getTotal())),
        "Schools-Total #": len(sch),
        "Schools-E": len(e),
        "Schools-M": len(m),
        "Schools-H": len(h),
        "Schools-EM": len(em),
        "Schools-MH": len(mh),
        "Schools-EMH": len(emh),
        "Schools-District Operated": len(dist_schools),
        "Schools-State Operated": len(state_schools),
        "Schools - Charter District": len(dist_charters),
        "Schools-Charter Independent": len(ind_charters),
        "Schools-Collaboratives": len(reg_collabs),
        "Schools-Preschools":
            len([p for p in sch_enrolls if isPkOnly(sch_enrolls[p])])
    }

    # Past years included this preschools-only number, then later cut it
    del summary["Schools-Preschools"]

    writeCSV(new_csv_file, summary)

    return summary

def getSchoolsByType(schools_list, type_):
    """Returns a list of dicts of schools matching the given type."""

    return [i for i in schools_list if i["school_type_iwl"] == type_]

def getSchoolsByConfig(schools_list, config):
    """Returns a list of dicts of schools matching the given grade config."""

    return [i for i in schools_list if i["grade_config_IWL"] == config]

def isPkOnly(school_obj):
    """Returns True if a school only has students in PK."""

    if school_obj.getTotal() == school_obj.getEnrolls("PK", "PK")[0]:
        if school_obj.getTotal() > 0:
            return True
        else:
            return False  # school has no students
    else:
        return False  # PK enroll doesn't match total enroll

def toPct(number):
    """Float (e.g. 0.04531590) >> percent with 2 decimal places (4.53)."""

    return float(format(number*100, ".2f"))

# TODO: move the actual saving part to utils.py?
def writeCSV(new_file_name, summary_stats):

    header = ["School_Year", "Students -Total #",
        "Students-Public E", "Students-Public M", "Students-Public H",
        "Students - Charter District", "Students-Charter Independent",
        "Students - Charter Total #", "Students-Chart Total %",
        "Schools-Total #", "Schools-E", "Schools-M", "Schools-H",
        "Schools-EM", "Schools-MH", "Schools-EMH",
        "Schools-District Operated", "Schools-State Operated",
        "Schools - Charter District", "Schools-Charter Independent",
        "Schools-Collaboratives"]
    print ("\nSaving file: " + new_file_name + " ...")
    with open(new_file_name, "wb") as csvfile:
        writer = csv.DictWriter(csvfile, header)
        writer.writeheader()
##        for s in schools_list:
##            writer.writerow(s)
        writer.writerow(summary_stats)
    csvfile.close()
    print ("Saved file: " + new_file_name)

    return


if __name__ == "__main__":
    summary = main()
