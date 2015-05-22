from time import sleep
import datetime as d
from subprocess import Popen
import json
import signal
import sys

config = json.loads(open('config.json', 'r').read())

class Downloader(object):
    def __init__(self):
        self.process = None

    def start(self):
        if self.process is not None:
            raise Exception('Cannot start process twice')
        
        self.process = Popen(['/usr/bin/env', 'python', config["dl_abs_script_path"]])

    def stop(self):
        if self.process is None:
            raise Exception('Process is already started')

        self.process.kill()
        self.process = None

    def started(self):
        return self.process is not None

def interval_to_datetimes(interval):
    now = d.datetime.now()
    interval_start = d.datetime(year=now.year,
                                month=now.month,
                                day=now.day,
                                hour=interval["start"]["h"],
                                minute=interval["start"]["m"])
    interval_end = interval_start + d.timedelta(minutes=interval["duration"])

    return { "start": interval_start, "end": interval_end }

def time_in_interval(time, interval):
    return time > interval["start"] and time < interval["end"]

def time_in_any_interval(time, intervals):
    for i in map(interval_to_datetimes, intervals):
        if time_in_interval(time, i):
            return True
    return False

def kill_downloader_and_exit(signal, frame):
    if dl.started():
        dl.stop()
    exit(0)

dl = Downloader()
intervals = config["intervals"]

signal.signal(signal.SIGINT, kill_downloader_and_exit)
signal.signal(signal.SIGTERM, kill_downloader_and_exit)

while True:  
    if time_in_any_interval(d.datetime.now(), intervals) and not dl.started():
        dl.start()
        print 'started downloader'
    elif dl.started():
        dl.stop()
        print 'stopped downloader'

    sleep(60)
