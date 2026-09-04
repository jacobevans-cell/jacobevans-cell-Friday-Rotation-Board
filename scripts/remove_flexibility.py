from pathlib import Path

# Trigger patch after workflow exists.
# Public form
p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s
block = '''          <div class="req-field full">\n            <label>Flexibility</label>\n            <label class="req-check"><input type="checkbox" id="reqSwap" checked> I can work a different Friday instead if needed</label>\n          </div>\n'''
s = s.replace(block, '', 1)
s = s.replace('    return { staff: staff, friday: f, swap: $("reqSwap").checked };', '    return { staff: staff, friday: f, swap: true };', 1)
if s == original:
    raise SystemExit('index.html: expected flexibility UI/code not found')
p.write_text(s, encoding='utf-8')

# Admin view: remove obsolete Can swap column/pill
p = Path('admin.html')
s = p.read_text(encoding='utf-8')
original = s
s = s.replace('<thead><tr><th>Friday</th><th>Staff</th><th>Can swap?</th><th>Submitted by</th><th></th></tr></thead>', '<thead><tr><th>Friday</th><th>Staff</th><th>Submitted by</th><th></th></tr></thead>', 1)
s = s.replace('<td><span class="pill">${r.canSwap?\'Yes\':\'No\'}</span></td>', '', 1)
if s == original:
    raise SystemExit('admin.html: expected swap column not found')
p.write_text(s, encoding='utf-8')
print('Removed Friday request flexibility UI and admin column.')
