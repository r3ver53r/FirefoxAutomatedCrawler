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
   
   if url is None:
      return None
   
   #Normalize the URL
   url = normalize(url)
   
   debug("Trying: "+url)
   
   #Check if the URL is already crawled and under scope
   if checkURL(url, Level) == 0:
		debug("Skipping: "+url)
		return
   
   #Browse the url and append to the crawled url_list
   debug("Scanning :-) : "+url)
   driver.get(url)
   url_list += [url]
   
   #sleep for SleepTime seconds to actually let scanning happen
   time.sleep(SleepTime)
   
   #Get all <a href=""> tags
   allTags = driver.find_elements_by_tag_name("a");

   #Get all the link values from the <a> tags and add to the queue
   for tag in allTags:
      links.append( tag.get_attribute('href') )
   
   debug("Extracted links from: "+url)
   
   #Crawl the links on the url page
   for link in links:
      crawl(link, Level - 1) 

def normalize(url):
   
   #Check for '/', '?', '#' as the last char of the URL
   if url[-1] == '/' or url[-1] == '?' or url[-1] == '#':
      url = url[:-1]
      normalize(url)
   
   debug("Normalized: "+str(url))   
   return url
      
def checkURL(url, Level):
   global url_list
   global domains
   global excluded_urls
   valid_scope = 0
   
   #Check if MaxLevel has reached
   if(Level == 0):
		debug("Skipping..MaxLevel Reached!!")
		return 
      
   #check if URL is None
   if url is None:
      return 0
   
   #Check if the URL is not in the excluded list of URLs
   for myurl in excluded_urls:
      if myurl in url:
         return 0
   
   #Check if the URL of same domain or list of domain
   for domain in domains:
      if domain in url:
         valid_scope = 1
   
   if valid_scope == 0:
      debug("Domain not in scope. Skipping!!: "+url)
      return 0   
   
   #Check if URL is already crawled
   if url in url_list:
      return 0
   
   return 1

def debug(debug_string):
   print "DEBUG STRING >>>> "+str(debug_string)
   
crawl(base_url, MaxLevel)     
print "\n\nTotal URLs:" +str(len(url_list))+"\n\n"
print url_list
