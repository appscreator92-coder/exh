import urllib3
import json
import gzip

resp = urllib3.request(
    "GET",
    "https://tv.jsrdn.com/tv_v5/getfeed.php?type=live")

jsonresp = resp.json()

stringdata = json.dumps(jsonresp['shows'], indent=4)
channel_data = json.loads(stringdata)
ids = channel_data.keys()
names=[]
logos=[]
epgids=[]

for i in ids:
    name = channel_data[i]['title']
    logo = channel_data[i]['img_logo']
    epg = channel_data[i]['seasons'][0]['episodes'][0]['id']
    names.append(name)
    logos.append(logo)
    epgids.append(str(epg))

xmltv = ['<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE tv SYSTEM "xmltv.dtd"><tv generator-info-name="https://github.com/amazeyourself/m3u">']
idlist = ",".join(epgids)
resp = urllib3.request(
    "GET",
    f"https://tv.jsrdn.com/epg/query.php?range=-96h,72h&id={idlist}")

jsonresp = resp.json()

stringdata = json.dumps(jsonresp['epg'], indent=4)
epgdata = json.loads(stringdata)
ids = epgdata.keys()

for i in ids:
    xmltv.append(f'<channel id="{i}">')
    xmltv.append(f'<display-name>{names[epgids.index(i)]}</display-name>')
    xmltv.append(f'<icon src="{logos[epgids.index(i)]}"/>')
    xmltv.append('</channel>')

for i in ids:
    if epgdata[i] != {}:
        for j in epgdata[i]['slots']:
            start = j['start'].replace('-','').replace(':','').replace(' ','') + " +0000"
            stop = j['end'].replace('-','').replace(':','').replace(' ','') + " +0000"
            xmltv.append(f'<programme channel="{i}" start="{start}" stop="{stop}">')
            xmltv.append(f'<title>{j["title"]}</title>')
            xmltv.append(f'<desc>{j["description"]}</desc>')
            xmltv.append(f'<icon src="{j["img_thumbh"]}"/>')
            xmltv.append('<rating>')
            if j['rating'] != 'null':
                xmltv.append(f'<value>{j["rating"]}</value>')
            else:
                xmltv.append('<value>NA</value>')
            xmltv.append('</rating>')
            xmltv.append('</programme>')


xmltv.append('</tv>')

with open('./epg/distrotv.xml', 'w', newline='', encoding="utf-8") as f:
    for lines in xmltv:
        f.write(f'{lines}\n')
f.close()

with gzip.open('./epg/distrotv.xml.gz', 'wb') as g:
    for lines in xmltv:
        g.write(f'{lines}')
g.close()
