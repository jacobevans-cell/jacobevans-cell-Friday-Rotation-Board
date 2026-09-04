from pathlib import Path

# Public page: add an Admin button next to theme toggle.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
if 'href="admin.html"' not in s:
    marker = '<button class="tool" id="themeBtn" type="button"'
    i = s.find(marker)
    if i < 0:
        raise SystemExit('theme button not found')
    # Insert before theme button so Admin is always visible beside it.
    s = s[:i] + '<a class="tool" href="admin.html" aria-label="Open admin controls">Admin</a>\n          ' + s[i:]
p.write_text(s, encoding='utf-8')

# Admin page: add add/edit controls and sign-out/back links.
p = Path('admin.html')
s = p.read_text(encoding='utf-8')

s = s.replace(
    '<button id="refresh" class="ghost" hidden>Refresh requests</button>',
    '<button id="refresh" class="ghost" hidden>Refresh requests</button>\n    <button id="signOut" class="ghost" hidden>Sign out</button>\n    <a href="index.html" style="margin-left:8px">Back to request page</a>',
    1
)

insert = '''\n  <section class="card" id="editCard" hidden>\n    <h2>Add or edit a day-off request</h2>\n    <p class="muted">Use this when you need to correct a staff member or date manually.</p>\n    <div class="summary" style="margin-top:12px">\n      <label>Staff<br><select id="editStaff"></select></label>\n      <label>Friday<br><input id="editDate" type="date"></label>\n    </div>\n    <div style="margin-top:12px">\n      <button id="saveEdit">Save request</button>\n      <button id="cancelEdit" class="ghost" hidden>Cancel edit</button>\n    </div>\n    <p id="editStatus" class="muted" style="margin-top:10px"></p>\n  </section>\n'''
if 'id="editCard"' not in s:
    s = s.replace('  <section class="card" id="summaryCard" hidden>', insert + '  <section class="card" id="summaryCard" hidden>', 1)

s = s.replace('<thead><tr><th>Friday</th><th>Staff</th><th></th></tr></thead>', '<thead><tr><th>Friday</th><th>Staff</th><th>Actions</th></tr></thead>', 1)
s = s.replace(
    "$('rows').innerHTML=requests.map(r=>`<tr><td>${esc(fmt(r.fridayDate))}</td><td><b>${esc(r.staffName)}</b></td><td><button class=\"ghost\" data-delete=\"${esc(r.id)}\">Remove</button></td></tr>`).join('');",
    "$('rows').innerHTML=requests.map(r=>`<tr><td>${esc(fmt(r.fridayDate))}</td><td><b>${esc(r.staffName)}</b></td><td><button class=\"ghost\" data-edit=\"${esc(r.id)}\" data-staff=\"${esc(r.staffName)}\" data-date=\"${esc(r.fridayDate)}\">Edit</button> <button class=\"ghost\" data-delete=\"${esc(r.id)}\">Remove</button></td></tr>`).join('');",
    1
)

anchor = "const esc=s=>String(s??'').replace(/[&<>\\\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\\"':'&quot;'}[c]));\n"
if 'let editingId=null;' not in s:
    js = '''let editingId=null;\nconst staffKey=n=>String(n).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');\nfunction fillEditor(){\n  $('editStaff').innerHTML=STAFF.map(n=>`<option>${esc(n)}</option>`).join('');\n  const d=new Date(); d.setDate(d.getDate()+((5-d.getDay()+7)%7||7));\n  $('editDate').value=d.toISOString().slice(0,10);\n}\nfillEditor();\n'''
    s = s.replace(anchor, anchor + js, 1)

s = s.replace("    $('tableCard').hidden=false;", "    $('tableCard').hidden=false;\n    $('editCard').hidden=false;\n    $('signOut').hidden=false;", 1)

old_handler = "$('rows').onclick=async e=>{const b=e.target.closest('[data-delete]');if(!b)return;if(!confirm('Remove this day-off request?'))return;b.disabled=true;try{await db.collection('fridayOffRequests').doc(b.dataset.delete).delete();await load();}catch(err){alert(err.message);b.disabled=false;}};"
new_handler = '''$('rows').onclick=async e=>{\n  const edit=e.target.closest('[data-edit]');\n  if(edit){editingId=edit.dataset.edit;$('editStaff').value=edit.dataset.staff;$('editDate').value=edit.dataset.date;$('cancelEdit').hidden=false;$('editStatus').textContent='Editing existing request.';$('editCard').scrollIntoView({behavior:'smooth'});return;}\n  const b=e.target.closest('[data-delete]');if(!b)return;if(!confirm('Remove this day-off request?'))return;b.disabled=true;try{await db.collection('fridayOffRequests').doc(b.dataset.delete).delete();await load();}catch(err){alert(err.message);b.disabled=false;}\n};\n$('saveEdit').onclick=async()=>{\n  const staff=$('editStaff').value,date=$('editDate').value;if(!staff||!date)return;\n  const key=staffKey(staff),newId=key+'__'+date;\n  $('saveEdit').disabled=true;$('editStatus').textContent='Saving…';\n  try{\n    await db.collection('fridayOffRequests').doc(newId).set({staffName:staff,staffKey:key,fridayDate:date,canSwap:true,submittedAt:firebase.firestore.FieldValue.serverTimestamp()});\n    if(editingId&&editingId!==newId)await db.collection('fridayOffRequests').doc(editingId).delete();\n    editingId=null;$('cancelEdit').hidden=true;$('editStatus').textContent='Saved ✓';await load();\n  }catch(err){$('editStatus').textContent=err.message||'Could not save.';}finally{$('saveEdit').disabled=false;}\n};\n$('cancelEdit').onclick=()=>{editingId=null;$('cancelEdit').hidden=true;$('editStatus').textContent='';};\n$('signOut').onclick=()=>auth.signOut();'''
if old_handler in s:
    s = s.replace(old_handler, new_handler, 1)

s = s.replace("if(!u){$('who').textContent='Not signed in.';$('who').className='muted';return;}", "if(!u){$('who').textContent='Not signed in.';$('who').className='muted';$('signIn').hidden=false;$('signOut').hidden=true;$('editCard').hidden=true;$('summaryCard').hidden=true;$('tableCard').hidden=true;return;}", 1)

p.write_text(s, encoding='utf-8')
print('Added public Admin button and admin add/edit/remove controls.')
