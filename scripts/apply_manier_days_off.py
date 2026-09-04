from pathlib import Path
import json,re
from collections import Counter
from datetime import datetime

p=Path('index.html')
s=p.read_text(encoding='utf-8')
m=re.search(r'(<script type="application/json" id="data">\s*)(\{.*?\})(\s*</script>)',s,re.S)
if not m: raise SystemExit('inline schedule data not found')
data=json.loads(m.group(2))

STAFF=['Lingam','Evans','Manier','Abby','Meda']
ROTATORS=['Lingam','Evans','Manier','Abby']
manier_off={'2026-09-04','2026-10-02','2026-11-06','2027-01-15','2027-02-12','2027-04-30'}
lingam_off={'2027-01-15'}

# Correct only the regular-Friday pairs needed to honor Manier's six hard days off,
# then compensate on two nearby dates so future regular rotation remains 13/13/12/12.
pair_overrides={
 '2026-10-02':('Abby','Evans'),
 '2026-10-16':('Manier','Lingam'),
 '2027-02-12':('Abby','Evans'),
 '2027-02-19':('Manier','Lingam'),
}

for f in data['fridays']:
    d=f['date']
    if f['type']!='REGULAR FRIDAY':
        continue
    if d in pair_overrides:
        f['morning1'],f['morning2']=pair_overrides[d]
    st={name:'OFF' for name in STAFF}
    for name in [f.get('morning1'),f.get('morning2')]:
        if name in STAFF:
            st[name]='Full Day 7:30–1:30'
    # Meda is standing Friday support unless unavailable. The previously mistaken Meda
    # day-off records are being removed, so these six dates should show Meda working.
    st['Meda']='Full Day 7:30–1:30'
    if d in manier_off:
        st['Manier']='OFF'
    if d in lingam_off:
        st['Lingam']='OFF'
    f['status']=st
    f['studentCoverage']='Assigned rotating teachers continue to 1:00'
    f['officeCoverage']='Jenny 7:30–11:30 | Cortni 9:30–1:30'
    f['training']='—'
    f['note']='Two rotating teachers provide Friday coverage. Meda is standing campus support when available. Student day ends at 1:00; assigned staff remain through 1:30.'

# Validate all hard days off are honored.
for f in data['fridays']:
    d=f['date']; st=f.get('status',{})
    if d in manier_off and f['type']=='REGULAR FRIDAY':
        assert st.get('Manier')=='OFF',(d,st.get('Manier'))
    if d in lingam_off and f['type']=='REGULAR FRIDAY':
        assert st.get('Lingam')=='OFF',(d,st.get('Lingam'))
    if d>='2026-09-04' and f['type']=='REGULAR FRIDAY':
        rot_work=[n for n in ROTATORS if st.get(n)=='Full Day 7:30–1:30']
        assert len(rot_work)==2,(d,rot_work)

# Rebuild summary from actual statuses.
working={'Full Day 7:30–1:30','Morning Coverage + Training','Training 11:30–1:30','Full-Day Coverage — Misses Training','On Campus (Completed)'}
summary=[]
for name in STAFF:
    month_counts={mo:0 for mo in data['months']}; total=missed=0
    for f in data['fridays']:
        st=f.get('status',{}).get(name,'OFF')
        if st in working:
            total+=1
            mo=datetime.strptime(f['date'],'%Y-%m-%d').strftime('%b %Y')
            if mo in month_counts: month_counts[mo]+=1
        if st=='Full-Day Coverage — Misses Training': missed+=1
    summary.append({'name':name,'months':month_counts,'total':total,'trainingsMissed':missed})
data['summary']=summary

future_reg=Counter()
for f in data['fridays']:
    if f['date']>='2026-09-04' and f['type']=='REGULAR FRIDAY':
        for n in ROTATORS:
            if f['status'].get(n)=='Full Day 7:30–1:30': future_reg[n]+=1
assert future_reg==Counter({'Evans':13,'Abby':13,'Lingam':12,'Manier':12}),future_reg

new_json=json.dumps(data,separators=(',',':'),ensure_ascii=False)
s=s[:m.start(2)]+new_json+s[m.end(2):]
p.write_text(s,encoding='utf-8')
print('MANIER DAYS OFF APPLIED')
print('Future regular totals:',dict(future_reg))
print('Summary totals:',{x['name']:x['total'] for x in summary})
