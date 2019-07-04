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

    CitationText = record["citation"]
        
    query = "SELECT count(*) FROM swdata WHERE url = '" + record["url"] + "'"
    count = scraperwiki.sqlite.execute(query)
    countcheck = count['data'][0][0]
    if countcheck > 0:
        print "Already in database"
    if countcheck == 0:
        try:
            print "New record"
            scraperwiki.sqlite.save(['url'], record)
            
            # Writing the message
            
            fromaddr = 'bchydrobot@gmail.com'
            toaddrs  = ['cskelton@vancouversun.com','cskeltonnews@gmail.com'] # or adrienne or bev
            msg = "Subject: New court ruling - " + record["citation"] + "\nTo: cskelton@vancouversun.com; cskeltonnews@gmail.com\n\nJust posted from " + record["type"] + ": '" + CitationText + "' " + record["url"]
            
            # Gmail login
            
            username = 'bchydrobot'
            password = os.environ['MORPH_PASSWORD']
            
            # Sending the mail 
            
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            
            time.sleep(30)
            
        except:
            print "Unable to add to table or email"
    
def scrape_hydro(url): # in case page changes

    html = requests.get(url)
    htmlpage = html.content
    
    soup = BeautifulSoup(htmlpage)
    
    section = soup.find ("table", {"class" : "current-521980323"})
    
    print section

    '''
    decisions = table.findAll ("a")
    
    for decision in decisions:
        record = {}
        record["type"] = "B.C. Supreme Court"
        record["citation"] = decision.text
        record["url"] = 'http://www.courts.gov.bc.ca' + decision.get('href')
        tweetit(record)
        
    '''


for x in range (0, 1):
    
    time.sleep(100) # wait one hour, change this to 3600 seconds
    
    scrape_hydro("https://www.bchydro.com/power-outages/app/outage-list.html#current-521980323")
    
