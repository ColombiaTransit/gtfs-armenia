import json
from pathlib import Path
import urllib.request
p=Path(__file__).resolve().parent/'data'
p.mkdir(exist_ok=True)
query='[out:json][timeout:180];(nwr["highway"="bus_stop"](4.35,-75.85,4.65,-75.58);nwr["public_transport"="platform"](4.35,-75.85,4.65,-75.58););out body;'
import urllib.parse
sources={'routes.json':'https://www.busesarmenia.com.co/grivera/get-data.php','shapes.json':'https://logirastreo.com/rutas_buses_armenia.php','osm.json':'https://overpass-api.de/api/interpreter?'+urllib.parse.urlencode({'data':query})}
for name,url in sources.items():
    if (p/name).exists(): continue
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ColombiaTransit GTFS research/0.1','Accept':'application/json'}),timeout=240) as r:
        data=json.load(r)
    if not data or (name=='osm.json' and not data.get('elements')): raise ValueError(name+' empty')
    (p/name).write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
