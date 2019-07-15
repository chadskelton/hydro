# Load in modules
# !!! NOTE - When doing a more general News Bot, should probably create another field that describes the data
# (i.e. "New Court Decision") and one that has the email of the person to notify (as this may vary depending
# on the site scraped. Could then have one script grabbing dozens of different sites and notifying
# dozens of different reporters/editors !!!

import scraperwiki
import tweepy
import time
from datetime import datetime
import smtplib
import requests
from BeautifulSoup import BeautifulSoup
# new for secret variables
import os
import mechanize

def emailit(record): # can use this function if want to email update instead of tweet it

# !!! Important, way this is setup it will only email if it hasn't been tweeted; if want to do both; should add the
# email stuff to the tweet one !!!
	time.sleep(60)
	
	query = "SELECT count(*) FROM swdata WHERE url = '" + record["updated"] + "'"
	count = scraperwiki.sqlite.execute(query)
    	countcheck = count['data'][0][0]
    	if countcheck > 0:
        	print "Already in database"
    	if countcheck == 0:
        	try:
			print "New record"
			scraperwiki.sqlite.save(['updated'], record)
	
            
			fromaddr = 'bchydrobot@gmail.com'
			toaddrs  = ['cskeltondata@gmail.com']
			msg = "Subject: Power outage in White Rock" + "\nTo: cskeltondata@gmail.com\n\nPower outage in White Rock at" + record["area"] + "affecting " + record["out"])

			# Gmail login

			username = 'bchydrobot'
			password = os.environ['MORPH_PASSWORD']

			# Sending the mail 

			server = smtplib.SMTP("smtp.gmail.com:587")
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr, toaddrs, msg)
			server.quit()
			
			
		except:
			print "Unable to add to table or email"

def scrape_hydro(url): # in case page changes

    html = requests.get(url)
    htmlpage = html.content
    
    soup = BeautifulSoup(htmlpage)
    
    section = soup.find ("div", {"id" : "current-521980323"})
    
    # print section
        
    table = section.find ("table", {"class": "municipality-list table-striped scroll-body sortable-table"})

    rows = table.findAll("tr")
        
    for row in rows:
        print row

        cells = row.findAll("td")
            
        try:
		record = {}
                record["municipality"] = cells[0].text
                record["offsince"] = cells[1].text
                record["status"] = cells[2].text
                record["area"] = cells[3].text
                record["out"] = cells[4].text
                record["cause"] = cells[5].text
                record["updated"] = cells[6].text
		
		print record
                # if "White Rock" in record["municipality"]:
                if "Surrey" in record["municipality"]:
                          print "Outage in White Rock"
                          emailit(record)
                else:
                          print "No outages in White Rock"
        except:  
                          
              print 'Problem scraping row'            
'''
    try:    
        if 'White Rock' in section.text:
            print "Outages in White Rock"
            emailit("Subject: Power outage in White Rock" + "\nTo: cskeltondata@gmail.com\n\nPower outage in White Rock")   
        else:
            print "No outages in White Rock"
    except:    
        print "Couldn't check for White Rock (possibly blank page)"
'''

for x in range (0, 1): # trying 15 instead of 22
    print "Cycle:" + str(x)
 
    scrape_hydro("https://www.bchydro.com/power-outages/app/outage-list.html#current-521980323")
    # time.sleep(3600) # wait one hour, change this to 3600 seconds
