import urllib2
import bs4  # Requires BeautifulSoup4 to be installed
import csv
import re
import logging as log


# Primary functions

def getAllInfo(schools_html):

    log.basicConfig(
        filename="ride_schools_logfile.log",
        format="%(levelname)s: %(message)s",
        level=logging.DEBUG)

    print ("Opening: " + schools_html)
    f = open(schools_html, "r")
    html = bs4.BeautifulSoup(f.read(), "html.parser")
    f.close()
    print ("Closed: " + schools_html)

    some_schools = html.find_all("tr", class_="DataGridItem")
    other_schools = html.find_all("tr", class_="DataGridAlternatingItem")
    all_schools = some_schools + other_schools

    print ("Scraping each school's info page. This may take a few minutes.")
    schools = []
    for i in all_schools:
        url = str(i.find_all("td")[1].find("a")["href"])
        url_ = "http://www2.ride.ri.gov/Applications/MasterDirectory/" + url
        try:
            sch_info = getSchoolInfo(url_)
        except urllib2.URLError:  # if can't load page, log URL and name
            log.warning("Couldn't load page: " + url_ +
                + "\n(Name: " + i.find_all("td")[1].find("a").get_text() +
                ")" + "\nPage skipped.")
        else:
            schools.append(sch_info)

    writeCSV("ride_schools_info.csv")

    return schools

def getSchoolInfo(url):

    page = bs4.BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")

    return {
        "name": getAttribute(page, "Name", "link"),
        "dist": getAttribute(page, "Parent", "link"),
        "status": getAttribute(page, "Active", "short"),
        "code": getAttribute(page, "Code", "short"),
        "type": getAttribute(page, "Type", "short"),
        # "grades": getAttribute(page, "Grades", "short"),
        # "level": getAttribute(page, "SchLevel", "short"),
        "nces": getAttribute(page, "NCESCode", "short"),
        "street1": getMultiAttribute(page, "Address")[0],
        "street2": getMultiAttribute(page, "Address")[1],
        "c_s_z": cleanCSZ(getAttribute(page, "CityStateZip", "long")),
        "phone": cleanPhone(getAttribute(page, "LocPhone", "long")),
        # "fax": cleanPhone(getAttribute(page, "LocFax", "long")),
        "url": getAttribute(page, "LocWebsite", "long"),
        "config": getAttribute(page, "01", "mid")
    }

def getAttribute(page, short_id, id_type):

    if id_type == "long":
        long_id = "ctl00_cphContent_repLocations_ctl01_lbl" + short_id
        tag = "span"
    elif id_type == "short":
        long_id = "ctl00_cphContent_lbl" + short_id
        tag = "span"
    elif id_type == "link":
        long_id = "ctl00_cphContent_hlk" + short_id
        tag = "a"
    elif id_type == "mid":
        long_id = ("ctl00_cphContent_repAttributes_ctl" + short_id +
            "_repValues_ctl01_lblAttValue")
        tag = "span"
    else:
        raise Exception("id_type is not valid")
    try:
        content = page.find(tag, {"id": long_id}).get_text()
    except AttributeError:
        return ""
    else:
        return str(content)

def getMultiAttribute(page, short_id):

    long_id = "ctl00_cphContent_repLocations_ctl01_lbl" + short_id
    tag = "span"

    try:
        content = list(page.find(tag, {"id": long_id}).strings)
    except AttributeError:
        return ("", "")
    else:
        a = str(content[0])
        b = str(", ".join(content[1:]))
        if len(content) > 2:
            log.debug("On " + page + ", multiple new lines found here:\n"
                +  "\n".join(content[1:]))
        return (a, b)

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


# Tools

def cleanPhone(phone_num):
    """Given '(123) 456-7890', returns '1234567890'."""

    return "".join(re.split("\W+", phone_num))

def cleanCSZ(c_s_z):
    """Given 'City, RI 12345', returns ('City', '12345').

    Will convert a 9-digit ZIP to a 5-digit ZIP if necessary.
    """

    city, sz = c_s_z.split(",")
    state, zip_ = sz.split()
    if state != "RI":
        log.debug("Encountered state of " + state +
            "when applying cleanCSZ to '" + c_s_z + "'.")
    zip5 = zip_[0:5]

    return (city, zip5)


# Run

if __name__ == "__main__":
    schools = getAllInfo("ride_all_schools.html")
