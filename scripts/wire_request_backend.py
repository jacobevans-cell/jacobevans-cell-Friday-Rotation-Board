from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Switch the public page from callable Functions to direct Firestore on the
# standalone Friday Rotation Board Firebase project.
s = s.replace(
    'https://www.gstatic.com/firebasejs/12.1.0/firebase-functions-compat.js',
    'https://www.gstatic.com/firebasejs/12.1.0/firebase-firestore-compat.js'
)

start_marker = '  /* ---------- Friday-off requests ---------- */'
end_marker = '  /* ---------- filtering ---------- */'
start = s.index(start_marker)
end = s.index(end_marker, start)

new_block = r'''  /* ---------- Friday-off requests ---------- */
  var requestFirebaseConfig = {
    apiKey: "AIzaSyDYzp_yHSiOGp26FOyXC-8-9U5MBz-QC-0",
    authDomain: "friday-rotation-board.firebaseapp.com",
    projectId: "friday-rotation-board",
    storageBucket: "friday-rotation-board.firebasestorage.app",
    messagingSenderId: "558058912278",
    appId: "1:558058912278:web:921853261b4002ba52d337"
  };
  if (!firebase.apps.length) firebase.initializeApp(requestFirebaseConfig);
  var requestAuth = firebase.auth();
  var requestDb = firebase.firestore();
  var requestProvider = new firebase.auth.GoogleAuthProvider();
  var requestAdmins = ["jacob.evans@explore.academy", "jacobicusjax@gmail.com"];

  var requestRows = function () {
    return SCHOOL.filter(function (f) { return daysFrom(f.d) > 0; });
  };
  var requestRecord = function () {
    var staff = $("reqStaff").value;
    var iso = $("reqFriday").value;
    var f = D.fridays.filter(function (x) { return x.date === iso; })[0];
    return { staff: staff, friday: f, swap: $("reqSwap").checked };
  };
  var updateRequestStatus = function () {
    var el = $("reqStatus");
    el.classList.remove("req-ok", "req-error");
    el.textContent = "Submitting this request means you will not be scheduled on that Friday.";
  };
  var ensureRequestUser = async function () {
    var user = requestAuth.currentUser;
    if (!user) {
      var result = await requestAuth.signInWithPopup(requestProvider);
      user = result.user;
    }
    var email = String(user && user.email || "").toLowerCase();
    var allowed = /@explore[.]academy$/.test(email) || requestAdmins.indexOf(email) > -1;
    if (!allowed) {
      await requestAuth.signOut();
      throw new Error("Use your Explore Academy Google account.");
    }
    return user;
  };
  var submitFridayRequest = async function () {
    var r = requestRecord();
    if (!r.friday || !r.staff) return;
    var btn = $("submitRequest");
    var status = $("reqStatus");
    btn.disabled = true;
    status.classList.remove("req-ok", "req-error");
    status.textContent = "Saving request…";
    try {
      var user = await ensureRequestUser();
      var staffKey = String(r.staff).toLowerCase();
      var docId = staffKey + "__" + r.friday.date;
      await requestDb.collection("fridayOffRequests").doc(docId).set({
        staffName: r.staff,
        staffKey: staffKey,
        fridayDate: r.friday.date,
        canSwap: r.swap,
        submittedByEmail: String(user.email || "").toLowerCase(),
        submittedByUid: user.uid,
        submittedAt: firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: false });
      status.classList.add("req-ok");
      status.textContent = "Request saved ✓ " + r.staff + " is marked unavailable for Friday, " + fmtLong(r.friday.d) + ".";
    } catch (e) {
      status.classList.add("req-error");
      var msg = e && e.message ? e.message : "Could not save the request.";
      if (/permission/i.test(msg)) msg = "This request could not be saved. Make sure you are signed in with your Explore Academy account and that Friday request access is enabled.";
      status.textContent = msg;
    } finally {
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
    $("requestForm").addEventListener("submit", function (ev) { ev.preventDefault(); submitFridayRequest(); });
    updateRequestStatus();
  };
  var syncRequestStaff = function () {
    if (!$("reqStaff")) return;
    if (state.me && D.staff.indexOf(state.me) > -1) $("reqStaff").value = state.me;
    updateRequestStatus();
  };

'''

s = s[:start] + new_block + s[end:]

required = [
    'projectId: "friday-rotation-board"',
    'firebase.firestore()',
    'collection("fridayOffRequests")',
    'Request saved ✓',
    'firebase-firestore-compat.js'
]
for item in required:
    if item not in s:
        raise SystemExit(f'missing expected standalone Firebase marker: {item}')
if 'dragonswood-9289e' in s:
    raise SystemExit('old Dragonswood Firebase project still present in index.html')
if 'firebase-functions-compat.js' in s:
    raise SystemExit('old Firebase Functions client still present')

p.write_text(s, encoding='utf-8')
print('Public request page moved to standalone Firestore.')
