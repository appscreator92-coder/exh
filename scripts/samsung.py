import requests
import os
import xml.etree.ElementTree as ET

regioncodes=['all','at','ca','ch','de','es','fr','gb','in','it','kr','us']
for region in regioncodes:
    playlist = [f'#EXTM3U x-tvg-url="https://i.mjh.nz/SamsungTVPlus/{region}.xml.gz"']

    url = f'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/SamsungTVPlus/{region}.xml'

    resp = requests.get(url)

    with open(f'samsung_{region}.xml', 'wb') as f:
        f.write(resp.content)

    root = ET.parse(f'samsung_{region}.xml').getroot()

    for type_tag in root.findall('channel'):
        chnlid = type_tag.get('id')
        name = type_tag[0].text
        ico = type_tag[1].get('src')
        playlist.append(f'#EXTINF:-1 tvg-id="{chnlid}" tvg-name="{name}" tvg-logo="{ico}",{name}')
        playlist.append(f'https://jmp2.uk/stvp-{chnlid}')

    with open(f'samsung_{region}.m3u', 'w') as g:
        for line in playlist:
            g.write(f"{line}\n")

    g.close()

    if os.path.exists(f"samsung_{region}.xml"):
        os.remove(f"samsung_{region}.xml")
