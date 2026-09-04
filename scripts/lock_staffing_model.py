from pathlib import Path

# Public page: replace active request staff pool only. Leave hidden draft assignments untouched.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old='"staff":["Lingam","Evans","Latoya","Meda","Abby"]'
new='"staff":["Lingam","Evans","Meda","Abby","Manier"]'
if old not in s:
    raise SystemExit('index staff pool not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Admin conflict calculations use same active pool.
p = Path('admin.html')
s = p.read_text(encoding='utf-8')
old="const STAFF=['Lingam','Evans','Latoya','Meda','Abby'];"
new="const STAFF=['Lingam','Evans','Meda','Abby','Manier'];"
if old not in s:
    raise SystemExit('admin staff pool not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

print('Locked Friday active staff pool: Lingam, Evans, Meda, Abby, Manier.')
