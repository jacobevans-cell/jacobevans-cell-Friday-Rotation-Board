# Friday Rotation Board — Current Handoff

Updated September 4, 2026.

## Current purpose

The public site is intentionally in **request-only mode**. Staff should only see the Friday day-off request form until availability has been collected and a real rotation is generated.

A submitted request is automatically approved and means:

> Do not schedule that staff member on that Friday.

There is no pending / approval / denial state.

## Repository

`jacobevans-cell/jacobevans-cell-Friday-Rotation-Board`

Main public page: `index.html`

Admin page: `admin.html`

Firebase rules: `firestore.rules`

Firebase config: `firebase.json` + `.firebaserc`

## Active Friday staff

- Lingam
- Evans
- Latoya
- Meda
- Abby

Former staff who must not receive future assignments:

- Dorr
- McKinley

Historical August records may still contain former staff and should not be rewritten merely for appearance.

## Firebase architecture

The Friday system is standalone and uses Firebase project:

`friday-rotation-board`

It does **not** use Dragonswood Firebase.

Web configuration:

- authDomain: `friday-rotation-board.firebaseapp.com`
- projectId: `friday-rotation-board`
- storageBucket: `friday-rotation-board.firebasestorage.app`
- messagingSenderId: `558058912278`
- appId: `1:558058912278:web:921853261b4002ba52d337`

The public Firebase API key is embedded in the web app as normal Firebase web configuration. No service-account private key belongs in the repository.

The system uses:

- Firebase Authentication → Google sign-in
- Cloud Firestore
- collection: `fridayOffRequests`
- no Cloud Functions

## Request document model

One deterministic document per staff/date:

`{staffKey}__{YYYY-MM-DD}`

Example:

`evans__2026-09-11`

Fields:

```text
staffName
staffKey
fridayDate
canSwap
submittedByEmail
submittedByUid
submittedAt
```

Submitting the same staff/date again overwrites the same record rather than creating a duplicate.

## Security model

Firestore rules are the authority.

Staff submission:

- must be signed in
- must use an `@explore.academy` account, except explicit admin accounts
- staff name/key must be one of the five active staff
- document ID must match staff/date
- submitter email and UID must match Firebase Auth

Admin read/delete access is restricted to:

- `jacob.evans@explore.academy`
- `jacobicusjax@gmail.com`

Other users cannot list all requests.

## Public request behavior

Staff choose:

1. staff member
2. Friday requested off
3. whether they can work another Friday instead

On submit:

1. Google sign-in occurs if needed.
2. Firestore saves the request.
3. The status box changes to green with `Request saved ✓` and the selected Friday.

If saving fails, the status box shows an error instead of pretending success.

## Admin page

`admin.html` reads Firestore directly after admin Google sign-in.

It shows:

- total requests
- number of Fridays affected
- all individual requests
- who submitted each request
- whether each person can swap
- how many active staff remain available on each affected Friday
- coverage conflict warnings when fewer than two of the five active staff remain available
- remove-request control

## One-time Firebase console requirements

Before real submissions can succeed:

1. Create Firestore Database in project `friday-rotation-board`.
2. Enable Authentication → Google.
3. Add `jacobevans-cell.github.io` to Authentication authorized domains.
4. Publish the repository's `firestore.rules`.

Rules-only Firebase CLI deployment:

```bash
firebase deploy --only firestore:rules --project friday-rotation-board
```

## Schedule generation rules

The old four-person 22/22/22/22 draft is obsolete as a final schedule because Abby is now a fifth rotating teacher and real day-off requests have not yet been incorporated.

When generating the new schedule, treat Firestore request records as hard unavailability constraints.

Priorities:

1. Never schedule someone on a requested-off Friday.
2. Never assign Dorr or McKinley on future dates.
3. Maintain required student coverage.
4. Preserve valid training-Friday structure.
5. Balance total Friday workload across the five active staff as evenly as possible.
6. Balance missed-training / stay-back assignments as evenly as possible.
7. Use `canSwap` when choosing compensating Fridays.
8. Flag impossible dates instead of inventing invalid coverage.

Nothing should become publicly visible as a schedule until the generated rotation is reviewed and deliberately published.

## Important implementation details to preserve

- Dates are parsed as local dates using `new Date(y, m-1, d)` rather than `new Date('YYYY-MM-DD')`.
- Request-only mode hides the old draft roster, workload, training labels, and calendar views.
- Light/dark mode remains available on the public request page.
- The theme choice is saved locally on each device.
- Request data itself is never stored in localStorage.
- Old draft schedule data may remain embedded for later regeneration, but it must not be treated as current published truth.
