from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s

# Public request form no longer needs Firebase Auth SDK.
s = s.replace('<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-auth-compat.js"></script>\n', '', 1)

s = s.replace(
    '<p class="req-small">Requests save directly to the Friday scheduling system. Google sign-in identifies the submission.</p>',
    '<p class="req-small">Requests save directly to the Friday scheduling system. No sign-in is required.</p>',
    1
)

# Remove auth/provider setup from request section.
s = s.replace('  var requestAuth = firebase.auth();\n', '', 1)
s = s.replace('  var requestProvider = new firebase.auth.GoogleAuthProvider();\n', '', 1)
s = s.replace('  var requestAdmins = ["jacob.evans@explore.academy", "jacobicusjax@gmail.com"];\n', '', 1)

start_marker = '  var ensureRequestUser = async function () {'
end_marker = '  var submitFridayRequest = async function () {'
if start_marker in s:
    start = s.index(start_marker)
    end = s.index(end_marker, start)
    s = s[:start] + s[end:]

s = s.replace('      var user = await ensureRequestUser();\n', '', 1)
s = s.replace('        submittedByEmail: String(user.email || "").toLowerCase(),\n        submittedByUid: user.uid,\n', '', 1)

# Keep only Firestore in the public request flow.
if 'firebase-firestore-compat.js' not in s:
    auth_anchor = '<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-app-compat.js"></script>\n'
    s = s.replace(auth_anchor, auth_anchor + '<script src="https://www.gstatic.com/firebasejs/12.1.0/firebase-firestore-compat.js"></script>\n', 1)

# Make permission errors useful without mentioning login.
s = s.replace(
    'if (/permission/i.test(msg)) msg = "This request could not be saved. Make sure you are signed in with your Explore Academy account and that Friday request access is enabled.";',
    'if (/permission/i.test(msg)) msg = "This request could not be saved yet. Friday request access is still being connected.";',
    1
)

required = [
    'No sign-in is required.',
    'var requestDb = firebase.firestore();',
    'submittedAt: firebase.firestore.FieldValue.serverTimestamp()',
    'Request saved ✓'
]
for item in required:
    if item not in s:
        raise SystemExit(f'missing expected no-login request code: {item}')

for forbidden in [
    'var requestAuth = firebase.auth();',
    'ensureRequestUser',
    'submittedByEmail:',
    'submittedByUid:',
    'Google sign-in identifies the submission.'
]:
    if forbidden in s:
        raise SystemExit(f'login code still present: {forbidden}')

if s != original:
    p.write_text(s, encoding='utf-8')
    print('Removed staff sign-in from Friday requests.')
else:
    print('No changes needed.')
