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

    # if multiple addresses, make a note in the logfile:
    labels = [i.get_text() for i in 
        page.find_all("span", {"class": "smalllabel"})]
    count = len([j for j in labels if j == "Address:"])
    if count > 1:
        log.debug("Found multiple addresses for " +
            getAttribute(page, "Name", "link") + "\n(" + url +
            ")\nFirst address used.")

    p_name, p_title = getPrincipal(page)

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
        "city": cleanCSZ(getAttribute(page, "CityStateZip", "long"))[0],
        "zip": cleanCSZ(getAttribute(page, "CityStateZip", "long"))[1],
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

def getPrincipal(page):

    # Look for exactly one person with the role of Principal, Director, or Superintendent
    # If one, get name and title (not role)
    # If none, log error (DEBUG)
    # If multiple:
        # check to see if they're actually the same person and have the same title - then use that person
        # log error (DEBUG) and concatenate names (and make title plural)
    # Optional: strip PhD and EdD from people's names (LOW PRIORITY)

    def getInfo(soup):

        rows = [row for row in soup.contents if isTag(row)]
        # print type(rows)
        # print ("Number of rows: " + str(len(rows)))  # cut
        name = str(rows[0].find_all("span")[1].get_text()).rstrip()
        title = str(rows[1].find_all("span")[1].get_text())
        roles = [str(role.get_text()) for role in rows[3].find_all("span")]

        return {
            "name": name,
            "title": title,
            "roles": roles
        }

    def isPrincipal(person):

        r = person["roles"]
        check_list = ["Principal", "Superintendent", "Director"]

        return any(i in check_list for i in r)

    t = page.find("div", {"id": "ctl00_cphContent_pnlContacts"}).table
    # for thing in t.contents:
    #     print isinstance(thing, bs4.element.Tag)
    # tags = [x for x in t.contents if isinstance(x, bs4.element.Tag)]
    tags = [x for x in t.contents if isTag(x)]
    # print len(tags)
    # print type(t)
    # print ("len of t: " + str(len(t)))
    # print type(t.contents)
    # print ("len of t.contents: " + str(len(t.contents)))
    # print ("filter" + str(len(filter(lambda x: x=="", t.contents))))
    # print type(t.contents[0])
    # print type(t.contents[1])
    # print type(t.contents[2])
    # print type(t.contents[3])
    # print type(t.contents[4])
    # print type(t.contents[5])
    # print "final" + str(type(t.contents[28]))
    # for c in t.contents:
    #     print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #     print c
    # people = []
    # for y in tags:
    #     try:
    #         table_exists = (y.table != None)
    #     except AttributeError:
    #         print "AE!!!"
    #         pass
    #     else:
    #         print table_exists  # cut
    #         if table_exists:
    #             people.append(getInfo(y))
    people = [getInfo(y) for y in tags if y.table != None]
    # print people  # cut
    principals = [z for z in people if isPrincipal(z)]
    # print principals  # cut

    if len(principals) == 1:
        return (principals[0]["name"], principals[0]["title"])
    elif len(principals) == 0:
        # log debug
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
            # names = ", ".join([p["name"] for p in principals])
            names = ", ".join(name_list)
            if len(set(title_list)) == 1:  # if they all have the same title
                titles = title_list[0] + "s"  # make it plural
            else:
                titles = ", ".join(title_list)
            # log debug
            # print ("Multiple principals found.")  # cut
            return (names, titles)
    else:
        # not good, log warning
        return ("", "")

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

def isTag(t):

    return isinstance(t, bs4.element.Tag)

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
