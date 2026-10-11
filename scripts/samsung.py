from concurrent.futures import ThreadPoolExecutor, as_completed
import pathlib
import xml.etree.ElementTree as ET
import requests

regioncodes = ['all', 'at', 'ca', 'ch', 'de', 'es', 'fr', 'gb', 'in', 'it', 'kr', 'us']

# Ensure the output directory exists
output_dir = pathlib.Path('./samsungtvplus')
output_dir.mkdir(parents=True, exist_ok=True)

# Custom HTTP headers to avoid request blocking during redirect resolution
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def resolve_redirect(channel_info):
    """
    Follows HTTP redirects for a single channel and returns the final target URL.
    """
    chnlid, name, ico = channel_info
    redirect_url = f'https://jmp2.uk/stvp-{chnlid}'
    
    try:
        # HEAD request is faster than GET as it avoids downloading the body content
        resp = requests.head(redirect_url, headers=HTTP_HEADERS, allow_redirects=True, timeout=10)
        final_url = resp.url
    except Exception as e:
        print(f"[!] Error resolving {chnlid}: {e}")
        final_url = redirect_url  # Fallback to original URL if request fails
        
    return chnlid, name, ico, final_url


for region in regioncodes:
    print(f"\n[*] Processing region: {region}")
    
    url = f'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/SamsungTVPlus/{region}.xml'
    
    resp = requests.get(url, headers=HTTP_HEADERS)
    if resp.status_code != 200:
        print(f"[-] Failed to fetch region {region}: HTTP {resp.status_code}")
        continue

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"[-] XML parsing error for region {region}: {e}")
        continue

    # Gather channels list
    channels = []
    for type_tag in root.findall('channel'):
        chnlid = type_tag.get('id')
        
        name_elem = type_tag.find('display-name')
        name = name_elem.text if name_elem is not None and name_elem.text else 'Unknown'
        
        ico_elem = type_tag.find('icon')
        ico = ico_elem.get('src', '') if ico_elem is not None else ''
        
        channels.append((chnlid, name, ico))

    print(f"[*] Resolving redirects for {len(channels)} channels in parallel...")
    
    # Resolve redirect URLs concurrently using ThreadPoolExecutor
    resolved_channels = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(resolve_redirect, ch) for ch in channels]
        for future in as_completed(futures):
            resolved_channels.append(future.result())

    # Build the M3U playlist file content
    playlist = [f'#EXTM3U x-tvg-url="https://i.mjh.nz/SamsungTVPlus/{region}.xml.gz"']
    for chnlid, name, ico, stream_url in resolved_channels:
        playlist.append(f'#EXTINF:-1 tvg-id="{chnlid}" tvg-name="{name}" tvg-logo="{ico}",{name}')
        playlist.append(stream_url)

    output_path = output_dir / f'{region}.m3u'
    with open(output_path, 'w', encoding='utf-8') as g:
        g.write('\n'.join(playlist) + '\n')
        
    print(f'[+] Successfully saved: {output_path}')
