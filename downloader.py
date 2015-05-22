from time import sleep
import requests as r

urls = open('urls.txt').readlines()

while True:
    for url in urls:
        print 'getting', url
        r.get(url)
