#!/usr/bin/env python

import time
import config
import os
import traceback
from selenium import webdriver
import random
import sys

path = os.path.dirname(os.path.realpath(__file__))

def getDriver():
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
    driver.step = "log-in"
    userF = driver.find_element_by_id("edit-name")
    userF.send_keys(config.username)
    passF = driver.find_element_by_id("edit-pass")
    passF.send_keys(config.password)
    time.sleep(0.1)

    #submit
    driver.step = "log-in submit"
    submitF = driver.find_element_by_id("edit-submit")
    submitF.click()
    time.sleep(0.1)

    # auth check
    driver.step = "log-in check"
    #title = driver.find_element_by_id("page-title")
    #title = driver.find_element_by_class_name('title')
    title = driver.title
    #print "title " +title
    if title == "Access denied":
        print "Access denied"
        return
    time.sleep(0.1)

    #request page
    driver.step = "request zone"
    time.sleep(0.1)
    driver.get('https://czds.icann.org/en/request/add')
    time.sleep(0.1)

    #select zones
    driver.step = "select zones"
    approvedF = driver.find_element_by_id("tld-filter-approved")
    approvedF.click()
    pendingF = driver.find_element_by_id("tld-filter-pending")
    pendingF.click()
    time.sleep(0.1)
    allF = driver.find_element_by_id("edit-tlds-fieldset-tld-all")
    if not allF.is_enabled():
        #no zones to request
        driver.step = "no zones found"
        return
    allF.click()
    #enter reason
    driver.step = "entering reason"
    reasonF = driver.find_element_by_id("edit-reason")
    reasonF.send_keys(config.request_message)
    time.sleep(0.1)

    #next form page
    driver.step = "next page 1"
    nextF = driver.find_element_by_id("edit-next1")
    nextF.click()
    time.sleep(0.1)

    #agree to terms
    driver.step = "agree to terms"
    termsF = driver.find_element_by_id("edit-agree-tc")
    termsF.click()
    #next form page
    driver.step = "next page 2"
    nextF = driver.find_element_by_id("edit-next2")
    nextF.click()
    time.sleep(0.1)

    #empty ip field
    driver.step = "blank ip"
    ipF = driver.find_element_by_id("edit-ips-from-request-ip-0")
    ipF.clear()
    time.sleep(0.1)
    #submit
    driver.step = "final submit"
    requestBF = driver.find_element_by_id("edit-submit")
    requestBF.click()
    time.sleep(20)

    #success check
    driver.step = "success check"
    try:
        zonesE = driver.find_element_by_xpath("//p[contains(text(), 'You have requested zone files for the following TLD')]/following-sibling::p")
    except:
        #debug
        print "unable to find result text"
        print ''
        driver.save_screenshot(path+'/error.png')
        with open(path+"/error.html", "w") as errorHTML:
            errorHTML.write(driver.page_source.encode('utf-8').strip())
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
        traceback.print_exc()
    else:
        try:
            # start fresh
            driver.delete_all_cookies()
            request(driver)
        except:
            print "error while requesting"
            print driver.current_url
            print "step: "+ driver.step
            print ""
            traceback.print_exc()
            with open(path+"/error.html", "w") as errorHTML:
                errorHTML.write(driver.page_source.encode('utf-8').strip())
            # print repr(driver.page_source)
        finally:
            driver.quit()

if __name__ == "__main__":
    run()

