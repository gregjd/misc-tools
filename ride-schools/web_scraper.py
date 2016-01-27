import urllib2
import bs4  # Requires BeautifulSoup4 to be installed
import csv
import re
import logging as log
from datetime import datetime
import constants


# Primary functions

def getAllInfo(schools_html):

    now = datetime.now()
    dt = "-".join([str(now.date()), str(now.hour), str(now.minute)])
    log.basicConfig(
        filename=("web_scraper_logfile_" + dt + ".log"),
        format="%(levelname)s: %(message)s",
        level=log.DEBUG)

    print ("Opening: " + schools_html)
    f = open(schools_html, "r")
    html = bs4.BeautifulSoup(f.read(), "html.parser")
    f.close()
    print ("Closed: " + schools_html)

    full_list = html.find_all("tr",
        class_=["DataGridItem", "DataGridAlternatingItem"])

    def getOrgSummary(org_soup):

        tags = org_soup.find_all("td")

        code = tags[0].get_text()
        name = tags[1].get_text().strip()
        link = tags[1].find("a")["href"]
        org_type = tags[3].get_text()

        return {
            "code": code,
            "name": name,
            "link": link,
            "org_type": org_type
        }

    def scrapeSchoolPage(school_summary):

        url = school_summary["link"]
        url_ = "http://www2.ride.ri.gov/Applications/MasterDirectory/" + url
        try:
            sch_info = getSchoolInfo(url_)
        except urllib2.URLError:  # if can't load page, log URL and name
            log.warning("Couldn't load page: " + url_ +
                "\n(Name: " + school_summary["name"] + ")\nPage skipped.")
            return None
        except AttributeError as e:
            log.warning("AttributeError encountered on this page: " + url_ +
                "\n(Name: " + school_summary["name"] + ")\n" +
                "Page skipped. See details below.")
            log.exception(e)
            return None
        else:
            return sch_info

    school_list = []
    district_list = []
    other_list = []
    for org in full_list:
        summary = getOrgSummary(org)
        if summary["org_type"] == "School":
            school_list.append(summary)
        elif summary["org_type"] == "LEA":
            district_list.append(summary)
        else:
            other_list.append(summary)

    print ("Scraping each school's info page. This may take a few minutes.")
    schools = []
    districts = []

    for s in school_list:
        sch_scrape = scrapeSchoolPage(s)
        if sch_scrape != None:
            schools.append(sch_scrape)
    for d in district_list:
        dist_scrape = scrapeSchoolPage(d)
        if dist_scrape != None:
            districts.append(dist_scrape)

    writeCSV("ride_schools_info.csv", convertAllToString(schools))

    return (schools, districts)

