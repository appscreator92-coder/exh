import urllib3
import xml.etree.ElementTree as ET
import pathlib
from lxml import etree
import gzip

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself/m3u')
resp = urllib3.request("GET", "https://olidigital.space/olitv-epg.php")
with open('olitv.xml', 'wb') as f:
    f.write(resp.data)
with open('olitv.xml', 'r', encoding="utf-8-sig") as f:
    text = f.read()
epgroot = ET.fromstring(text, parser=etree.XMLParser(recover=True,encoding='utf-8'))
chnl = ET.SubElement(root, 'channel')
chnl.set('id', 'OLI TV')
dspl = ET.SubElement(chnl, 'display-name')
icon = ET.SubElement(chnl, 'icon')
dspl.text = "Oli TV"
icon.set('src', "https://i.ibb.co/XfvTQyJn/main-removebg-preview.png")

for type_tag in epgroot.findall('programme'):
    title = type_tag.find('title').text
    desctag = type_tag.find('desc')
    desc = desctag.text
    start = type_tag.get("start")
    stop = type_tag.get("stop")
    prog = ET.SubElement(root, 'programme')
    prog.set('channel', "OLI TV")
    prog.set('start', start)
    prog.set('stop', stop)
    progtitle = ET.SubElement(prog, 'title')
    progtitle.text = title
    progdesc = ET.SubElement(prog, 'desc')
    progdesc.text = desc

xml = pathlib.Path("olitv.xml")
xml.unlink()

xml_data = ET.tostring(root)

with open('olitv.xml', 'wb') as f:
    f.write(xml_data)
    print("Exported!")
f.close()

with gzip.open('olitv.xml.gz', 'wb') as g:
    g.write(xml_data)
g.close()
