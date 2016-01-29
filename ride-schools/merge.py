import csv
from constants import VARIABLES_MAP as VM


SCHOOL_YEAR = "2015-2016"  # change this each year

# clean up some parts of this code

def main():

    last = listToDict(getDataFromCSV("last_year.csv"), "school_code")
    # enroll = listToDict(getDataFromCSV("enroll.csv"), "schcode")
    this = listToDict(getDataFromCSV("ride_schools_info.csv"), "code")
    sch_enrolls, dist_enrolls = enroll.main("enroll.csv")

    schools_list = []
    checked = set()
    for sch_code in last:
        if last[sch_code]["is_open"] == "Y":
            if sch_code in this:
                new_dict = getFromScrape(sch_code, last[sch_code], this)
                new_dict["num_students"] = getTotalEnroll(sch_code, sch_enrolls)
                new_dict["school_year"] = SCHOOL_YEAR
                new_dict["url"] = fixURL(new_dict["url"])
                checkGrades(sch_code, this[sch_code], sch_enrolls)
                schools_list.append(new_dict)
            else:
                print ("WARNING: " + sch_code + " not in this year's data!" +
                    "\n Not included in results file.\n")
        else:
            new_dict = last[sch_code]
            new_dict["school_year"] = SCHOOL_YEAR
            schools_list.append(new_dict)
        checked.add(sch_code)
    for e in sch_enrolls:
        if e not in checked:
            if e[-3:] != "190":
                print (e + " appears to be a new school")
                new_dict = getFromScrape(e, dict(), this)
                new_dict["num_students"] = getTotalEnroll(sch_code, sch_enrolls)
                new_dict["school_year"] = SCHOOL_YEAR
                new_dict["url"] = fixURL(new_dict["url"])
                checkGrades(sch_code, this[sch_code], sch_enrolls)
                schools_list.append(new_dict)
                checked.add(sch_code)

    writeCSV("new_year.csv", schools_list)

    return

def getFromScrape(code, sch_dict, lookup):

    if code not in lookup:
        print ("WARNING: " + code + " not found in data for this year!")
        return sch_dict
    else:
        # for prop in sch_dict:
        #     if prop in VM:
        #         sch_dict[prop] = lookup[code][VM[prop]]
        for prop in VM:
            sch_dict[prop] = lookup[code][VM[prop]]
        return sch_dict

def getTotalEnroll(code, sch_enrolls):

    try:
        num = sch_enrolls[code].getTotal()
    except KeyError:
        print ("Couldn't find school " + code +
            " in enrollments file.\n")
        return ""
    else:
        return str(num)

def checkGrades(code, sch_dict, sch_enrolls):

    try:
        obj = sch_enrolls[code]
    except KeyError:
        # outfile.write("Couldn't find school " + school["code"] +
        #     " in enrollment data.\n")
        print (code + " not in enrollment data")
        return
    g_start = sch_dict["grade_min"]
    g_end = sch_dict["grade_max"]
    check = obj.checkGrades(g_start, g_end)
    if check["match"] == False:
        if check["missing"] != []:
            missing_grades = ", ".join(check["missing"])
            print (obj.getName() + "'s grade span is supposed to be " +
                g_start + " to " + g_end + ", but it has zero students " +
                "enrolled in grade(s) " + missing_grades + ".\n")
        if check["extra"] != []:
            extra_grades = ", ".join(check["extra"])
            print (obj.getName() + "'s grade span is supposed to be " +
                g_start + " to " + g_end + ", but it also has students " +
                "enrolled in grade(s) " + extra_grades + ".\n")

    return

def fixURL(raw_url):

    if raw_url == "":
        return ""
    else:
        new_url = raw_url
        if new_url[0:7] not in ["http://", "https:/"]:
            new_url = "http://" + new_url
        if new_url[-1] != "/":
            new_url = new_url + "/"
        return new_url

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

def writeCSV(new_file_name, schools_list):

    sorted_list = sorted(schools_list, key=lambda k: k["school_code"])
    # header = [i for i in schools_list[0]]
    header = ["ID", "school_code", "school_year", "rolled_into",
        "district_code_IWL", "district_code_lea", "school_type_iwl",
        "school_type_other", "is_open", "name_iwl", "name_hub",
        "low_grade", "high_grade", "grade_config_IWL", "grade_config_HUB",
        "street1", "street2", "city", "zip", "phone", "url",
        "principal", "principal_label", "num_students", "num_teachers",
        "notes", "name_short", "district_name", "name_short_lea",
        "corecity_4_yn", "corecity_5_yn", "corecity_6_yn", "charter_yn",
        "compare_py_dsc", "elem_yn", "middle_yn", "high_yn", "pk_only_yn",
        "title1_yn", "grade_span", "include_IWL_file_yn", "display_yn_HUB",
        "nces_code", "ACT_CEEB_code", "ucoa_code", "ucoa_leacode",
        "ctract2010", "cblock2010", "ctract2000", "cblock2000", "MC_yn",
        "neighborhood"]
    print "\nSaving file:", new_file_name, "..."
    with open(new_file_name, "wb") as csvfile:
        writer = csv.DictWriter(csvfile, header)
        writer.writeheader()
        for s in sorted_list:
            writer.writerow(s)
    csvfile.close()
    print "Saved file:", new_file_name

    return


if __name__ == "__main__":
    main()