def getSchoolInfo(url):

    page = bs4.BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")

    sch_name = "name": getAttribute(page, "Name", "link")

    # if multiple addresses, make a note in the logfile:
    labels = [i.get_text() for i in 
        page.find_all("span", {"class": "smalllabel"})]
    count = len([j for j in labels if j == "Address:"])
    if count > 1:
        log.debug("Found multiple addresses for " +
            sch_name + "\n(" + url +
            ")\nFirst address used.")

    street1, street2 = getMultiAttribute(page, "Address")
    city, zip_ = cleanCSZ(getAttribute(page, "CityStateZip", "long"))

    p_name, p_title = getPrincipal(page, url, sch_name)

    return {
        "name": sch_name,
        "dist": getAttribute(page, "Parent", "link"),
        "status": getAttribute(page, "Active", "short"),
        "code": getAttribute(page, "Code", "short"),
        "type": getAttribute(page, "Type", "short"),
        "grades": getAttribute(page, "Grades", "short"),
        # "level": getAttribute(page, "SchLevel", "short"),
        "nces": getAttribute(page, "NCESCode", "short"),
        "street1": street1,
        "street2": street2,
        "city": city,
        "zip": zip_,
        "phone": cleanPhone(getAttribute(page, "LocPhone", "long")),
        # "fax": cleanPhone(getAttribute(page, "LocFax", "long")),
        "url": getAttribute(page, "LocWebsite", "long"),
        "p_name": p_name,
        "p_title": p_title,
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
        content = page.find(tag, {"id": long_id}).get_text().strip()
    except AttributeError:
        return ""
    else:
        return content

def getMultiAttribute(page, short_id):

    long_id = "ctl00_cphContent_repLocations_ctl01_lbl" + short_id
    tag = "span"

    try:
        content = list(page.find(tag, {"id": long_id}).strings)
    except AttributeError:
        return ("", "")
    else:
        a = content[0].strip()
        b = ", ".join([s.strip() for s in content[1:]])
        if len(content) > 2:
            log.debug("Multiple new lines found here:\n"
                +  "\n".join(content[1:]))
        return (a, b)

def getPrincipal(page, url, sch_name):

    def getInfo(soup):

        rows = [row for row in soup.contents if isTag(row)]
        name = rows[0].find_all("span")[1].get_text().strip()
        title = rows[1].find_all("span")[1].get_text().strip()
        roles = [role.get_text() for role in rows[3].find_all("span")]
        # removes double-spaces in the middle of names w/o middle initials:
        name_ = name.replace(u"  ", u" ")

        return {
            "name": name_,
            "title": title,
            "roles": roles
        }

    def isPrincipal(person):

        r = person["roles"]
        check_list = ["Principal", "Superintendent", "Director"]

        return any(i in check_list for i in r)

    try:
        t = page.find("div", {"id": "ctl00_cphContent_pnlContacts"}).table
    except AttributeError:
        return ("", "")
    tags = [x for x in t.contents if isTag(x)]
    people = [getInfo(y) for y in tags if y.table != None]
    principals = [z for z in people if isPrincipal(z)]

    if len(principals) == 1:
        if principals[0]["name"] != "[No Contact Selected]":
            return (principals[0]["name"], principals[0]["title"])
        else:
            return ("", "")
    elif len(principals) == 0:
        log.debug("No principal found in contacts list for " + sch_name +
            ".\n(" + url + ")")
        return ("", "")
    elif len(principals) > 1:
        name_list = [p["name"] for p in principals]
        title_list = [p["title"] for p in principals]
        if len(set(name_list)) == 1:  # if they're actually the same person
            if len(set(title_list)) == 1:  # if the title is the same
                title_ = title_list[0]
            else:
                title_ = ", ".join(title_list)
            return (name_list[0], title_)
        else:
            names = "; ".join(name_list)
            if len(set(title_list)) == 1:  # if they all have the same title
                titles = title_list[0] + "s"  # make it plural
            else:
                titles = "; ".join(title_list)
                log.debug("Multiple principals found for " + sch_name +
                    ".\n(" + url + ")")
            return (names, titles)
    else:
        log.warning("Encoutered error when trying to find principal for " +
            sch_name + ".\n(" + url + ")")
        return ("", "")

def convertAllToString(list_of_dicts):

    for d in list_of_dicts:
        for key in d:
            try:
                d[key] = str(d[key])
            except UnicodeEncodeError:
                # replace right single quote mark with single quote mark
                d[key] = d[key].replace(u"\u2019", u"'").replace(u"\u2013", u"")
                d[key] = str(d[key])
                # TODO: deal with other cases, if they were to exist

    return list_of_dicts

def writeCSV(new_file_name, data):

    header = ["code", "type", "status", "name", "dist", "config", "nces",
        "street1", "street2", "city", "zip", "phone",
        "url", "p_name", "p_title"]
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

def isTag(t):

    return isinstance(t, bs4.element.Tag)

def cleanPhone(phone_num):
    """Given '(123) 456-7890', returns '1234567890'."""

    try:
        new_phone = "".join(re.split("\W+", phone_num))
    except ValueError:
        log.debug("Encountered error when trying to clean: " + phone_num)
        return phone_num
    else:
        return new_phone

def cleanCSZ(c_s_z):
    """Given 'City, RI 12345', returns ('City', '12345').

    Will convert a 9-digit ZIP to a 5-digit ZIP if necessary.
    """

    if c_s_z == "":
        return ("", "")
    else:
        try:
            city, sz = c_s_z.split(",")
            state, zip_ = sz.split()
        except ValueError as e:
            log.debug("Encountered error when trying to clean: " + c_s_z +
                "\nOutput city and ZIP left blank.")
            return ("", "")
        else:
            if state != "RI":
                log.debug("Encountered state of " + state +
                    " when applying cleanCSZ to '" + c_s_z + "'.")
            zip5 = zip_[0:5]
            return (city, zip5)


# Run

if __name__ == "__main__":
    schools, districts = getAllInfo("ride_all_schools.html")
