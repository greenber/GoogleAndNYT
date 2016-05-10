import urllib
import mechanize
from bs4 import BeautifulSoup
import re
import xlwt
import unicodedata
import csv
import xlrd
import time
from random import randint
import openpyxl
import os.path
import codecs
import unicodedata

#Set up
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]

#This is hard coded in since you only game me one to do
url ="http://anom.archivesnationales.culture.gouv.fr/ir?ir=FRANOM_00083&start=&persname=&geogname=Bamako+%28Mali%29&corpname_ordre_religieux=&corpname_maison_commerce=&corpname_peuple=&corpname_nationalite=&corpname_bateau=&q=&date=&from=&to="
#URL to open
response = br.open(url)

#make it into a BS object
soup = BeautifulSoup(response, "html.parser")

root = soup.findAll("ul", "root")[0]

urls = root.findAll("a")


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def findShit(urlsList):
	for u in urlsList:
		u = "http://anom.archivesnationales.culture.gouv.fr" + u["href"]
		print u
		response = br.open(u)
		soup = BeautifulSoup(response, "html.parser")
		record = soup.findAll("blockquote")
		#print record
		doc = ""
		labels = soup.findAll("h1", "unittitle")
		if (len(record) != 0):
			#Makes the document 
			for docs in record:
				doc = doc + docs.text
			save_path = '/Users/Alice/Desktop/ScrapingGoogle/iRel'
			title = remove_accents( labels[0].text.replace("\\", ""))
			print title
			#20 was randomly choosen =/ Seem like a nice number 
			#Write to file
			title = title[:20] + ".txt"
			completeName = os.path.join(save_path, title)
			f = codecs.open(completeName, "w+", "utf-8")
			f.write(doc)
			f.close()
		else:
			block = soup.findAll("ul", "child")[0]
			urls = block.findAll("a")
			findShit(urls)



findShit(urls)











