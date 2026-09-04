from pathlib import Path
import json, re
from collections import Counter

p=Path('index.html')
s=p.read_text(encoding='utf-8')
m=re.search(r'(<script type="application/json" id="data">\s*)(\{.*?\})(\s*</script>)',s,re.S)
if not m: raise SystemExit('inline schedule data not found')
data=json.loads(m.group(2))

# Naming only: Latoya Manier is displayed as Manier everywhere.
def rename(v):
    if isinstance(v,dict):
        out={}
        for k,val in v.items():
            nk='Manier' if k=='Latoya' else k
            out[nk]=rename(val)
        return out
    if isinstance(v,list): return [rename(x) for x in v]
    if isinstance(v,str): return v.replace('Latoya','Manier')
    return v
data=rename(data)

STAFF=['Lingam','Evans','Manier','Abby','Meda']
ROTATORS=['Lingam','Evans','Manier','Abby']
data['staff']=STAFF

off={
 ('Meda','2026-09-04'),('Meda','2026-10-02'),('Meda','2026-11-06'),
 ('Lingam','2027-01-15'),('Meda','2027-01-15'),('Meda','2027-02-12'),
 ('Manier','2027-04-30')
}

# Explicit live regular-coverage assignments. Two rotating teachers each date.
regular_pairs={
 '2026-09-04':('Abby','Evans'),
 '2026-09-11':('Manier','Lingam'),
 '2026-09-25':('Abby','Evans'),
 '2026-10-02':('Manier','Lingam'),
 '2026-10-16':('Abby','Evans'),
 '2026-10-30':('Manier','Lingam'),
 '2026-11-06':('Abby','Evans'),
 '2026-11-20':('Manier','Lingam'),
 '2026-12-04':('Abby','Evans'),
 '2026-12-11':('Manier','Lingam'),
 '2026-12-18':('Abby','Evans'),
 '2027-01-08':('Manier','Lingam'),
 '2027-01-15':('Abby','Evans'),
 '2027-01-22':('Manier','Lingam'),
 '2027-02-05':('Abby','Evans'),
 '2027-02-12':('Manier','Lingam'),
 '2027-02-19':('Abby','Evans'),
 '2027-03-05':('Manier','Lingam'),
 '2027-03-19':('Abby','Evans'),
 '2027-04-02':('Manier','Lingam'),
 '2027-04-09':('Abby','Evans'),
 '2027-04-16':('Manier','Lingam'),
 '2027-04-30':('Abby','Evans'),
 '2027-05-07':('Manier','Lingam'),
 '2027-05-14':('Abby','Evans'),
}

# Training structure: morning pair, stay-back teacher, morning teacher who joins training.
training_plan={
 '2026-09-18':(('Evans','Manier'),'Evans','Manier'),
 '2026-10-23':(('Lingam','Abby'),'Lingam','Abby'),
 '2026-11-13':(('Manier','Evans'),'Manier','Evans'),
 '2027-01-29':(('Abby','Lingam'),'Abby','Lingam'),
 '2027-02-26':(('Evans','Abby'),'Evans','Abby'),
 '2027-03-26':(('Manier','Lingam'),'Manier','Lingam'),
 '2027-04-23':(('Abby','Evans'),'Abby','Evans'),
}

for f in data['fridays']:
    d=f['date']; typ=f['type']
    if d < '2026-09-04':
        # Preserve historical assignments, only ensure current display-name key exists.
        st=f.get('status',{})
        for name in STAFF:
            st.setdefault(name,'OFF')
        f['status']=st
        continue
    if typ=='REGULAR FRIDAY':
        pair=regular_pairs[d]
        if any((name,d) in off for name in pair):
            raise SystemExit(f'hard-off conflict in regular pair {d}: {pair}')
        f['morning1'],f['morning2']=pair
        f['morningExtra']=''
        f['studentCoverage']='Assigned rotating teachers continue to 1:00'
        f['officeCoverage']='Jenny 7:30–11:30 | Cortni 9:30–1:30'
        f['training']='—'
        f['note']='Two rotating teachers provide Friday coverage. Meda is standing campus support when available. Student day ends at 1:00; assigned staff remain through 1:30.'
        st={name:'OFF' for name in STAFF}
        for name in pair: st[name]='Full Day 7:30–1:30'
        if ('Meda',d) not in off: st['Meda']='Full Day 7:30–1:30'
        f['status']=st
    elif typ=='TRAINING FRIDAY':
        pair,stay,join=training_plan[d]
        if any((name,d) in off for name in STAFF):
            raise SystemExit(f'unhandled training-day hard off on {d}')
        f['morning1'],f['morning2']=pair
        f['morningExtra']=''
        f['studentCoverage']=f'Cortni + {stay} 11:30–1:00'
        f['officeCoverage']='Jenny 7:30–11:30 | OPEN 11:30–1:30 (Admin to assign)'
        attendees=[name for name in STAFF if name!=stay]
        f['training']=', '.join(attendees)+' 11:30–1:30'
        f['note']=f'{stay} stays with Cortni and misses training. {join} covers the morning and joins training at 11:30. Office coverage remains open for administration to assign.'
        st={name:'Training 11:30–1:30' for name in STAFF}
        st[stay]='Full-Day Coverage — Misses Training'
        st[join]='Morning Coverage + Training'
        f['status']=st
    elif typ=='NO SCHOOL / NO SCHEDULE':
        f['morning1']=f['morning2']='—'; f['morningExtra']=''
        f['studentCoverage']=f['officeCoverage']=f['training']='—'
        f['status']={name:'CLOSED' for name in STAFF}

