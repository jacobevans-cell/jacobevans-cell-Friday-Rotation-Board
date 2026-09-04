# Trigger workflow after creation.
from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''  var renderCards = function (rows) {\n    var groups = [], seen = {};\n    rows.forEach(function (f) {\n      if (!seen[f.mk]) { seen[f.mk] = { key: f.mk, name: monthName(f.d), items: [] }; groups.push(seen[f.mk]); }\n      seen[f.mk].items.push(f);\n    });\n    $("cardsView").innerHTML = groups.map(function (g) {\n      return '<div class="monthgrp"><h3>' + esc(g.name) + ' <span class="mono" style="letter-spacing:0">'\n        + g.items.length + "</span></h3>"\n        + '<div class="cards">' + g.items.map(cardHtml).join("") + "</div></div>";\n    }).join("");\n  };'''
new='''  var renderCards = function (rows) {\n    var groupedHtml = function (items) {\n      var groups = [], seen = {};\n      items.forEach(function (f) {\n        if (!seen[f.mk]) { seen[f.mk] = { key: f.mk, name: monthName(f.d), items: [] }; groups.push(seen[f.mk]); }\n        seen[f.mk].items.push(f);\n      });\n      return groups.map(function (g) {\n        return '<div class="monthgrp"><h3>' + esc(g.name) + ' <span class="mono" style="letter-spacing:0">'\n          + g.items.length + "</span></h3>"\n          + '<div class="cards">' + g.items.map(cardHtml).join("") + "</div></div>";\n      }).join("");\n    };\n\n    var current = rows.filter(function (f) { return daysFrom(f.d) >= 0; });\n    var past = rows.filter(function (f) { return daysFrom(f.d) < 0; });\n    var html = groupedHtml(current);\n    if (past.length) {\n      html += '<details class="past-days"><summary><span>Past Days</span><span class="mono">' + past.length + '</span></summary>'\n        + '<div class="past-days-body">' + groupedHtml(past) + '</div></details>';\n    }\n    $("cardsView").innerHTML = html;\n  };'''
if old not in s:
    raise SystemExit('renderCards block not found')
s=s.replace(old,new,1)

css_marker='''/* ============================ GRID VIEW ============================ */'''
css='''.past-days{margin-top:1.5rem;border:1px solid var(--rule);border-radius:8px;background:var(--card);box-shadow:var(--shadow);overflow:hidden}\n.past-days summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1rem 1.15rem;font-family:'Archivo',sans-serif;font-weight:700;color:var(--ink);background:var(--card-2)}\n.past-days summary::-webkit-details-marker{display:none}\n.past-days summary::before{content:'▸';color:var(--brass-2);margin-right:.35rem}\n.past-days[open] summary::before{content:'▾'}\n.past-days summary span:first-of-type{flex:1}\n.past-days-body{padding:1rem}\n.past-days-body .monthgrp:first-child{margin-top:0}\n\n'''
if '.past-days{' not in s:
    if css_marker not in s: raise SystemExit('CSS marker not found')
    s=s.replace(css_marker,css+css_marker,1)

p.write_text(s,encoding='utf-8')
print('Past cards now collapse under Past Days by default.')
