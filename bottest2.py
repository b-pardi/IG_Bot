from bs4 import BeautifulSoup
import urllib
import requests
from botImports import *

r = requests.get('https://twitter.com/USABillOfRights/status/468852515409502210/photo/1')#, headers = {'HEADERS GO HERE'})
bs = BeautifulSoup(r.content, 'html.parser')
imgUrl = bs.find('img', attrs={'alt': 'Embedded image permalink'}).get('src')
urllib.urlretrieve(imgUrl, "cnn.jpg")

