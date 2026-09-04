# Friday Rotation Board — Current Handoff

Updated September 4, 2026.

## Current purpose

The planned day-off collection phase is complete and the **live Friday schedule is now published**.

The public site shows the working Friday rotation. The old planned-day-off request form is hidden. Future unplanned absences are intended to be handled as **sick days** in the next update.

## Repository

`jacobevans-cell/jacobevans-cell-Friday-Rotation-Board`

Main public page: `index.html`

Admin page: `admin.html`

Firebase rules: `firestore.rules`

Firebase config: `firebase.json` + `.firebaserc`

## Founding source and invariants

The original Friday system was extracted from `Friday_School_Schedule_2026-2027.xlsm` and documented in the original Sports-Calendar handoff. The current live schedule must continue to preserve these founding requirements unless the user explicitly changes them:

- 42 Fridays total
- 26 regular Fridays
- 8 training Fridays
- 2 completed Fridays
- 6 no-school Fridays
- minimum two assigned teachers for student coverage
- training Friday structure with two morning-coverage teachers, one staying with Cortni through dismissal, and the other joining training at 11:30
- exactly one teacher missing each training because they stay with students
- the 11:30–1:30 office assignment remains OPEN on the 8 training Fridays for administration to assign
- office hours remain 7:30 a.m.–1:30 p.m.; student dismissal is 1:00 p.m.
- no future assignment for Dorr or McKinley

The current published schedule passed automated checks for all inventory counts, training structure, open-office count, and collected hard unavailability constraints before publication.

## Locked Friday staffing model

Active Friday pool:

- Lingam
- Evans
- Meda
- Abby
- Manier

`Manier` is the display name used for Latoya Manier in this system.

### Standing Friday support

Meda is treated as standing Friday campus support when available.

The two-person regular rotating coverage pool is:

- Abby
- Manier
- Evans
- Lingam

The live future regular workload is balanced at 13 / 13 / 12 / 12 assignments across those four rotating teachers.

### Fixed Teacher Clarity training Fridays

- September 18, 2026
- October 23, 2026
- November 13, 2026
- January 29, 2027
- February 26, 2027
- March 26, 2027
- April 23, 2027

Training Fridays remain a separate staffing problem from regular Fridays.

## Firebase architecture

Standalone Firebase project:

`friday-rotation-board`

Current system:

- Cloud Firestore collection `fridayOffRequests`
- public staff submissions require no sign-in when that form is enabled
- admin page uses Google sign-in
- no dependency on Dragonswood Firebase
- no Cloud Functions currently required for the live static schedule

Admin read/delete access is restricted to:

- `jacob.evans@explore.academy`
- `jacobicusjax@gmail.com`

## Admin page

`admin.html` now supports:

- Google admin sign-in
- viewing all recorded day-off requests
- conflict counts
- adding a request manually
- editing a request
- removing a request
- refreshing records
- signing out

## Live schedule generation rules

When the schedule is rebuilt, use Firestore records as hard unavailability constraints and preserve the founding invariants above.

Priority order:

1. Never schedule someone on a recorded unavailable date.
2. Maintain minimum student coverage.
3. Preserve valid training-Friday structure.
4. Preserve the 8 open training-day office shifts unless administration explicitly changes that rule.
5. Treat Meda as standing Friday support when available.
6. Build regular rotating coverage across Abby, Manier, Evans, and Lingam.
7. Keep rotating workload as even as possible.
8. Never assign Dorr or McKinley on future dates.
9. Flag impossible dates instead of inventing invalid coverage.

## NEXT LOCKED UPDATE — Sick-day auto-rebalance + teacher email

This is the next planned feature after the live schedule.

Once planned day-off collection is closed, any newly entered absence should be treated as a **sick day**.

Required future behavior:

1. Admin/staff records a sick day for a Friday.
2. The system compares that absence against the currently published assignment.
3. If the absent person is scheduled, the scheduler automatically computes the smallest valid re-balance that preserves all founding coverage/training constraints.
4. The system must not silently create one-person coverage or invalid training coverage.
5. The updated schedule is saved as the new live schedule.
6. A clear audit trail records what changed and why.
7. Teachers affected by the change receive an automatic email showing the changed Friday assignment.
8. If no valid automatic replacement exists, the system flags the date for admin action rather than fabricating coverage.

This later update will likely require a server-side Firebase trigger/function plus an authenticated email-sending path. Do not implement the email workflow by exposing credentials in browser code.

## Important implementation details to preserve

- Parse dates locally with `new Date(y, m-1, d)`, not `new Date('YYYY-MM-DD')`.
- Light/dark mode remains available.
- Calendar export must stay consistent with the live status data.
- Request/absence data itself is never stored only in localStorage.
- Any future automatic schedule adjustment must rerun the founding invariant checks before publication.
