from time import sleep
import requests as r
import datetime as d

urls = open('urls.txt').readlines()

def dl(url):
    res = None
    try:
        res = r.get(url, stream=True)
    except:
        print d.datetime.now(), 'request failed'
    else:
        if res.status_code != 200:
            print d.datetime.now(), 'failed with status', res.status_code
        for chunk in res.iter_content(chunk_size=1024): 
            pass

while True:
    for url in urls:
        if not url:
            continue

        url = url.strip()

        print d.datetime.now(), 'getting', url
        dl(url)
