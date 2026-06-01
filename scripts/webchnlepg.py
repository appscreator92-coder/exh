import json
import urllib3
import xml.etree.ElementTree as ET
import gzip
urls = ['https://whiplash.cc/scheds/wl.xml', 'https://whiplash.cc/scheds/win.xml', 'http://45.153.245.180/epgs/spark/epg.xml']
for i in urls:
    f = urllib3.request("GET", i)
    data = ET.fromstring(f.data)
    root = ET.Element('tv')
    root.set('generator-info-url', 'https://github.com/amazeyourself/m3u')
    if 'whiplash.cc' in i:
        idlist = ["C1.145.ersatztv.org", 'C2.1.147.ersatztv.org', 'C3.1.148.ersatztv.org', 'C3.147.ersatztv.org', 'C7.151.ersatztv.org']
        chnllist= ['whiplash', 'whiplashii','whiplashcinema','windowtv','atlas']
        displname = ['Whiplash', 'Whiplash II', 'Whiplash Cinema', 'Window TV', 'Atlas']
        logolist= ['whiplash', 'whiplash2','whiplashcinema','windowtv','atlas']
        for j in data.findall("channel"):
            if j.get("id") in idlist:
                chnl = ET.SubElement(root, 'channel')
                chnl.set('id',chnllist[idlist.index(j.get("id"))])
                dspl = ET.SubElement(chnl, 'display-name')
                icon = ET.SubElement(chnl, 'icon')
                dspl.text = displname[idlist.index(j.get("id"))]
                icon.set('src', f'https://whiplash.cc/assets/img/channels/{logolist[idlist.index(j.get("id"))]}.png')

        for j in data.findall("programme"):
            epgid = j.get("channel")
            if epgid in idlist:
                title = j.find('title').text
                if j.find('sub-title') != None:
                    sub = j.find('sub-title').text
                if j.find('desc') != None:
                    desc = j.find('desc').text
                if j.find('rating') != None:
                    rating = j.find('rating').text
                start = j.get("start")
                stop = j.get("stop")
                prog = ET.SubElement(root, 'programme')
                prog.set('channel', chnllist[idlist.index(epgid)])
                prog.set('start', start)
                prog.set('stop', stop)
                progtitle = ET.SubElement(prog, 'title')
                progtitle.text = title
                if j.find('desc') != None:
                    progdesc = ET.SubElement(prog, 'desc')
                    progdesc.text = desc
                if j.find('sub-title') != None:
                    progsub = ET.SubElement(prog, 'sub-title')
                    progsub.text = sub
                if j.findall('category') != None:
                    for cat in j.findall('category'):
                        progcat = ET.SubElement(prog, 'category')
                        progcat.text = cat.text
                if j.find('rating') != None:
                    prograting = ET.SubElement(prog, 'rating')
                    prograting.text = rating
    else:
        for j in data.findall("channel"):
            chnl = ET.SubElement(root, 'channel')
            chnl.set('id',j.get("id"))
            dspl = ET.SubElement(chnl, 'display-name')
            icon = ET.SubElement(chnl, 'icon')
            dspl.text = j.find("display-name").text
            if j.find('icon') == None:
                icon.set('src', j.find('img').get("src"))
            else:
                icon.set('src', j.find('icon').get("src"))
                
        for j in data.findall("programme"):
            title = j.find('title').text
            if j.find('sub-title') != None:
                sub = j.find('sub-title').text
            if j.find('desc') != None:
                desc = j.find('desc').text
            start = j.get("start")
            stop = j.get("stop")
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', chnllist[idlist.index(epgid)])
            prog.set('start', start)
            prog.set('stop', stop)
            progtitle = ET.SubElement(prog, 'title')
            progtitle.text = title
            if j.find('desc') != None:
                progdesc = ET.SubElement(prog, 'desc')
                progdesc.text = desc
            if j.find('sub-title') != None:
                progsub = ET.SubElement(prog, 'sub-title')
                progsub.text = sub
            if j.findall('category') != None:
                for cat in j.findall('category'):
                    progcat = ET.SubElement(prog, 'category')
                    progcat.text = cat.text

xml_data = ET.tostring(root)

with open('./epg/webchnl.xml', 'wb') as g:
    g.write(xml_data)
    print("Exported!")
g.close()

with gzip.open('./epg/webchnl.xml.gz', 'wb') as g:
    g.write(xml_data)
g.close()
