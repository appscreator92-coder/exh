import requests
import pathlib
import xml.etree.ElementTree as ET

regioncodes=['all','ar','br','ca','cl','de','dk','es','fr','gb','it','mx','no','se','us']
for region in regioncodes:
    playlist = [f'#EXTM3U x-tvg-url="https://i.mjh.nz/PlutoTV/{region}.xml.gz"']

    url = f'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/{region}.xml'

    resp = requests.get(url)

    with open(f'pluto_{region}.xml', 'wb') as f:
        f.write(resp.content)

    root = ET.parse(f'pluto_{region}.xml').getroot()

    for type_tag in root.findall('channel'):
        chnlid = type_tag.get('id')
        name = type_tag[0].text
        ico = type_tag[1].get('src')
        playlist.append(f'#EXTINF:-1 tvg-id="{chnlid}" tvg-name="{name}" tvg-logo="{ico}",{name}')
        playlist.append(f'https://jmp2.uk/plu-{chnlid}.m3u8')

    with open(f'./plutotv/{region}.m3u', 'w') as g:
        for line in playlist:
            g.write(f"{line}\n")

    g.close()
    xml = pathlib.Path(f"pluto_{region}.xml")
    xml.unlink()