# Rebuild summary from actual live statuses.
working={'Full Day 7:30–1:30','Morning Coverage + Training','Training 11:30–1:30','Full-Day Coverage — Misses Training','On Campus (Completed)'}
months=data['months']
summary=[]
for name in STAFF:
    month_counts={mo:0 for mo in months}
    total=missed=0
    for f in data['fridays']:
        st=f.get('status',{}).get(name,'OFF')
        if st in working:
            total+=1
            from datetime import datetime
            dt=datetime.strptime(f['date'],'%Y-%m-%d')
            mo=dt.strftime('%b %Y')
            if mo in month_counts: month_counts[mo]+=1
        if st=='Full-Day Coverage — Misses Training': missed+=1
    summary.append({'name':name,'months':month_counts,'total':total,'trainingsMissed':missed})
data['summary']=summary
data['summaryIntro']='A workday includes regular Friday coverage, standing campus support, training attendance, or pre-training coverage.'
data['fairness']='Regular rotating coverage is balanced across the four rotating teachers after approved availability constraints. Meda is standing Friday campus support when available, so her workday total is not part of the rotating-teacher fairness comparison.'

# Founding-document invariant checks.
types=Counter(f['type'] for f in data['fridays'])
assert len(data['fridays'])==42
assert types==Counter({'REGULAR FRIDAY':26,'TRAINING FRIDAY':8,'NO SCHOOL / NO SCHEDULE':6,'COMPLETED':2}),types
assert sum('OPEN 11:30–1:30' in f.get('officeCoverage','') for f in data['fridays'])==8
for f in data['fridays']:
    d=f['date']; typ=f['type']; st=f.get('status',{})
    if d>='2026-09-04':
        text=json.dumps(f)
        assert 'Dorr' not in text and 'McKinley' not in text and 'Coach' not in text
    if d>='2026-09-04' and typ=='REGULAR FRIDAY':
        rot_work=[n for n in ROTATORS if st.get(n)=='Full Day 7:30–1:30']
        assert len(rot_work)==2,(d,rot_work)
    if d>='2026-09-04' and typ=='TRAINING FRIDAY':
        assert sum(v=='Full-Day Coverage — Misses Training' for v in st.values())==1
        assert sum(v=='Morning Coverage + Training' for v in st.values())==1
        assert sum(v=='Training 11:30–1:30' for v in st.values())==3
    for name,date in off:
        if d==date: assert st.get(name)=='OFF',(name,d,st.get(name))

# Ensure future regular rotating totals differ by at most one.
future_reg=Counter()
for f in data['fridays']:
    if f['date']>='2026-09-04' and f['type']=='REGULAR FRIDAY':
        for n in ROTATORS:
            if f['status'][n]=='Full Day 7:30–1:30': future_reg[n]+=1
assert max(future_reg.values())-min(future_reg.values())<=1,future_reg

new_json=json.dumps(data,separators=(',',':'),ensure_ascii=False)
s=s[:m.start(2)]+new_json+s[m.end(2):]

# Close planned-day-off collection and publish the live schedule views.
s=s.replace('<body class="request-only">','<body>',1)
s=s.replace('<section id="requests" aria-labelledby="reqHead">','<section id="requests" aria-labelledby="reqHead" hidden>',1)
s=s.replace('<h1>Friday Day-Off Requests</h1>','<h1>Friday Rotation Board</h1>',1)
s=s.replace('Friday availability · 2026–2027','Friday campus & staff rotation · 2026–2027',1)
p.write_text(s,encoding='utf-8')

print('LIVE SCHEDULE PUBLISHED')
print('Future regular rotating totals:',dict(future_reg))
print('Summary totals:',{x['name']:(x['total'],x['trainingsMissed']) for x in summary})
print('All founding inventory/training/open-office/hard-off checks passed.')
