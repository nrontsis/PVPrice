import urllib.request
import urllib.error
from datetime import datetime
import os
from pathlib import Path
import time

def wait_for_internet_connection():
    for i in range(3600):
        try:
            response = urllib.request.urlopen('http://www.google.com',timeout=1)
            return
        except urllib.error.URLError:
            time.sleep(1)
            pass

wait_for_internet_connection()

opener = urllib.request.build_opener()
# Adding a header to avoid 403 forbidden errors
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')]
urllib.request.install_opener(opener)
now = datetime.now()

dirpath = str(Path(__file__).parent) + '/websites/pvinsights.com/' + now.strftime("%Y%m%d%H%M%S") + '/'
os.mkdir(dirpath)
filename = 'index.html'
urllib.request.urlretrieve('http://pvinsights.com/index.php', dirpath + filename)

dirpath = str(Path(__file__).parent) + '/websites/energytrend.com/' + now.strftime("%Y%m%d%H%M%S") + '/'
os.mkdir(dirpath)
filename = 'solar-price.html'
urllib.request.urlretrieve('https://www.energytrend.com/solar-price.html', dirpath + filename)
print('Done!')
time.sleep(2)
