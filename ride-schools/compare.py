import web_scraper
import enroll
from constants import VARIABLES_MAP as VM
import logging as log
import csv
import urllib2
from retrying import retry
import socket

# CODE NEEDS MAJOR CLEANUP!

def main():

    outfile = open("changes_new.txt", "w")

    schools_file = open("ride_schools_info.csv", "r")
    schools = list(csv.DictReader(schools_file))
    schools_file.close()
    # schools, districts = web_scraper.getAllInfo("ride_all_schools.html")
    sch_enrolls, dist_enrolls = enroll.main("enroll.csv")

    schools_dict = {}
    for i in web_scraper.convertAllToString(schools):
        if "Public School" in i["type"]:
            schools_dict[i["code"]] = i

    f = open("last_year.csv", "r")
    access = list(csv.DictReader(f))
    f.close()

    checked = set()
    websites = {}
    for b in schools_dict:
        # if b not in checked:
        #     outfile.write(schools_dict[b]["name"] +
        #         " not in last year's database.\n")
        checkGrades(schools_dict[b], sch_enrolls, outfile)
        # if schools_dict[b]["url"] != "":
        #     schools_dict[b]["url"] = "http://" + schools_dict[b]["url"] + "/"
        schools_dict[b]["url"] = fixURL(schools_dict[b]["url"])
        url = schools_dict[b]["url"]
        # url = "http://" + schools_dict[b]["url"]
        if url not in websites:
            websites[url] = 1
        else:
            websites[url] += 1
        # url_check = checkURL(url, outfile)
        # if url_check != False:
        #     schools_dict[b]["url"] = url_check
        # else:
        #     outfile.write("Failure connecting to URL for " + schools_dict[b]["name"] +
        #         ".\n(" + url + ")\n")
        schools_dict[b]["num_students"] = getTotalEnroll(schools_dict[b]["code"],
            sch_enrolls, outfile)
    for a in access:
        ac = a["school_code"]
        checked.add(ac)
        try:
            for prop in a:
                if prop in VM:
                    if a[prop] != schools_dict[ac][VM[prop]]:
                        outfile.write(a["name_iwl"] + " has a mismatch:\n" +
                            "Old " + prop + ": " + a[prop] + "\n" +
                            "New " + prop + ": " + schools_dict[ac][VM[prop]] +
                            "\n")
        except KeyError as e:
            outfile.write("School " + ac + " missing from new data.\n")
    for c in schools_dict:
        if c not in checked:
            outfile.write(schools_dict[c]["name"] +
                " not in last year's database.\n")
    for w in websites:
        if websites[w] > 1:
            outfile.write(w + " is listed as a website for " + str(websites[w]) +
                " schools.\n")

    outfile.close()

    return schools_dict

def runSchool():

    return

def checkGrades(school, sch_enrolls, outfile):

    try:
        obj = sch_enrolls[school["code"]]
    except KeyError:
        outfile.write("Couldn't find school " + school["code"] +
            " in enrollment data.\n")
        return
    g_start = school["grade_min"]
    g_end = school["grade_max"]
    check = obj.checkGrades(g_start, g_end)
    if check["match"] == False:
        if check["missing"] != []:
            missing_grades = ", ".join(check["missing"])
            # log.warning(obj.getName() + "'s grade span is supposed to be " +
            #     g_start + " to " + g_end + ", but it has zero students " +
            #     "enrolled in grade(s) " + missing_grades + ".")
            outfile.write(obj.getName() + "'s grade span is supposed to be " +
                g_start + " to " + g_end + ", but it has zero students " +
                "enrolled in grade(s) " + missing_grades + ".\n")
        if check["extra"] != []:
            extra_grades = ", ".join(check["extra"])
            # log.warning(obj.getName() + "'s grade span is supposed to be " +
            #     g_start + " to " + g_end + ", but it has zero students " +
            #     "enrolled in grade(s) " + missing_grades + ".")
            outfile.write(obj.getName() + "'s grade span is supposed to be " +
                g_start + " to " + g_end + ", but it also has students " +
                "enrolled in grade(s) " + extra_grades + ".\n")
    
    return

def getTotalEnroll(school_code, sch_enrolls, outfile):

    try:
        num = sch_enrolls[school_code].getTotal()
    except KeyError:
        # outfile.write("Couldn't find school " + school_code +
        #     " in enrollments file.\n")
        return ""
    else:
        return str(num)


# # @retry(socket.error(), tries=4, delay=3, backoff=2)
# @retry(socket.error())
# def urlopenWithRetry(url):
#     return urllib2.urlopen("http://example.com")

# @retry(socket.error, tries=4, backoff=2)
def checkURL(url, outfile):

    if url == "":
        return ""
    else:
        url_http = url
        # url_http = "http://" + url
        # url_https = "https://" + url

        try:
            urllib2.urlopen(url_http)
            # urlopenWithRetry(url_http)
        except (urllib2.URLError, socket.error):
            outfile.write("Error connecting to: " + url + "\n")
            return False
            # try:
            #     urllib2.urlopen(url_https)
            #     # urlopenWithRetry(url_https)
            # except urllib2.URLError:
            #     outfile.write("Error connecting to: " + url + "\n")
            #     return False
            # else:
            #     outfile.write("Note: Site " + url +
            #         " only connects with HTTPS.\n")
            #     return url_https
        else:
            return url_http

def checkForSiteDuplicates():

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


if __name__ == "__main__":
    schools_dict = main()
