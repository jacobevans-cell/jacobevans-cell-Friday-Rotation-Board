from pathlib import Path
import json,re
from datetime import datetime

p=Path('index.html')
s=p.read_text(encoding='utf-8')
m=re.search(r'(<script type="application/json" id="data">\s*)(\{.*?\})(\s*</script>)',s,re.S)
if not m:
    raise SystemExit('inline schedule data not found')
data=json.loads(m.group(2))

STAFF=['Lingam','Evans','Manier','Abby','Meda']
ABSENT={
    '2027-04-23': {'Evans','Abby'},
    '2027-05-07': {'Evans','Abby'},
}

# Least-disruptive reflow. May 7 already had Evans/Abby off, so no assignment change there.
for f in data['fridays']:
    d=f['date']
    if d=='2027-04-23':
        assert f['type']=='TRAINING FRIDAY'
        f['morning1']='Lingam'
        f['morning2']='Manier'
        f['studentCoverage']='Cortni + Lingam 11:30–1:00'
        f['officeCoverage']='Jenny 7:30–11:30 | OPEN 11:30–1:30 (Admin to assign)'
        f['training']='Manier, Meda 11:30–1:30'
        f['note']='Evans and Abby are unavailable for travel. Lingam stays with Cortni and misses training. Manier covers the morning and joins training at 11:30. Meda attends training. Office coverage remains open for administration to assign.'
        f['status']={
            'Lingam':'Full-Day Coverage — Misses Training',
            'Evans':'OFF',
            'Manier':'Morning Coverage + Training',
            'Abby':'OFF',
            'Meda':'Training 11:30–1:30',
        }
    if d=='2027-05-07':
        assert f['type']=='REGULAR FRIDAY'
        f['status']['Evans']='OFF'
        f['status']['Abby']='OFF'

for f in data['fridays']:
    d=f['date']; st=f.get('status',{})
    if d in ABSENT:
        for name in ABSENT[d]:
            assert st.get(name)=='OFF',(d,name,st.get(name))
    if d>='2026-09-04' and f['type']=='REGULAR FRIDAY':
        rot=[n for n in ['Lingam','Evans','Manier','Abby'] if st.get(n)=='Full Day 7:30–1:30']
        assert len(rot)==2,(d,rot)
    if d>='2026-09-04' and f['type']=='TRAINING FRIDAY':
        morning=[n for n in STAFF if st.get(n) in ('Full-Day Coverage — Misses Training','Morning Coverage + Training')]
        stay=[n for n in STAFF if st.get(n)=='Full-Day Coverage — Misses Training']
        join=[n for n in STAFF if st.get(n)=='Morning Coverage + Training']
        assert len(morning)==2,(d,morning)
        assert len(stay)==1,(d,stay)
        assert len(join)==1,(d,join)

working={'Full Day 7:30–1:30','Morning Coverage + Training','Training 11:30–1:30','Full-Day Coverage — Misses Training','On Campus (Completed)'}
summary=[]
for name in STAFF:
    month_counts={mo:0 for mo in data['months']}; total=missed=0
    for f in data['fridays']:
        status=f.get('status',{}).get(name,'OFF')
        if status in working:
            total+=1
            mo=datetime.strptime(f['date'],'%Y-%m-%d').strftime('%b %Y')
            if mo in month_counts: month_counts[mo]+=1
        if status=='Full-Day Coverage — Misses Training': missed+=1
    summary.append({'name':name,'months':month_counts,'total':total,'trainingsMissed':missed})
data['summary']=summary

regular={n:0 for n in ['Lingam','Evans','Manier','Abby']}
for f in data['fridays']:
    if f['date']>='2026-09-04' and f['type']=='REGULAR FRIDAY':
        for n in regular:
            if f['status'].get(n)=='Full Day 7:30–1:30': regular[n]+=1
assert regular=={'Lingam':12,'Evans':13,'Manier':12,'Abby':13},regular

new_json=json.dumps(data,separators=(',',':'),ensure_ascii=False)
s=s[:m.start(2)]+new_json+s[m.end(2):]
p.write_text(s,encoding='utf-8')
print('VEGAS ABSENCES REFLOWED')
print('Apr 23:', next(f['status'] for f in data['fridays'] if f['date']=='2027-04-23'))
print('May 7:', next(f['status'] for f in data['fridays'] if f['date']=='2027-05-07'))
print('Regular totals:', regular)
print('Summary totals:', {x['name']:x['total'] for x in summary})
print('Trainings missed:', {x['name']:x['trainingsMissed'] for x in summary})

# one-time trigger 2026-09-04
