from pathlib import Path

p = Path('admin.html')
s = p.read_text(encoding='utf-8')

if 'let editingId=null;' not in s:
    marker = "const esc=s=>"
    start = s.find(marker)
    if start < 0:
        raise SystemExit('admin esc helper not found')
    end = s.find('\n', start)
    if end < 0:
        raise SystemExit('admin esc helper line end not found')
    js = '''\nlet editingId=null;\nconst staffKey=n=>String(n).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');\nfunction fillEditor(){\n  $('editStaff').innerHTML=STAFF.map(n=>`<option>${esc(n)}</option>`).join('');\n  const d=new Date(); d.setDate(d.getDate()+((5-d.getDay()+7)%7||7));\n  $('editDate').value=d.toISOString().slice(0,10);\n}\nfillEditor();'''
    s = s[:end] + js + s[end:]

required=['let editingId=null;','const staffKey=','fillEditor();','data-edit=','id="editCard"']
for item in required:
    if item not in s:
        raise SystemExit(f'missing admin editor piece: {item}')

p.write_text(s,encoding='utf-8')
print('Fixed Friday admin editor initialization.')
