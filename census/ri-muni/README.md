## Data sources and notes:

All data is from the American Community Survey 2014 5-year estimates, except age data, which is Census 2010 Summary File 1 100% data.

In the data output files, variables with `pct_` prefixes represent that respective variable (without the prefix) divided by the total population number. This yields a decimal between 0 and 1, which can be converted to a percent if desired.

The section headings below are links to the respective Census data tables.


### [Age](http://factfinder.census.gov/bkmk/table/1.0/en/DEC/10_SF1/QTP2/0400000US44.06000)

Age data uses individual years of age, which are only given (at our geography level) in the decennial census. Individual years of age are given through 99. 100 through 104 and 105 through 109 are given in 5-year groups, and 110 and older is one group.

There are two sets of data output files for age. One ("age") has age given in specific groups: 0–1, 2–4, 5–12, 13–18, 19–25, 26–64, 65+. The other ("age_all") has individual years of age, with the aforementioned groupings for people age 100 and older.

For the age groupings, if you open the data output file in Excel, you may see that Excel has converted the column headers `2-4` and `5-12` into dates ("4-Feb" and "12-May"). That is just Excel being annoying.

*Note:* Age data is also available [here](http://factfinder.census.gov/bkmk/table/1.0/en/DEC/10_SF1/PCT12/0400000US44.06000). The raw data should be the same as in the other table, although the variable codes are different.


### [Income](http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/B19013/0400000US44.06000)

The variable given here, `med_hh_inc`, represents "Median household income in the past 12 months (in 2014 Inflation-adjusted dollars)."

Income was not aggregated to catchment areas because that calculation wouldn't make sense. We are starting out with medians and not raw data, so we can't just take a mean of medians. (I mean, we can, but it wouldn't really make sense to do that.)


### [Language](http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/S1601/0400000US44.06000)

This is data on language spoken at home. The population examined is only people age 5 or older (`pop_5+`). In the data output, they are placed into three categories:
- `eng_only`: Speak only English
- `ne_very`: Speak a language other than English; Speak English "very well"
- `ne_less`: Speak a language other than English; Speak English less than "very well"

Some calculations were needed to transform the raw Census data to the output data. `eng_only` was calculated by taking the sum of people who speak a non-English language at home (`not_eng_only`) and subtracting that from `pop_5+`. `ne_very` and `ne_less` were not explicitly given in the raw data, and instead were calculated by taking `not_eng_only` and multiplying it by the percent of those people who were reported as speaking English "very well" or less than "very well." (`not_eng_only` is not included in the final output.)


### [Poverty](http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/S1701/0400000US44.06000)

The variables given in the output data area:
- `total_det`: Population for whom poverty status is determined
- `below_pov`: Below poverty level (of the population for whom poverty status is determined)

The population examined is only people "for whom poverty status is determined." This is typically close to, but slightly less than, the total population. Since the poverty rate is calculated as `below_pov` divided by `total_det`, this means that it is really the poverty rate among people for whom poverty status is determined.


### [Race](http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/B03002/0400000US44.06000)

Hispanic or Latino of any race is placed in the `hispanic` category. For people who are not Hispanic or Latino, the following categories have the following meanings:
- `white`: White
- `black`: Black or African American
- `native`: American Indian and Alaska Native
- `asian`: Asian
- `pac`: Native Hawaiian and Other Pacific Islander
- `other`: Some other race
- `multi`: Two or more races


### [Sex](http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/S0101/0400000US44.06000)

This is the most straightforward data set. The variables given are `total`, `male`, and `female`, which are what they sound like.
