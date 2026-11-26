"""Research-only Portugalito reconstruction. Never writes production GTFS."""
import json, os, re, math, unicodedata, urllib.request, urllib.parse
from pathlib import Path
OUT=Path("research-output/portugalito")
OUT.mkdir(parents=True,exist_ok=True)
def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD",s.lower()) if not unicodedata.combining(c))
def request(base,suffix,payload,content_type):
    base=os.getenv(base,"").rstrip("/")
    if not base.startswith("https://"): raise SystemExit("Private HTTPS endpoint is not configured")
    url=base if base.endswith("/"+suffix) else base+"/"+suffix
    h={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Content-Type":content_type}
    for key in ("CF_ACCESS_CLIENT_ID","CF_ACCESS_CLIENT_SECRET"):
        if os.getenv(key):h[key.replace("_","-")]=os.environ[key]
    try:
        with urllib.request.urlopen(urllib.request.Request(url,data=payload,headers=h,method="POST"),timeout=240) as r:return json.load(r)
    except Exception as exc:raise SystemExit(f"Private {suffix} request failed: {type(exc).__name__} HTTP {getattr(exc,'code','n/a')}") from None
def overpass(q):
    p=request("API_OVERPASS","interpreter",urllib.parse.urlencode({"data":q}).encode(),"application/x-www-form-urlencoded")
    if p.get("remark") or not p.get("elements"):raise SystemExit("Overpass incomplete or empty")
    return p["elements"]
def dist(a,b):return math.hypot((a[0]-b[0])*111000,(a[1]-b[1])*110600)
def project(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))) if dx or dy else 0
    return [a[0]+dx*t,a[1]+dy*t]
def road_names(w):
    t=w.get("tags",{})
    return " ".join(norm(t.get(k,"")) for k in ("name","alt_name","official_name"))
def roadmatch(w,typ,num):
    names=road_names(w)
    return bool(re.search(r"\b"+typ+r"\s*"+str(num)+r"\b",names))
def coords(w):return [[v["lon"],v["lat"]] for v in w.get("geometry",[]) if v]
roads=overpass('[out:json][timeout:180];way["highway"](4.395,-75.79,4.55,-75.66);out body geom;')
roads=[w for w in roads if w.get("type")=="way" and len(coords(w))>1 and w.get("tags",{}).get("highway") not in {"footway","path","steps","pedestrian","cycleway","construction","proposed","track","bridleway"} and w.get("tags",{}).get("access") not in {"private","no"} and w.get("tags",{}).get("motor_vehicle")!="no"]
pois=overpass('[out:json][timeout:90];(nwr["name"~"Portugalito|B.scula|Caimo|Jardines de Armenia|San Pedro|Tres Esquinas|Cejita|Caza.*Pesca|Tiro.*Pesca",i](4.395,-75.79,4.55,-75.66);node(703492500,703492570,4322327208);way(308547109,294432279););out center;')
(OUT/"osm-landmarks.json").write_text(json.dumps(pois,ensure_ascii=False,indent=2))
report={"status":"UNVERIFIED_RESEARCH_ONLY","source":"BASA website itinerary; OSM road candidates; historical target 43 km","anchors":{},"warnings":[]}
def store(key,p,source,**extra):
    report["anchors"][key]={"point_lon_lat":p,"source":source,**extra}
    return p
def intersection(key,c,k,near):
    a=[w for w in roads if roadmatch(w,"calle|cl",c)]
    b=[w for w in roads if roadmatch(w,"carrera|cra|kr",k)]
    # Each point is a real common OSM road node, not an invented crossing.
    nodes={n for w in b for n in w.get("nodes",[])}
    hits={}
    for w in a:
        for n,v in zip(w.get("nodes",[]),coords(w)):
            if n in nodes:hits[n]=v
    ranked=sorted(hits.items(),key=lambda x:dist(near,x[1]))
    if not ranked or dist(near,ranked[0][1])>800:
        report["warnings"].append(f"Unresolved intersection {key}");return None
    n,p=ranked[0]
    return store(key,p,"OSM common road node",osm_node=n,other_candidates=[{"node":i,"point":v} for i,v in ranked[1:5]])
def snap(key,p,source,predicate=lambda w:True,max_dist=500):
    ranked=[]
    for w in roads:
        if not predicate(w):continue
        c=coords(w); q=min((project(p,a,b) for a,b in zip(c,c[1:])),key=lambda v:dist(p,v))
        d=dist(p,q)
        if d<=max_dist:ranked.append((d,w,q))
    ranked.sort(key=lambda x:x[0])
    if not ranked:
        report["warnings"].append(f"No road candidate for {key}");return None
    d,w,q=ranked[0]
    return store(key,q,source,reference_lon_lat=p,offset_m=round(d,1),osm_way=w["id"],road=w.get("tags",{}).get("name"),alternatives=[{"osm_way":v["id"],"offset_m":round(e,1),"point":z,"road":v.get("tags",{}).get("name")} for e,v,z in ranked[1:4]])
