''' 
To do:
   check if the browser is crashed 
   check if the response of a URL is 200 ok
   
'''
from selenium import webdriver
import time

MaxLevel = 5
SleepTime= 10
fp = webdriver.FirefoxProfile("E:/PenTest/FirefoxProfile")                 
driver = webdriver.Firefox(fp) 
url_list = []
base_url = 'http://coursera.org'
domains  = ["https://coursera.org", "http://coursera.org", "https://www.coursera.org", "https://www.coursera.org"]
excluded_urls = ["https://coursera.org/logout"]


def crawl(url, Level):
   global url_list
   global SleepTime
   links = []
   
   print "Trying URL: "+str(url)
   
   #Check if the URL is already crawled and under scope
   if checkURL(url) == 0:
		print "Skipping !!"
		return
   
   #Check if MaxLevel has reached
   if(Level == 0):
		print "Skipping..MaxLevel Reached!!"
		return 
      
   #Browse the url and append to the crawled url_list
   print "Scanning :-)"
   driver.get(url)
   url_list += [url]
   
   #sleep for SleepTime seconds to actually let scanning happen
   time.sleep(SleepTime)
   
   #Get all <a href=""> tags
   allTags = driver.find_elements_by_tag_name("a");

   #Get all the link values from the <a> tags and add to the queue
   for tag in allTags:
      links.append( tag.get_attribute('href') )
   
   print "Extracted links from: "+url
   
   #Crawl the links on the url page
   for link in links:
      crawl(link, Level - 1) 

def normalize(url):
   
   if url is None:
      return None
      
   #Check for '/', '?', '#' as the last char of the URL
   if url[-1] == '/' or url[-1] == '?' or url[-1] == '#':
      print "Normalizing: "+str(url)
      url = url[:-1]
      normalize(url)
         
   return url
      
def checkURL(url):
   global url_list
   global domains
   global excluded_urls
   valid_scope = 0
   
   #check if URL is None
   if url is None:
      return 0
   
   #Normalize the URL
   url = normalize(url)
   
   #Check if the URL is not in the excluded list of URLs
   for myurl in excluded_urls:
      if myurl in url:
         return 0
   
   #Check if the URL of same domain or list of domain
   for domain in domains:
      if domain in url:
         valid_scope = 1
   
   if valid_scope == 0:
      print "Domain not in scope. Skipping!!"
      return 0   
   
   #Check if URL is already crawled
   if url in url_list:
      return 0
   
   return 1

      
crawl(base_url, MaxLevel)     
print "\n\nTotal URLs:" +str(len(url_list))+"\n\n"
print url_list
