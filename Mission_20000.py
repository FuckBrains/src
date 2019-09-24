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



def web_submit(submit,chrome_driver,debug=0):
    try:
        chrome_driver.get('https://stripchat.com')
    except:
        pass
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    cookie_ = '[{"domain": "stripchat.com", "expiry": 1600716196, "httpOnly": false, "name": "baseAmpl", "path": "/", "secure": false, "value": "%7B%22platform%22%3A%22Web%22%2C%22device_id%22%3A%225949384b-41ac-42e8-a445-418bb76ce912R%22%2C%22session_id%22%3A1569180105643%2C%22up%22%3A%7B%22page%22%3A%22view%22%2C%22navigationParams%22%3A%7B%22limit%22%3A60%2C%22offset%22%3A0%7D%7D%7D"}, {"domain": "stripchat.com", "expiry": 1569180243, "httpOnly": false, "name": "_gat", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716185, "httpOnly": false, "name": "guestWatchHistoryIds", "path": "/", "secure": false, "value": ""}, {"domain": "stripchat.com", "expiry": 1600716124.14764, "httpOnly": true, "name": "stripchat_com_ABTest_recommended_key", "path": "/", "secure": false, "value": "B"}, {"domain": "stripchat.com", "expiry": 1569266581, "httpOnly": false, "name": "_gid", "path": "/", "secure": false, "value": "GA1.2.572702782.1569180106"}, {"domain": "stripchat.com", "expiry": 1632252181, "httpOnly": false, "name": "_ga", "path": "/", "secure": false, "value": "GA1.2.54903429.1569180106"}, {"domain": "stripchat.com", "expiry": 1571772198.044346, "httpOnly": true, "name": "stripchat_com_sessionRemember", "path": "/", "secure": true, "value": "1"}, {"domain": "stripchat.com", "expiry": 1571772198.044113, "httpOnly": true, "name": "stripchat_com_sessionId", "path": "/", "secure": true, "value": "f97a85844eae195aa598cc7c9134a5e6a19a64e139be5f0c2e1e8a78404a"}, {"domain": "stripchat.com", "expiry": 1600716105, "httpOnly": false, "name": "alreadyVisited", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716185, "httpOnly": false, "name": "isVisitorsAgreementAccepted", "path": "/", "secure": false, "value": "1"}, {"domain": "stripchat.com", "expiry": 1600716198, "httpOnly": false, "name": "guestSubscriptionIds", "path": "/", "secure": false, "value": ""}, {"domain": "stripchat.com", "expiry": 253402257600, "httpOnly": false, "name": "G_ENABLED_IDPS", "path": "/", "secure": false, "value": "google"}, {"domain": "stripchat.com", "expiry": 1884540186, "httpOnly": false, "name": "amplitude_id_19a23394adaadec51c3aeee36622058dstripchat.com", "path": "/", "secure": false, "value": "eyJkZXZpY2VJZCI6IjU5NDkzODRiLTQxYWMtNDJlOC1hNDQ1LTQxOGJiNzZjZTkxMlIiLCJ1c2VySWQiOiIyMTIyNjU5MCIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU2OTE4MDEwNTY0MywibGFzdEV2ZW50VGltZSI6MTU2OTE4MDE4NjA1MywiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6OSwic2VxdWVuY2VOdW1iZXIiOjl9"}, {"domain": "stripchat.com", "expiry": 1600716125.042566, "httpOnly": true, "name": "stripchat_com_modelLandingNamespace", "path": "/", "secure": false, "value": "none"}, {"domain": "stripchat.com", "expiry": 1576956185.479051, "httpOnly": true, "name": "stripchat_com_affiliateId", "path": "/", "secure": false, "value": "1240cbd3455450b5c499e77219039717203959411ca4f7e1d644be59ffb037fc"}]'
    cookies = json.loads(cookie_)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry']) 
        chrome_driver.add_cookie(cookie)    
    chrome_driver.get('http://stripchat.com')
    sleep(3000)
    