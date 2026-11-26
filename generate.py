"""Research-only BASA GTFS builder; no live API calls."""
import argparse,csv,io,json,math,zipfile
from pathlib import Path
from collections import defaultdict
from datetime import date,timedelta
from shapely.geometry import Point,LineString
from pyproj import Transformer
P=Path(__file__).resolve().parent
T=Transformer.from_crs(4326,32618,always_xy=True)
OPS={'R1':(95,11),'R2':(120,10),'R3':(60,3),'R4':(115,14),'R5':(86,5),'R6':(92,5),'R7':(78,3),'R9':(96,8),'R18':(110,11),'R28':(100,10),'R31':(80,2),'R32':(100,5),'R35':(75,13),'R36':(95,12),'R37':(93,7)}
HOLD={'R9':'44.7 km geometry vs historical 32 km; cycle unverified','R24':'No frequency','R25':'No frequency','R33':'No frequency; long geometry segment','R-EXPRESA':'Shared realtime identifier; combined dispatch allocation unknown','R-EXP-GIB':'Shared realtime identifier; combined dispatch allocation unknown','R-PORTUGALITO':'No shape and special timetable unknown'}
def load(n):return json.loads((P/'data'/n).read_text(encoding='utf-8'))
def hh(s):return f'{s//3600:02}:{s//60%60:02}:{s%60:02}'
def build(out,start,end,first,last):
    catalog=load('routes.json'); raw=defaultdict(list)
    for x in load('shapes.json'):raw[x['ruta']].append(x)
    osm=load('osm.json')['elements']; nodes={x['id']:x for x in osm if x['type']=='node'}
    stops={}
    for k,x in nodes.items():
        t=x.get('tags',{}); name=t.get('name','')
        if (t.get('highway')=='bus_stop' or (t.get('public_transport')=='platform' and t.get('bus')=='yes')) and 'jeep' not in name.lower():
            stops[k]=x
    tables=defaultdict(list); report=[]; used=set()
    def add(f,**kw):tables[f].append(kw)
    add('agency',agency_id='BASA',agency_name='Buses Armenia S.A.',agency_url='https://www.busesarmenia.com.co/',agency_timezone='America/Bogota',agency_lang='es')
    add('calendar',service_id='draft_weekday',monday=1,tuesday=1,wednesday=1,thursday=1,friday=1,saturday=0,sunday=0,start_date=start.strftime('%Y%m%d'),end_date=end.strftime('%Y%m%d'))
    import holidays
    co=holidays.country_holidays('CO',years=range(start.year,end.year+1))
    for d in sorted(co):
        if start<=d<=end and d.weekday()<5:add('calendar_dates',service_id='draft_weekday',date=d.strftime('%Y%m%d'),exception_type=2)
    for r in catalog:
        rid=r['ruta']; sid=r['polyPasa']; info={'route':rid,'source_shape':sid,'status':'held','reason':HOLD.get(rid,'')}
        report.append(info)
        if r['estado']!='Activo' or rid in HOLD or rid not in OPS or len(raw[sid])<2:continue
        a=raw[sid]
        if rid=='R28':
            cuts=[i for i in range(1,len(a)) if int(a[i]['id'])-int(a[i-1]['id'])!=1]
            assert cuts==[328],cuts
            a=a[328:]; info['geometry_note']='Second ID block 7353–7680 retained; first block excluded; not a verified newer revision.'
        coords=[]
        for x in reversed(a):
            v=(float(x['cy']),float(x['cx']))
            if not coords or v!=coords[-1]:coords.append(v)
        xy=[T.transform(*v) for v in coords]; line=LineString(xy)
        matches=[]
        for k,x in stops.items():
            pt=Point(T.transform(x['lon'],x['lat'])); dist=line.distance(pt)
            if dist<=30:
                along=line.project(pt)
                matches.append((along,k,dist))
        matches.sort(); info.update(length_km=round(line.length/1000,2),candidate_stops=len(matches),shape_points=len(coords))
        if len(matches)<2:info['reason']='Fewer than 2 candidate stops';continue
        cycle,buses=OPS[rid]; headway=math.ceil(cycle/buses)*60
        add('routes',route_id=rid,agency_id='BASA',route_short_name=rid,route_long_name='',route_type=3,route_color=r['colorPoly'].lstrip('#').upper())
        trip=rid+'_draft'; add('trips',route_id=rid,service_id='draft_weekday',trip_id=trip,shape_id=rid)
        add('frequencies',trip_id=trip,start_time=first,end_time=last,headway_secs=headway,exact_times=0)
        cumulative=0
        for i,(lon,lat) in enumerate(coords):
            if i:cumulative+=math.dist(xy[i-1],xy[i])
            add('shapes',shape_id=rid,shape_pt_lat=lat,shape_pt_lon=lon,shape_pt_sequence=i+1,shape_dist_traveled=round(cumulative,3))
        prev=0
        for i,(along,k,dist) in enumerate(matches):
            x=stops[k]; used.add(k); sec=max(prev,round((along-matches[0][0])/line.length*cycle*60));prev=sec
            add('stop_times',trip_id=trip,arrival_time=hh(sec),departure_time=hh(sec),stop_id=f'osm_{k}',stop_sequence=i+1,shape_dist_traveled=round(along,3),timepoint=0)
        info.update(status='draft',reason='',headway_seconds=headway,cycle_minutes=cycle)
    for k in sorted(used):
        x=stops[k]; name=x.get('tags',{}).get('name') or f'Paradero OSM {k}'
        if name == 'PARQUE LA CONSTITUCIÓN': name = 'Parque La Constitución'
        add('stops',stop_id=f'osm_{k}',stop_name=name,stop_lat=x['lat'],stop_lon=x['lon'])
    add('feed_info',feed_publisher_name='ColombiaTransit research draft',feed_publisher_url='https://github.com/ColombiaTransit',feed_lang='es',feed_start_date=start.strftime('%Y%m%d'),feed_end_date=end.strftime('%Y%m%d'),feed_version='draft-0.1',feed_contact_url='https://github.com/ColombiaTransit/gtfs-armenia/issues')
    assert tables['trips'] and tables['stops']
    routeids={x['route_id'] for x in tables['routes']}; tripids={x['trip_id'] for x in tables['trips']}; stopids={x['stop_id'] for x in tables['stops']}
    assert all(x['route_id'] in routeids for x in tables['trips'])
    assert all(x['trip_id'] in tripids and x['stop_id'] in stopids for x in tables['stop_times'])
    for trip in tripids:
        rows=[x for x in tables['stop_times'] if x['trip_id']==trip]; assert len(rows)>=2 and all(a['shape_dist_traveled']<=b['shape_dist_traveled'] and a['departure_time']<=b['arrival_time'] for a,b in zip(rows,rows[1:]))
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for name,rows in tables.items():
            if not rows:continue
            b=io.StringIO(); w=csv.DictWriter(b,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);z.writestr(name+'.txt',b.getvalue())
    result={'draft_only':True,'counts':{k:len(v) for k,v in tables.items()},'routes':report,'physical_osm_candidates':len(stops),'basic_checks':'passed'}
    out.with_suffix('.report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=P/'gtfs-armenia-draft.zip');p.add_argument('--start',type=date.fromisoformat,required=True);p.add_argument('--end',type=date.fromisoformat,required=True);p.add_argument('--first',default='05:00:00');p.add_argument('--last',default='22:00:00');p.add_argument('--allow-estimates',action='store_true');a=p.parse_args()
    if not a.allow_estimates:p.error('Research only: explicitly acknowledge estimated schedules with --allow-estimates')
    if a.end<a.start or a.first>=a.last:p.error('Invalid dates or service window')
    build(a.output,a.start,a.end,a.first,a.last)
