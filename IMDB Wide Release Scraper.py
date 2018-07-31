#!/usr/bin/env python
"""IMDB Scraper.py: A script to download the basic metadata of wide release movies from IMDB and save to a CSV."""
__author__ = "Reid Pickford"
__Date__ = 7/29/2018
__license__ = "GPL"

import pickle
import urllib.request

origin = 'https://www.imdb.com/list/ls057823854/'
template1 = "?st_dt=&mode=detail&page="
template2 = "&sort=release_date,asc"
#I checked in advance the number of pages, this can be edited as data set grows
num_pages = 100

#Downloading HTML to memory for all 100 pages
#WARNING: Saves to memory ~250mb in addition to multiple pages being parsed, moderately resource intensive for duration of script
SOURCE_FILE = 'imdb_source_release.p'
source = pickle.load(open(SOURCE_FILE, 'rb'))
print("Downloading "+str(num_pages)+" Pages:")
for page in range(1, num_pages+1):
    url = origin + template1 + str(page) + template2
    print("Reading Page: "+str(page))
    with urllib.request.urlopen(url) as file:
        html = file.read()
        source.append(html)
print("Complete")
        
#Headers that precede desired metadata (first 2 unique to title and year, 3rd common but first one after year always precedes the score)
header1 = "lister-item-header"
header2 = "lister-item-year text-muted unbold"
header3 = "<strong title=\""
Title = list()
Year = list()
Length = list()
Rating = list()

#Finds and returns the first title after giving it the index of the preceding header1 (start), and the html string
def titleFinder(start, string):
    st = 0
    end = string.find("</a>",start)
    flag = 0
    derp = int(end)
    while flag==0:
        if page[derp-1:derp] == ">":
            flag = 1
            st = int(derp)
        else:
            derp -= 1
    return string[st:end].replace("\\","").replace("\"","").replace(","," ")
	
#Returns the year found after supplying the index of the header2 preceding it
def yearFinder(start, string):
    flag = 0
    derp = int(start)
    while flag==0:
        if page[derp:derp+4].isnumeric():
            flag = 1
        else:
            derp += 1
    return string[derp:derp+4]
	
#Using the index of the header3 as start (immediately preceding header2, this is important) this will return the average user rating
def ratingFinder(start,string):
    return string[start+15:start+18].replace(" b","")

#Movies on the page, there are 100 (except the last page)
#Don't account for last page because it's just pre-release anyway
for i in range(0,99):
    page = str(source[i])
    index = 0
    for j in range(0,100):
        #For some reason the first and only first page has some parsing issue which results in a single off collection
        if(i==0 and j == 99):
            print("Parsing Data")
        else:
            index = page.find(header1,index)
            Title.append(titleFinder(index,page))
            index = page.find(header2,index)
            Year.append(yearFinder(index,page))
            index = page.find(header3,index)
            Rating.append(ratingFinder(index,page))

#Writing to file as csv, filter movies that don't have ratings out and those before 1972 and after 2017 (list incomplete before then so data not useable)
file = open("IMDB_Data.csv","w")    
file.write("Title, Year, Rating\n")
for i in range(0,len(Year)):
    if(Rating[i]!="CTY" and int(Year[i])>1971 and int(Year[i])<2018):
        file.write(str(Title[i])+","+str(Year[i])+","+str(Rating[i])+"\n")
file.close()