import json
import os
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error

p=Path(__file__).resolve().parent/'data'
p.mkdir(exist_ok=True)
query='[out:json][timeout:180];(nwr["highway"="bus_stop"](4.35,-75.85,4.65,-75.58);nwr["public_transport"="platform"](4.35,-75.85,4.65,-75.58););out body;'
sources={'routes.json':'https://www.busesarmenia.com.co/grivera/get-data.php','shapes.json':'https://logirastreo.com/rutas_buses_armenia.php'}
for name,url in sources.items():
    if (p/name).exists(): continue
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ColombiaTransit GTFS research/0.1','Accept':'application/json'}),timeout=240) as r:
        data=json.load(r)
    if not data: raise ValueError(name+' empty')
    (p/name).write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
if not (p/'osm.json').exists():
    endpoint=os.environ.get('API_OVERPASS','').strip()
    if not endpoint: raise SystemExit('Missing organization variable API_OVERPASS; public fallback disabled')
    if not endpoint.startswith('https://'): raise SystemExit('API_OVERPASS must use HTTPS')
    endpoint=endpoint.rstrip('/')
    if not endpoint.endswith('/interpreter'):
        endpoint += '/interpreter'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'es-CO,es;q=0.9,en;q=0.8','Content-Type':'application/x-www-form-urlencoded'}
    try:
        request=urllib.request.Request(endpoint,data=urllib.parse.urlencode({'data':query}).encode(),headers=headers,method='POST')
        with urllib.request.urlopen(request,timeout=240) as response:
            data=json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f'Private Overpass returned HTTP {exc.code}') from None
    except Exception as exc:
        raise SystemExit(f'Private Overpass request failed ({type(exc).__name__})') from None
    if not isinstance(data,dict) or not data.get('elements') or data.get('remark'):
        raise SystemExit('Private Overpass returned empty or incomplete data')
    (p/'osm.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    print(f'Private Overpass: {len(data["elements"])} elements fetched')
