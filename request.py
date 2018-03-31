#!/usr/bin/env python

import time
import config
import os
import traceback
from selenium import webdriver
import random
import sys

path = os.path.dirname(os.path.realpath(__file__))

debug = False

def printd(data):
    if debug:
        print(data)

def getDriver():
    driver = webdriver.PhantomJS(path+"/phantomjs")
    driver.set_window_size(1366,768)
    time.sleep(0.5)
    return driver

def getRemoteDriver():
    driver = webdriver.Remote(
            #desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
            desired_capabilities=webdriver.DesiredCapabilities.CHROME,
            command_executor='http://127.0.0.1:4444:/wd/hub'
            )
    time.sleep(0.5)
    return driver

def request(driver):
    driver.get('https://czds.icann.org/en')
    time.sleep(5)
   
    if driver.page_source == "<html><head></head><body></body></html>":
        print "Got blank page, exiting"
        return

    #log in
    driver.step = "log-in"
    printd(driver.step)
    userF = driver.find_element_by_id("edit-name")
    userF.send_keys(config.username)
    passF = driver.find_element_by_id("edit-pass")
    passF.send_keys(config.password)
    time.sleep(0.1)

    #submit
    driver.step = "log-in submit"
    printd(driver.step)
    submitF = driver.find_element_by_id("edit-submit")
    submitF.click()
    time.sleep(2)

    # auth check
    driver.step = "log-in check"
    printd(driver.step)
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
    printd(driver.step)
    time.sleep(0.1)
    driver.get('https://czds.icann.org/en/request/add')
    time.sleep(5)

    #select zones
    driver.step = "select zones"
    printd(driver.step)
    approvedF = driver.find_element_by_id("tld-filter-approved")
    approvedF.click()
    pendingF = driver.find_element_by_id("tld-filter-pending")
    pendingF.click()
    time.sleep(0.1)
    allF = driver.find_element_by_id("edit-tlds-fieldset-tld-all")
    if not allF.is_enabled():
        #no zones to request
        driver.step = "no zones found"
        printd(driver.step)
        return
    allF.click()
    #enter reason
    driver.step = "entering reason"
    printd(driver.step)
    reasonF = driver.find_element_by_id("edit-reason")
    reasonF.send_keys(config.request_message)
    time.sleep(0.1)

    #next form page
    driver.step = "next page 1"
    printd(driver.step)
    nextF = driver.find_element_by_id("edit-next1")
    nextF.click()
    time.sleep(5)

    #agree to terms
    driver.step = "agree to terms"
    printd(driver.step)
    termsF = driver.find_element_by_id("edit-agree-tc")
    termsF.click()
    time.sleep(5)
    #next form page
    driver.step = "next page 2"
    printd(driver.step)
    nextF = driver.find_element_by_id("edit-next2")
    nextF.click()
    time.sleep(5)

    #empty ip field
    driver.step = "blank ip"
    printd(driver.step)
    ipF = driver.find_element_by_id("edit-ips-from-request-ip-0")
    ipF.clear()
    time.sleep(0.1)
    #submit
    driver.step = "final submit"
    printd(driver.step)
    requestBF = driver.find_element_by_id("edit-submit")
    requestBF.click()
    time.sleep(60)

    #success check
    driver.step = "success check"
    printd(driver.step)
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
        printd("getting driver")
        driver = getRemoteDriver()
    except:
        print "FAIL: Unable to connect to Driver"
        traceback.print_exc()
    else:
        try:
            # start fresh
            printd("deleting cookies and trying requesting driver")
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

