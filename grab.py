#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import config


def view():
    driver.save_screenshot('screen.png')
    os.system("gnome-open screen.png")


driver = webdriver.PhantomJS("./phantomjs")


driver.get('https://czds.icann.org/en')

#import pdb;pdb.set_trace()

print "Logging in"
userF = driver.find_element_by_id("edit-name")
userF.send_keys(config.username)
passF = driver.find_element_by_id("edit-pass")
passF.send_keys(config.password)
time.sleep(0.5)
#submit
view()
submitF = driver.find_element_by_id("edit-submit")
submitF.click()

time.sleep(0.5)
driver.get('https://czds.icann.org/en/request/add')

time.sleep(0.5)

view()

#TODO add secsess check
driver.quit()

