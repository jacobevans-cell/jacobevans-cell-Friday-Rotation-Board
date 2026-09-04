const { onCall, HttpsError } = require('firebase-functions/v2/https');
const { initializeApp } = require('firebase-admin/app');
const { getFirestore, FieldValue } = require('firebase-admin/firestore');

initializeApp();

const db = getFirestore();
const REGION = 'us-central1';
const STAFF = ['Lingam', 'Evans', 'Latoya', 'Meda', 'Abby'];
const STAFF_KEYS = Object.fromEntries(STAFF.map((name) => [name, name.toLowerCase()]));
const ADMIN_EMAILS = new Set([
  'jacob.evans@explore.academy',
  'jacobicusjax@gmail.com'
]);

function emailOf(request) {
  return String(request.auth?.token?.email || '').toLowerCase().trim();
}

function requireSignedIn(request) {
  if (!request.auth) throw new HttpsError('unauthenticated', 'Sign in with Google first.');
  const email = emailOf(request);
  if (!email.endsWith('@explore.academy') && !ADMIN_EMAILS.has(email)) {
    throw new HttpsError('permission-denied', 'Use an Explore Academy account.');
  }
  return email;
}

function requireAdmin(request) {
  if (!request.auth) throw new HttpsError('unauthenticated', 'Sign in first.');
  const email = emailOf(request);
  if (!ADMIN_EMAILS.has(email)) {
    throw new HttpsError('permission-denied', 'Admin access required.');
  }
  return email;
}

function validDate(value) {
  return /^2026-\d{2}-\d{2}$/.test(value) || /^2027-\d{2}-\d{2}$/.test(value);
}

exports.submitFridayOffRequest = onCall({ region: REGION }, async (request) => {
  const email = requireSignedIn(request);
  const data = request.data || {};
  const staffName = String(data.staffName || '').trim();
  const fridayDate = String(data.fridayDate || '').trim();
  const canSwap = Boolean(data.canSwap);

  if (!STAFF.includes(staffName)) {
    throw new HttpsError('invalid-argument', 'Unknown staff member.');
  }
  if (!validDate(fridayDate)) {
    throw new HttpsError('invalid-argument', 'Invalid Friday date.');
  }

  const staffKey = STAFF_KEYS[staffName];
  const docId = `${staffKey}__${fridayDate}`;
  const ref = db.collection('fridayOffRequests').doc(docId);
  const existing = await ref.get();

  const payload = {
    staffName,
    staffKey,
    fridayDate,
    canSwap,
    submittedByEmail: email,
    submittedByUid: request.auth.uid,
    updatedAt: FieldValue.serverTimestamp()
  };
  if (!existing.exists) payload.createdAt = FieldValue.serverTimestamp();

  await ref.set(payload, { merge: true });

  return {
    ok: true,
    id: docId,
    staffName,
    fridayDate,
    canSwap
  };
});

exports.listFridayOffRequests = onCall({ region: REGION }, async (request) => {
  requireAdmin(request);
  const snap = await db.collection('fridayOffRequests').orderBy('fridayDate').get();
  const requests = snap.docs.map((doc) => {
    const data = doc.data();
    return {
      id: doc.id,
      staffName: data.staffName,
      staffKey: data.staffKey,
      fridayDate: data.fridayDate,
      canSwap: Boolean(data.canSwap),
      submittedByEmail: data.submittedByEmail || '',
      createdAt: data.createdAt?.toDate ? data.createdAt.toDate().toISOString() : null,
      updatedAt: data.updatedAt?.toDate ? data.updatedAt.toDate().toISOString() : null
    };
  });
  return { ok: true, requests };
});

exports.deleteFridayOffRequest = onCall({ region: REGION }, async (request) => {
  requireAdmin(request);
  const id = String(request.data?.id || '').trim();
  if (!/^[a-z]+__20\d{2}-\d{2}-\d{2}$/.test(id)) {
    throw new HttpsError('invalid-argument', 'Invalid request id.');
  }
  await db.collection('fridayOffRequests').doc(id).delete();
  return { ok: true, id };
});
