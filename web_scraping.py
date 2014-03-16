from selenium import webdriver

import sys, re
import optparse 
from pprint import pprint
import time

class Site(object):
    def __init(self):
        self.url = ""
        self.csv = ""
        self.prod = ""
        self.desc = ""
        self.was = ""
        self.now = ""
        self.size = ""
        

class Boot(object):
    """docstring for FlightInfo"""
    def __init__(self):
        self.brand = ''
        self.name = ''
        self.size = ''
        self.origPrice = 0.0
        self.currPrice = 0.0
        self.save = 0.0
        self.discount = 0
        self.url = ""

    def load(self, brand, name, size, was, now, url):
        self.brand = brand
        self.name = name
        self.size = size
        self.origPrice = float(was)
        self.currPrice = float(now)
        self.save = max(self.origPrice - self.currPrice, 0)
        if self.origPrice != 0:
            self.discount = (self.save / self.origPrice) *100
        else:
            self.discount = 0.0
        self.url = url

    def dump(self):
        rtn = ""
        rtn += '"' + self.brand + '",'
        rtn += '"' +self.name + '",'
        rtn += '"' +self.size + '",'
        rtn += '"' +str(self.origPrice) + '",'
        rtn += '"' +str(self.currPrice) + '",'
        rtn += '"' +str(self.save) + '",'
        rtn += '"%.2f"' % self.discount + '%,' 
        rtn += self.url+','
        return rtn

def loadPage(browser, url):
    browser.get(url)
    info_list = browser.page_source.split('\n')
    return info_list

def writeLog(url_list):
    fw = open('url.log', 'w')
    for url in url_list:
        fw.write(url.encode('ascii','ignore') + '\n')
    fw.close()

def getOption():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--size", dest="size",
                      help="place of departure ")
    parser.add_option("-t", "--destination", dest="destination",
                      help="place of arrive")
    parser.add_option("-d", "--depart_date", dest="depart_date",
                      help="depart date")
    parser.add_option("-r", "--return_date", dest="return_date",
                      help="return date")
    (options, args) = parser.parse_args()
    return options

def SelectBrowser():
    browsers = [webdriver.Safari, webdriver.Chrome, webdriver.Firefox, webdriver.ie, webdriver.Opera ]

    for b in browsers:
        try:
            browser = b()
            return browser
        except:
            continue

def process(browser, site):
    #infoList = loadPage(browser, url)
    print site.url
    browser.get(site.url)
    bootList = browser.find_elements_by_class_name(site.prod)
    rtnList = []
    for boot in bootList:
        a = boot.find_element_by_xpath('a')
        url = a.get_attribute('href')
        url = url.encode('ascii', 'ignore')
        descBlk = boot.find_element_by_class_name(site.desc)
        wasBlk = boot.find_element_by_class_name(site.was)
        nowBlk = boot.find_element_by_class_name(site.now)
        if site.size != "NONE":
            sizeBlk = boot.find_element_by_class_name(site.size)
        else:
            sizeBlk = descBlk
        desc = descBlk.text.encode('ascii', 'ignore')
        dl = desc.split()
        brand = dl[0]
        name = " ".join(dl[1:])
        was = wasBlk.text.encode('ascii', 'ignore')
        was = was.split(':')[-1]
        size = sizeBlk.text.encode('ascii', 'ignore')
        if "PDS" in was:
            was = '0.0'
        now = nowBlk.text.encode('ascii', 'ignore')
        now = now.split(':')[-1]
        b = Boot()
        b.load(brand, name, size,was, now,url)
        rtnList.append(b)
    return rtnList

def run(site):
    options = getOption()
    print "LOAD Page"
    browser = SelectBrowser()
    #browser = webdriver.Remote(url, webdriver.DesiredCapabilities.HTMLUNIT.copy())
    bList = process(browser, site)
    fo = open(site.csv, 'w')
    title = "brand, name, size, Orig, Current, Save, Discount, Url,"
    print title
    fo.write(title+"\n")
    for b in bList:
        line = b.dump()
        #print line
        fo.write(line+"\n")
    fo.close()
    browser.quit()
    print 'DONE'

def runSoccer():
    soccer = Site()
    soccer.url = 'http://www.prodirectsoccer.com/lists/football-boots.aspx?listName=football-boots&s=7.5_8&p=all'
    soccer.csv ='football.csv'
    soccer.prod = 'list_productentity'
    soccer.desc = 'list_description'
    soccer.was = 'list_pricesalewas'
    soccer.now = 'list_price'
    soccer.size = 'list_description_sizes'

    run(soccer)

def runRunning():
    running = Site()
    running.url = 'http://www.prodirectrunning.com/lists/running-shoes.aspx?s=8_7.5&p=all'
    running.csv = 'running.csv'
    running.prod = "list_productentity"
    running.desc = 'list_description'
    running.was = 'list_pricesalewas'
    running.now = 'list_price'
    running.size = "NONE"

    run(running)

def runTrainer():
    running = Site()
    running.url = 'http://www.prodirectselect.com/lists/trainers.aspx?listName=trainers&s=7.5_8&p=all'
    running.csv = 'trainer.csv'
    running.prod = "list_productentity"
    running.desc = 'list_description'
    running.was = 'list_pricesalewas'
    running.now = 'list_price'
    running.size = "list_description_sizes"

    run(running)


if __name__ == "__main__":
    runSoccer()
    runRunning()
    runTrainer()
    
 
    
    #main(runUrl, runCsv)
