import bs4
import requests
import re
import hashlib
import time

def get_availability_string():
    url="https://www.gef.be.ch/gef/de/index/Corona/Corona/corona_impfung_bern.html"

    page=requests.get(url).content

    soup = bs4.BeautifulSoup(page, 'lxml')


    # find elements that contain the data we want
    found = soup.find_all("h3", string=re.compile("Sind Termine verfügbar"))

    result = ''
    for x in found:
        result = result + str(x.find_next_sibling('p'))
    return result

result = get_availability_string()
initialString = hashlib.sha224(result.encode()).hexdigest()
print('Initial text: ' + result)
while True:
    time.sleep(600)
    result = get_availability_string()
    if initialString != hashlib.sha224(result.encode()).hexdigest():
        print('Availability has changed: ' + result)
        initialString = hashlib.sha224(result.encode()).hexdigest()



