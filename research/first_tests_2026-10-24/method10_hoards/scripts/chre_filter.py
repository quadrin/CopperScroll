import csv,sys,json
rows=list(csv.DictReader(open(sys.argv[1],encoding='utf-8')))
def f(x):
    try: return float(x)
    except: return None
out=[]
for r in rows:
    t1=f(r['terminalYear1']); t2=f(r['terminalYear2'])
    lat=f(r['latitude']); lon=f(r['longitude'])
    tt=[x for x in (t1,t2) if x is not None]
    if not tt: 
        dated='nodate'
    elif max(tt) < -63 or min(tt) > 136:
        continue
    inbox = lat is not None and lon is not None and 29.5<=lat<=33.4 and 34.2<=lon<=36.0
    r['_inbox']=inbox
    out.append(r)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
for r in out:
    print(r['id'],'|',r['hoardName'],'|n=',r['coinCount'],'|',r['latitude'][:7],r['longitude'][:7],'box' if r['_inbox'] else 'OUT','|T',r['terminalYear1'],r['terminalYear2'],'|',r['summary'][:200].replace('\n',' '))
