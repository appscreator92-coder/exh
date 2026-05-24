import urllib3
import json
from datetime import datetime
import gzip
import xml.etree.ElementTree as ET

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself')

date = datetime.now().strftime("%d/%m/%Y")
resp = urllib3.request("POST",
                       "https://www.dishtv.in/services/epg/signin")

http = urllib3.PoolManager()
token_data = resp.json()

token = token_data['token']

for i in range(1, 106):
    encoded_body = json.dumps({
        "channelgenre": "",
        "language": "",
        "allowPastEvents": "true",
        "dataSize": "large",
        "pageNum": i,
        "date": datetime.now().strftime("%d/%m/%Y")
    })
    test = http.request("POST",
                        f"https://www.dishtv.in/services/epg/channels?pageNum={i}&date={date}",
                        body=encoded_body,
                        headers={"Authorization-Token": token,
                                 "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryqdpVYTfDycoyAdQG",
                                 "Origin": "https://www.dishtv.in",
                                 "Referer": "https://www.dishtv.in/channel-guide.html",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
                                 "X-Requested-With": "XMLHttpRequest"})

    channellist = test.json()['programDetailsByChannel']
    for j in channellist:
        epgid = j['channelid']
        chnl = ET.SubElement(root, 'channel')
        chnl.set('id', epgid)
        dspl = ET.SubElement(chnl, 'display-name')
        icon = ET.SubElement(chnl, 'icon')
        dspl.text = j['channelname']
        icon.set('src', j['channelimage'])
        lcn = ET.SubElement(chnl, 'lcn')
        lcn.text = j['lcn']

        for prg in channellist[channellist.index(j)]['programs']:
            epgid = prg['channelid']
            start = prg['start'].replace('-','').replace(':','').replace('T','').replace('Z',' +0530')
            stop = prg['stop'].replace('-','').replace(':','').replace('T','').replace('Z',' +0530')
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start)
            prog.set('stop', stop)
            title = prg['title']
            desc = prg['desc']
            cat = prg['genre']
            date = prg['date']
            thumb = prg['programmeurl']
            directors = prg['credits']["directors"]
            producers = prg['credits']["producers"]
            actors = prg["credits"]['actors']
            prgtitle = ET.SubElement(prog, 'title')
            prgtitle.text = title
            prgdesc = ET.SubElement(prog, 'desc')
            prgdesc.text = desc
            prgcat = ET.SubElement(prog, 'category')
            prgcat.text = cat
            prgdate = ET.SubElement(prog, 'date')
            prgdate.text = date
            cred = ET.SubElement(prog, 'credits')
            for k in directors:
                director = ET.SubElement(cred, 'director')
                director.text = k
            for k in actors:
                actor = ET.SubElement(cred, 'actor')
                actor.text = k
            for k in producers:
                producer = ET.SubElement(cred, 'producer')
                producer.text = k
            prgico = ET.SubElement(prog, 'icon')
            prgico.set("src", thumb)

xml_data = ET.tostring(root)

with open('./epg/dishtv.xml', 'wb') as f:
    f.write(xml_data)
    print("Exported!")
f.close()

with gzip.open('./epg/dishtv.xml.gz', 'wb') as f:
    f.write(xml_data)
f.close()
