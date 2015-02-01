#!/usr/bin/env python

import time
import config
import os
import traceback
from selenium import webdriver
import random
import sys

def getDriver():
    path = os.path.dirname(os.path.realpath(__file__))
    driver = webdriver.PhantomJS(path+"/phantomjs")
    driver.set_window_size(1366,768)
    time.sleep(0.5)
    return driver

def getRemoteDriver():
    driver = webdriver.Remote(
            desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
            command_executor='http://127.0.0.1:4444:/wd/hub'
            )
    time.sleep(0.5)
    return driver

def request(driver):
    driver.get('https://czds.icann.org/en')
   
    if driver.page_source == "<html><head></head><body></body></html>":
        print "Got blank page, exiting"
        return

#log in
    userF = driver.find_element_by_id("edit-name")
    userF.send_keys(config.username)
    passF = driver.find_element_by_id("edit-pass")
    passF.send_keys(config.password)
    time.sleep(0.1)
#submit
    submitF = driver.find_element_by_id("edit-submit")
    submitF.click()

#request page
    time.sleep(0.1)
    driver.get('https://czds.icann.org/en/request/add')
    time.sleep(0.1)
#select zones
    approvedF = driver.find_element_by_id("tld-filter-approved")
    approvedF.click()
    pendingF = driver.find_element_by_id("tld-filter-pending")
    pendingF.click()
    time.sleep(0.1)
    allF = driver.find_element_by_id("edit-tlds-fieldset-tld-all")
    if not allF.is_enabled():
#no zones to request
        return
    allF.click()
#enter reason
    reasonF = driver.find_element_by_id("edit-reason")
    reasonF.send_keys(config.request_message)
    time.sleep(0.1)

#next form page
    nextF = driver.find_element_by_id("edit-next1")
    nextF.click()
    time.sleep(0.1)

#agree to terms
    termsF = driver.find_element_by_id("edit-agree-tc")
    termsF.click()
#next form page
    nextF = driver.find_element_by_id("edit-next2")
    nextF.click()
    time.sleep(0.1)

#empty ip field
    ipF = driver.find_element_by_id("edit-ips-from-request-ip-0")
    ipF.clear()
    time.sleep(0.1)
#submit
    requestBF = driver.find_element_by_id("edit-submit")
    requestBF.click()
    time.sleep(0.1)

#success check
    try:
        zonesE = driver.find_element_by_xpath("//p[contains(text(), 'You have requested zone files for the following TLD')]/following-sibling::p")
    except:
        #debug
        print "unable to find result text"
        print ''
        print repr(driver.page_source)
        driver.save_screenshot('error.png')
    else:
        zonesNum = len(zonesE.text.split())

        print "Requested %d zones: " % zonesNum
        print zonesE.text.upper()


def run():
    #driver = getDriver()
    try:
        driver = getRemoteDriver()
    except:
        print "FAIL: Unable to connect to Driver"
    else:
        try:
            request(driver)
        except:
            print "error while requesting"
            print driver.current_url
            print ""
            traceback.print_exc()
            print repr(driver.page_source)
        finally:
            driver.quit()

if __name__ == "__main__":
    run()

