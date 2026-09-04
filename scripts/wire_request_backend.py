from pathlib import Path

# Triggered after the workflow is present so the frontend patch runs.
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add visible success/error/disabled states.
css='''\n/* central request submission states */\n.req-status.req-ok{background:var(--s-work-bg);border-left-color:var(--s-work-fg);color:var(--s-work-fg)}\n.req-status.req-error{background:#FCE9E7;border-left-color:#A63D35;color:#7D2924}\n:root[data-theme="dark"] .req-status.req-error{background:#351B1A;color:#FFB7AF}\n.btn:disabled{opacity:.48;cursor:not-allowed;filter:grayscale(.25)}\n'''
if 'central request submission states' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Load Firebase client libraries before the application code.
marker='<script type="application/json" id="data">'
libs='''<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-app-compat.js"></script>\n<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-auth-compat.js"></script>\n<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-functions-compat.js"></script>\n\n'''
if 'firebase-functions-compat.js' not in s:
    s=s.replace(marker,libs+marker,1)

s=s.replace('<button class="btn" type="submit" id="submitRequest" disabled>Submit request</button>',
            '<button class="btn" type="submit" id="submitRequest">Submit request</button>',1)
s=s.replace('Central request storage is being connected. The submit button will enable once requests can be saved safely.',
            'Requests save directly to the Friday scheduling system. Google sign-in identifies the submission.',1)

start=s.index('  /* ---------- Friday-off requests ---------- */')
end=s.index('  /* ---------- filtering ---------- */',start)
new_block=r'''  /* ---------- Friday-off requests ---------- */
  var requestFirebaseConfig = {
    apiKey: "AIzaSyC918WJoGQgxRKsqcz-3bXI7iZWv_1bwYE",
    authDomain: "dragonswood-9289e.firebaseapp.com",
    projectId: "dragonswood-9289e",
    storageBucket: "dragonswood-9289e.firebasestorage.app",
    messagingSenderId: "1064477064695",
    appId: "1:1064477064695:web:283e1016ee2303d39042f2",
    measurementId: "G-LPRLDGVBD2"
  };
  if (!firebase.apps.length) firebase.initializeApp(requestFirebaseConfig);
  var requestAuth = firebase.auth();
  var requestFunctions = firebase.app().functions("us-central1");

  var requestRows = function () {
    return SCHOOL.filter(function (f) { return daysFrom(f.d) > 0; });
  };
  var requestRecord = function () {
    var staff = $("reqStaff").value;
    var iso = $("reqFriday").value;
    var f = D.fridays.filter(function (x) { return x.date === iso; })[0];
    return { staff: staff, friday: f, swap: $("reqSwap").checked };
  };
  var setRequestMessage = function (text, kind) {
    var box = $("reqStatus");
    box.textContent = text;
    box.classList.remove("req-ok", "req-error");
    if (kind === "ok") box.classList.add("req-ok");
    if (kind === "error") box.classList.add("req-error");
  };
  var updateRequestStatus = function () {
    setRequestMessage("This is an availability request only. No Friday assignments are currently published.", "");
  };
  var ensureRequestUser = async function () {
    var user = requestAuth.currentUser;
    if (!user) {
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.setCustomParameters({ hd: "explore.academy", prompt: "select_account" });
      var result = await requestAuth.signInWithPopup(provider);
      user = result.user;
    }
    var email = String(user.email || "").toLowerCase();
    if (!email.endsWith("@explore.academy") && email !== "jacobicusjax@gmail.com") {
      await requestAuth.signOut();
      throw new Error("Use your Explore Academy Google account.");
    }
    return user;
  };
  var submitRequest = async function () {
    var r = requestRecord();
    if (!r.friday || !r.staff) return;
    var btn = $("submitRequest");
    btn.disabled = true;
    btn.textContent = "Saving…";
    setRequestMessage("Signing in and saving your request…", "");
    try {
      await ensureRequestUser();
      var call = requestFunctions.httpsCallable("submitFridayOffRequest");
      await call({ staffName: r.staff, fridayDate: r.friday.date, canSwap: r.swap });
      var msg = "Request saved ✓ " + r.staff + " is marked unavailable for Friday, " + fmtLong(r.friday.d) + ".";
      setRequestMessage(msg, "ok");
      toast("Friday-off request saved.");
      btn.textContent = "Saved ✓";
      setTimeout(function () { btn.textContent = "Submit request"; btn.disabled = false; }, 1800);
    } catch (err) {
      var message = String(err && err.message || "Could not save the request.");
      if (/not-found/i.test(message)) message = "The request service is not deployed yet. No request was saved.";
      setRequestMessage(message, "error");
      btn.textContent = "Try again";
      btn.disabled = false;
    }
  };
  var renderRequestForm = function () {
    $("reqStaff").innerHTML = D.staff.map(function (n) { return '<option value="' + esc(n) + '">' + esc(n) + "</option>"; }).join("");
    var rr = requestRows();
    $("reqFriday").innerHTML = rr.map(function (f) {
      return '<option value="' + f.date + '">' + esc(fmtLong(f.d)) + "</option>";
    }).join("");
    if (state.me && D.staff.indexOf(state.me) > -1) $("reqStaff").value = state.me;
    $("reqStaff").addEventListener("change", updateRequestStatus);
    $("reqFriday").addEventListener("change", updateRequestStatus);
    $("requestForm").addEventListener("submit", function (ev) { ev.preventDefault(); submitRequest(); });
    updateRequestStatus();
  };
  var syncRequestStaff = function () {
    if (!$("reqStaff")) return;
    if (state.me && D.staff.indexOf(state.me) > -1) $("reqStaff").value = state.me;
    updateRequestStatus();
  };

'''
s=s[:start]+new_block+s[end:]

required=[
  'httpsCallable("submitFridayOffRequest")',
  'Request saved ✓',
  'id="submitRequest">Submit request</button>',
  'firebase-functions-compat.js',
  'req-status.req-ok'
]
for item in required:
    if item not in s:
        raise SystemExit('missing '+item)

p.write_text(s,encoding='utf-8')
print('Friday request frontend wired to Firebase Functions.')
