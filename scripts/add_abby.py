from pathlib import Path
import json, re

index = Path('index.html')
s = index.read_text(encoding='utf-8')

m = re.search(r'(<script type="application/json" id="data">\s*)(\{.*?\})(\s*</script>)', s, re.S)
if not m:
    raise SystemExit('inline schedule data not found')

data = json.loads(m.group(2))

staff = data.get('staff', [])
if 'Abby' not in staff:
    staff.append('Abby')
data['staff'] = staff

for f in data.get('fridays', []):
    status = f.setdefault('status', {})
    if 'Abby' not in status:
        status['Abby'] = 'CLOSED' if f.get('type') == 'NO SCHOOL / NO SCHEDULE' else 'OFF'

months = data.get('months', [])
summary = data.setdefault('summary', [])
if not any(r.get('name') == 'Abby' for r in summary):
    summary.append({
        'name': 'Abby',
        'months': {m: 0 for m in months},
        'total': 0,
        'trainingsMissed': 0
    })

# The old four-person totals are no longer the target after adding Abby.
data['summaryIntro'] = (
    'The active Friday scheduling pool is Lingam, Evans, Latoya, Meda, and Abby. '
    'The published rotation is temporarily hidden while availability is collected and the schedule is rebuilt.'
)
data['fairness'] = (
    'Fairness note: Abby is now part of the regular Friday rotation. The next generated schedule will rebalance '
    'Friday workdays across all five active staff after day-off requests are collected.'
)

for rule in data.get('rules', []):
    if rule.get('item') == 'Active Friday rotation':
        rule['rule'] = (
            'The active Friday rotation is Lingam, Evans, Latoya, Meda, and Abby. '
            'Dorr and McKinley are no longer assigned future Friday duty; August history remains visible only in the unpublished source schedule.'
        )

new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
s = s[:m.start(2)] + new_json + s[m.end(2):]
index.write_text(s, encoding='utf-8')

readme = Path('README.md')
if readme.exists():
    r = readme.read_text(encoding='utf-8')
    if '- Abby' not in r:
        r = r.replace('- Meda\n', '- Meda\n- Abby\n', 1)
    r = r.replace(
        'The current rotation is balanced at **22 Friday workdays per active staff member** and **2 missed trainings per active staff member**.',
        'The rotation is being rebuilt for five active staff after availability is collected. Abby is now part of the regular Friday scheduling pool.'
    )
    readme.write_text(r, encoding='utf-8')

handoff = Path('HANDOFF.md')
if handoff.exists():
    h = handoff.read_text(encoding='utf-8')
    h = h.replace('four active Friday-duty staff', 'five active Friday-duty staff')
    h = h.replace('Lingam, Evans, Latoya, and Meda', 'Lingam, Evans, Latoya, Meda, and Abby')
    if '**Abby added to regular rotation (Sep 4, 2026):**' not in h:
        marker = '**TEMPORARY PUBLIC MODE (Sep 4, 2026):**'
        note = ('**Abby added to regular rotation (Sep 4, 2026):** Abby is now part of the active Friday scheduling pool and should be treated like the other regular rotating teachers when the new schedule is generated.\n\n')
        pos = h.find(marker)
        if pos >= 0:
            h = h[:pos] + note + h[pos:]
        else:
            h = note + h
    handoff.write_text(h, encoding='utf-8')

# Verify the public request form will include Abby because it renders directly from data.staff.
check = index.read_text(encoding='utf-8')
assert '"staff":["Lingam","Evans","Latoya","Meda","Abby"]' in check
print('Abby added to active Friday staff pool.')
