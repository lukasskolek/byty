import requests
import re
import time
from random import randint
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen
import json
import os
from bs4 import BeautifulSoup as bs

# print ("done importing")

cache = []
time.sleep(randint(1, 30))
if os.path.isfile('./cachefile_byty.json'):
    with open('./cachefile_byty.json') as fh:
        try:
            cache = json.load(fh)
        except json.decoder.JSONDecodeError:
            os.remove('./cachefile_byty.json')
url = "https://www.byty.sk/okres-bratislava-i/2-izbove-byty/predaj/?p[param1][to]=220000&p[order]=1"
url2 = "https://www.byty.sk/okres-bratislava-i/3-izbove-byty/predaj/?p[param1][to]=250000&p[order]=1"
page = urlopen(url)
page2 = urlopen(url2)
soup = bs((page.read()), features="lxml")

vsetky = [x for x in set(filter(lambda x: '4273' in x, [x.get('href') for x in soup.find_all('a')]))]
new = [x for x in filter(lambda x: x not in cache, vsetky)]
cache += new
byty = 'Tieto su nove: \n'
for x in new:
    byty += x + '\n'

with open('./cachefile_byty.json', 'w') as fh:
    json.dump(cache, fh)

if new:
    msg = EmailMessage()
    msg.set_content(byty)
    toaddrs = 'luky.skolek@gmail.com', 'kristina.lappyova@gmail.com'
    msg['From'] = 'diery2020cierne@gmail.com'
    msg['To'] = ", ".join(toaddrs)
    msg['Subject'] = 'Aha, novy byt!'
    fromaddr = 'diery2020cierne@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('diery2020cierne@gmail.com', '3P6ciaUaLJiraKk')
    server.send_message(msg)
    server.quit()
    response = urlopen(url).read()
else:
    print('All has been seen')
