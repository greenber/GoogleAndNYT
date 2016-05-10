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
from mechanize import ParseResponse, urlopen, urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
import codecs

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]

##Change to change what you search
array = ["climate change poverty"]
print array[0]

for x in array:
	driver = webdriver.Firefox()
	driver.get("http://jpe.library.arizona.edu/")
	elem = driver.find_element_by_id("gsc-i-id1")
	elem.send_keys(x)
	elem.send_keys(Keys.RETURN)
	num = driver.find_elements_by_class_name("gsc-cursor-page")
	#For loop of pages
	index = 1
	while (len(num) > index):
		content = driver.page_source
		page = BeautifulSoup(content, "html.parser")
		elements = page.findAll("div", "gsc-webResult gsc-result")
		#for Loop for every element on the page
		for w in elements:
			url = w.findAll("a", "gs-title")[0]['href']
			title = w.findAll("a", "gs-title")[0].text
			typeOfPage = w.findAll("a", "gs-title")[0]["data-ctorig"]
			length = len(typeOfPage)
			if ((typeOfPage[(length - 4):] == ".htm")) or ((typeOfPage[(length - 5):] == ".html")):
				rep = br.open(url)
				page  = BeautifulSoup(rep, "html.parser")
				art = page.findAll("p", False) #PRobs can't do this
				article = ""
				for z in art:
					article += z.text 
				save_path = '/Users/Alice/Desktop/ScrapingGoogle/UOfA/' + x + "/"
				fo = codecs.open(title+".txt", "w+", "utf-8")
				fo.write(article)
				fo.close()
			else:
				try: 
					br.retrieve(url, title + ".pdf")[0]
				except Exception, e:
					print e
		num[index].click()
		num = driver.find_elements_by_class_name("gsc-cursor-page")
		print num[index]
		index = index + 1
		print index
		







#content = driver.page_source

#print content


driver.close()


#Cit: 
#
