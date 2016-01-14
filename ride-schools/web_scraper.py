import urllib2
import bs4  # Requires BeautifulSoup4 to be installed
import csv


# create master dict/list of schools
# get master list HTML
# for each school (if it satisfies a condition?): get certain info
# write that info to our master dict/list
# write results to CSV
# compare?

def getAllInfo(all_schools):

    f = open(all_schools, "r")
    html = bs4.BeautifulSoup(f.read(), "html.parser")
    f.close()

    some_schools = html.find_all("tr", class_="DataGridItem")
    other_schools = html.find_all("tr", class_="DataGridAlternatingItem")
    all_schools = some_schools + other_schools

    schools = []
    for i in all_schools:
        url = str(i.find_all("td")[1].find("a")["href"])
        url_ = "http://www2.ride.ri.gov/Applications/MasterDirectory/" + url
        try:
            sch_info = getSchoolInfo(url_)
        except urllib2.URLError, e:  # if can't load page, print URL and name
            # print (e)
            print ("URLError: " + url_)
            print (i.find_all("td")[1].find("a").get_text() + "\n")
        else:
            schools.append(sch_info)

    # do something
    # writeCSV

    writeCSV("ride_schools_info.csv")

    return schools

def getSchoolInfo(url):

    page = bs4.BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")

    return {
        "code": getAttribute(page, "Code", "short"),
        "grades": getAttribute(page, "Grades", "short"),
        "level": getAttribute(page, "SchLevel", "short"),
        "address": getAttribute(page, "Address", "long"),
        "c_s_z": getAttribute(page, "CityStateZip", "long"),
        "phone": getAttribute(page, "LocPhone", "long"),
        "fax": getAttribute(page, "LocFax", "long"),
        "url": getAttribute(page, "LocWebsite", "long")
    }

def getAttribute(page, short_id, id_type):

    if id_type == "long":
        long_id = "ctl00_cphContent_repLocations_ctl01_lbl" + short_id
    elif id_type == "short":
        long_id = "ctl00_cphContent_lbl" + short_id
    else:
        raise Exception("id_type is not valid")
    try:
        content = page.find("span", {"id": long_id}).get_text()
    except AttributeError:
        content = ""

    return str(content)

def writeCSV(new_file_name, data):

    header = ["code", "grades", "level", "address",
        "c_s_z", "phone", "fax", "url"]
    print '\nSaving file:', new_file_name, '...'
    with open(new_file_name, "wb") as csvfile:
        writer = csv.DictWriter(csvfile, header)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
    csvfile.close()
    print 'Saved file:', new_file_name

    return


if __name__ == "__main__":
    schools = getAllInfo("ride_all_schools.html")
