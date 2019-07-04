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

def emailit(msg): # can use this function if want to email update instead of tweet it

# !!! Important, way this is setup it will only email if it hasn't been tweeted; if want to do both; should add the
# email stuff to the tweet one !!!

        try:
            
            fromaddr = 'bchydrobot@gmail.com'
            toaddrs  = ['cskeltondata@gmail.com']

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
    
    print section
        
    if 'White Rock' in section.text:
        print "Outages in White Rock"
        emailit("Subject: Power outage in White Rock" + "\nTo: cskeltondata@gmail.com\n\nPower outage in White Rock")   
    else:
        print "No outages in White Rock"
        
    '''
    decisions = table.findAll ("a")
    
    for decision in decisions:
        record = {}
        record["type"] = "B.C. Supreme Court"
        record["citation"] = decision.text
        record["url"] = 'http://www.courts.gov.bc.ca' + decision.get('href')
        tweetit(record)
        
    '''

for x in range (0, 22):
    
    scrape_hydro("https://www.bchydro.com/power-outages/app/outage-list.html#current-521980323")
    time.sleep(3600) # wait one hour, change this to 3600 seconds
