import emaillink
from time import sleep
import random
import os
import time
import sys
import json
import re
from urllib import request, parse
import name_get
import Chrome_driver
import email_imap as imap
import db



def web_submit(submit):
    chrome_driver = Chrome_driver.get_chrome(submit)
    try:
    	chrome_driver.get(submit['Site'])
    except Eexception as e:
    	print(str(e))
    a = input('Input to start next Mission:')
    chrome_driver.close()
    chrome_driver.quit()