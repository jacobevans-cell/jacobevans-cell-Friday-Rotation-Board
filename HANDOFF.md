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

## Locked Friday staffing model

Active Friday pool:

- Lingam
- Evans
- Meda
- Abby
- Manier

Latoya is no longer part of the active future Friday pool. Dorr and McKinley also must not receive future Friday assignments. Historical records may still contain former staff and should not be rewritten merely for appearance.

### Standing Friday support

Meda is treated as a standing Friday presence / campus support person. The regular rotating coverage pool is primarily:

- Abby
- Manier
- Evans
- Lingam

Meda may still submit a Friday-off request; any such request is a hard unavailability constraint.

### Fixed Teacher Clarity training Fridays

The following dates are locked as Teacher Clarity training Fridays based on the September 4 staffing chat:

- September 18, 2026
- October 23, 2026
- November 13, 2026
- January 29, 2027
- February 26, 2027
- March 26, 2027
- April 23, 2027

Training Fridays must be scheduled separately from normal Friday rotation logic. The staffing chat specifically indicates short-staffing may require only Meda and Lingam to attend some trainings while remaining staff cover students. Do not assume that pattern automatically; treat it as a scheduling option when solving the final calendar.

## Firebase architecture

The Friday system is standalone and uses Firebase project:

`friday-rotation-board`

It does **not** use Dragonswood Firebase.

The system uses:

- public no-login staff submission
- Cloud Firestore
- collection: `fridayOffRequests`
- Google sign-in only for the protected admin page
- no Cloud Functions

## Request document model

One deterministic document per staff/date:

`{staffKey}__{YYYY-MM-DD}`

Example:

`evans__2026-09-11`

Current stored fields:

```text
staffName
staffKey
fridayDate
canSwap
submittedAt
```

`canSwap` is retained internally for compatibility but is no longer exposed as a staff choice. Operationally every request simply means the person is unavailable that Friday.

Submitting the same staff/date again overwrites the same record rather than creating a duplicate.

## Security model

Firestore rules are the authority.

Public staff submission:

- no sign-in required
- staff name/key must be one of the five active staff
- document ID must match staff/date
- request data is not publicly readable

Admin read/delete access is restricted to:

- `jacob.evans@explore.academy`
- `jacobicusjax@gmail.com`

## Public request behavior

Staff choose only:

1. staff member
2. Friday requested off

On submit:

1. Firestore saves the request.
2. The status box changes to green with `Request saved ✓` and the selected Friday.

There is no flexibility checkbox and no staff sign-in.

## Admin page

`admin.html` reads Firestore directly after admin Google sign-in.

It shows:

- total requests
- number of Fridays affected
- individual staff/date requests
- how many active staff remain available on each affected Friday
- coverage conflict warnings when fewer than two active staff remain available
- remove-request control

## Schedule generation rules

The old embedded draft schedule is not final truth. A new schedule will be generated after day-off requests are collected.

When generating the new schedule, treat Firestore request records as hard unavailability constraints.

Priorities:

1. Never schedule someone on a requested-off Friday.
2. Use the locked active staff pool: Lingam, Evans, Meda, Abby, Manier.
3. Treat Meda as standing Friday support unless she has requested that Friday off.
4. Build regular rotating coverage primarily across Abby, Manier, Evans, and Lingam.
5. Never assign Latoya, Dorr, or McKinley on future dates.
6. Preserve the seven locked Teacher Clarity training dates.
7. Maintain required student coverage.
8. Handle training Fridays separately from regular Fridays.
9. Balance regular rotating workload as evenly as possible after hard constraints.
10. Flag impossible dates instead of inventing invalid coverage.

Nothing should become publicly visible as a schedule until the generated rotation is reviewed and deliberately published.

## Important implementation details to preserve

- Dates are parsed as local dates using `new Date(y, m-1, d)` rather than `new Date('YYYY-MM-DD')`.
- Request-only mode hides the old draft roster, workload, training labels, and calendar views.
- Light/dark mode remains available on the public request page.
- The theme choice is saved locally on each device.
- Request data itself is never stored in localStorage.
- Old draft schedule data may remain embedded for later regeneration, but it must not be treated as current published truth.