major=lambda w:w.get("tags",{}).get("highway") in {"primary","secondary","tertiary","primary_link","secondary_link","tertiary_link","unclassified","residential"}
arterial=lambda w:w.get("tags",{}).get("highway") in {"primary","secondary","tertiary","primary_link","secondary_link","tertiary_link"}
start=intersection("Calle25_Carrera17",25,17,[-75.6773,4.532])
out16=intersection("Calle25_Carrera16",25,16,[-75.677,4.5315])
out26=intersection("Calle26_Carrera16",26,16,[-75.67698,4.5314])
end26=intersection("Calle26_Carrera17",26,17,[-75.6773,4.53175])
cejita=snap("La_Cejita",[-75.67789,4.53272],"OSM neighbourhood node 5770618450; not exact junction",arterial,350)
c19=snap("Carrera19",[-75.682,4.526],"Approximate search centre; named street candidate",lambda w:roadmatch(w,"carrera|cra|kr",19) or "19 de enero" in road_names(w),900)
tres=snap("Tres_Esquinas",[-75.68884,4.51924],"BASA other-route geometry descriptions, nearby business reference",lambda w:w.get("tags",{}).get("junction")=="roundabout" or arterial(w),350)
calle51=snap("Calle51",[-75.691,4.512],"Street candidate near urban corridor",lambda w:roadmatch(w,"calle|cl",51),900)
jardines=snap("Jardines",[-75.69243,4.50809],"OSM cemetery way 308547109 centroid, road candidate",arterial,600)
granada=snap("Granada",[-75.70219,4.49195],"OSM police node 4322327208, road candidate",major,300)
caimo=snap("El_Caimo",[-75.70938,4.47491],"OSM village node 703492570, road candidate",major,350)
port=snap("Portugalito",[-75.77242,4.41127],"OSM locality node 703492500; turnaround UNVERIFIED",major,700)
basculas=[x for x in pois if re.search("bascula",norm(x.get("tags",{}).get("name",""))) and "lon" in x or re.search("bascula",norm(x.get("tags",{}).get("name",""))) and x.get("center")]
report["bascula_candidates"]=basculas
bascula=None
if len(basculas)==1:
    b=basculas[0];v=b.get("center",b)
    if dist([v["lon"],v["lat"]],[-75.70938,4.47491])<3500:
        bascula=snap("La_Bascula",[v["lon"],v["lat"]],"Named OSM candidate, not verified boarding point",major,250)
if not bascula:report["warnings"].append("La Bascula unresolved; skipped in exploratory routing only")
club=snap("Club",[-75.68823,4.51056],"OSM club way 294432279 centroid, nearby street candidate",lambda w:roadmatch(w,"calle|cl",50) or roadmatch(w,"carrera|cra|kr",8) or arterial(w),600)
c8=snap("Carrera8",[-75.689,4.5095],"Named return street candidate",lambda w:roadmatch(w,"carrera|cra|kr",8),900)
ret50=intersection("Calle50_Carrera18",50,18,[-75.68885,4.518])
ret18=intersection("Calle26_Carrera18",26,18,[-75.678,4.532])
sequence=[start,out16,out26,cejita,c19,tres,calle51,jardines,granada,caimo]+([bascula] if bascula else [])+[port]+([bascula] if bascula else [])+[caimo,granada,jardines,c8,club,ret50,ret18,end26,start]
report["required_anchors_resolved"]=all(p is not None for p in sequence)
report["ordered_points"]=sequence
def save():
    (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
save()
if not report["required_anchors_resolved"]:
    print("Required urban or rural anchor unresolved; no complete shape generated.")
else:
    points=[p for i,p in enumerate(sequence) if i==0 or dist(p,sequence[i-1])>1]
    payload={"profile":"bus","points":points,"points_encoded":False,"instructions":False,"calc_points":True}
    result=request("GRAPHHOPPER_URL","route",json.dumps(payload).encode(),"application/json")
    path=result["paths"][0]
    line=path["points"]["coordinates"]
    if len(line)<3:raise SystemExit("GraphHopper returned no usable geometry")
    report.update(distance_km=round(path["distance"]/1000,3),historical_target_km=43,deviation_km=round(path["distance"]/1000-43,3),travel_minutes=round(path["time"]/60000,1))
    report["warnings"].append("GraphHopper candidate: check snapped points, street directions, turnaround and La Bascula before acceptance. No timetable inferred.")
    geo={"type":"FeatureCollection","features":[{"type":"Feature","properties":{"route":"R-PORTUGALITO","status":"UNVERIFIED_RESEARCH_ONLY"},"geometry":{"type":"LineString","coordinates":line}}]+[{"type":"Feature","properties":{"anchor":k,**{a:b for a,b in v.items() if a!="point_lon_lat"}},"geometry":{"type":"Point","coordinates":v["point_lon_lat"]}} for k,v in report["anchors"].items()]}
    (OUT/"candidate.geojson").write_text(json.dumps(geo,ensure_ascii=False))
    save()
