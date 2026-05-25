import json
import urllib3
import xml.etree.ElementTree as ET
import gzip
f = urllib3.request("GET", "https://whiplash.cc/api/schedule.php")
data = f.json()
root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself/m3u')
chnllist= ['whiplash', 'whiplashii','whiplashcinema','windowtv','atlas']
displname = ['Whiplash', 'Whiplash II', 'Whiplash Cinema', 'Window TV', 'Atlas']
logolist= ['whiplash', 'whiplash2','whiplashcinema','windowtv','atlas']
for i in chnllist:
    if data[i] != None:
        title = data[i]['title']
        sub = data[i]['sub_title']
        desc = data[i]['desc']
        timezone = data[i]['start'][19:25].replace(':','')
        start = data[i]['start'][0:-6].replace('-','').replace(':','').replace('T','') + " " + timezone
        stop = data[i]['stop'][0:-6].replace('-','').replace(':','').replace('T','') + " " + timezone
        chnl = ET.SubElement(root, 'channel')
        chnl.set('id',i)
        dspl = ET.SubElement(chnl, 'display-name')
        icon = ET.SubElement(chnl, 'icon')
        dspl.text = displname[chnllist.index(i)]
        icon.set('src', f"https://whiplash.cc/assets/img/channels/{logolist[chnllist.index(i)]}.png")
        
        prog = ET.SubElement(root, 'programme')
        prog.set('channel', i)
        prog.set('start', start)
        prog.set('stop', stop)
        progtitle = ET.SubElement(prog, 'title')
        progtitle.text = title
        progdesc = ET.SubElement(prog, 'desc')
        progdesc.text = desc
        progsub = ET.SubElement(prog, 'sub-title')
        progsub.text = sub

xml_data = ET.tostring(root)

with open('./epg/whiplash.xml', 'wb') as g:
    g.write(xml_data)
    print("Exported!")
g.close()

with gzip.open('./epg/whiplash.xml.gz', 'wb') as g:
    g.write(xml_data)
g.close()
