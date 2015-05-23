from time import sleep
import requests as r
import datetime as d

urls = open('urls.txt').readlines()

def dl_pipe_to_dev_null(url):
    res = None
    try:
        res = r.get(url, stream=True)
    except:
        print d.datetime.now(), 'request failed'
    else:
        if res.status_code != 200:
            print d.datetime.now(), 'failed with status', res.status_code
        with open('/dev/null', 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

while True:
    for url in urls:
        if not url:
            continue

        url = url.strip()

        print d.datetime.now(), 'getting', url
        dl_pipe_to_dev_null(url)
