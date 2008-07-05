#!/usr/bin/python

import feedparser, datetime

import sys
sys.path.append('/django/deployment')
d = feedparser.parse('http://metalab.at/wiki/index.php?title=Spezial:Letzte_%C3%84nderungen&feed=atom')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "mos.settings"

from mos import settings

from mos.rss.models import Change

for x in d.entries:
    
    updated = datetime.datetime(*x.updated_parsed[0:6])
    
    preexisting = Change.objects.filter(title=x.title, link=x.link, author=x.author, updated=updated)
    
    if len(preexisting) > 0:
        continue
    
    change = Change(title=x.title, link=x.link, author=x.author, updated=updated)
    change.save()
