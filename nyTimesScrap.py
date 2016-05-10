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
from openpyxl.styles import Color, Font, Style, colors, PatternFill
from openpyxl.cell import get_column_letter
from goose import Goose

import os.path
import codecs

import json

yearArry = [2000, 2010]

#Set up
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]
#http://api.nytimes.com/svc/search/v2/articlesearch.json?q=Climate+Change&begin_date=19000101&end_date=19090101&page=1&api-key=sample-key
#URL to open
for year in yearArry:	
	index = 0
	i = index * 10
	query = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=Climate+Change&begin_date="+ str(year) + "0101&end_date="+str(year + 9)+"0101&page="+ str(index) +"&api-key=sample-key"
	response = br.open(query)
	soup = BeautifulSoup(response, "html.parser")
	newDictionary=json.loads(str(soup))
	hits = newDictionary['response']['meta']['hits']

	while i < hits: 
		print i
		index  = index + 1
		i = index * 10
		
		try: 
			try:
				query = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=Climate+Change&begin_date="+ str(year) + "0101&end_date="+str(year + 9)+"0101&page="+ str(index) +"&api-key=sample-key"
				response = br.open(query)
			except Exception, e:
				print e
				continue
			soup = BeautifulSoup(response, "html.parser")
			newDictionary=json.loads(str(soup))
			stories = newDictionary["response"]['docs']

			for x in stories:
				save_path = '/Users/Alice/Desktop/ScrapingGoogle/'
				date = x["pub_date"][:4]
				date = int(date)
				print date
				print year
				save_path = save_path + str(year) + '/'
				print save_path	
				g = Goose()
				url = x["web_url"]
				try:
					print "Hello"
					rep = br.open(url)
					page = BeautifulSoup(rep, "html.parser")
					linkSpan = page.findAll("span", "downloadPDF")[0]
					link = linkSpan("a")[0]['href']
					print link
					title = x["headline"]["main"]
					pathName = str(year) + "/" + title + ".pdf"
					rep = br.open(link)
					page = BeautifulSoup(rep, "html.parser")
					#print page
					button = page.findAll("iframe", id = "archivePDF")[0]
					print button['src']
					# print button
					br.retrieve(button['src'], pathName)[0]
					print i
				except Exception, e:
					article = g.extract(url=url)
					rep = br.open(url)
					page = BeautifulSoup(rep, "html.parser")
					#title = x["headline"]["main"] + ".txt"
					#Get title 
					title = article.title 
					print title
					article = page.findAll("p", itemprop = "articleBody")
					art = ""
					for a in article:
						art += a.text
					title = title + ".txt"
					completeName = os.path.join(save_path, title)
					f = codecs.open(completeName, "w+", "utf-8")
					f.write(art)
					f.close()
					print i
		except Exception, e:
			print e

			continue



#http://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
