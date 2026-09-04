# Friday Rotation Board

> **Public mode right now:** request days off only. The rotation/schedule is intentionally hidden until availability is collected and a real schedule is generated.

Standalone 2026–2027 Friday campus and staff rotation system for Explore Academy.

## Locked Friday staffing model

Active Friday pool:

- Lingam
- Evans
- Meda
- Abby
- Manier

Meda is treated as a standing Friday presence / campus support person. Regular rotating coverage is built primarily around Abby, Manier, Evans, and Lingam, while still honoring any day-off request Meda submits.

Latoya is no longer in the active future Friday rotation pool. Dorr and McKinley are also not assigned future Friday duty. Historical August records may remain in the hidden draft data.

Fixed Teacher Clarity training Fridays from the September 4 staffing chat:

- September 18, 2026
- October 23, 2026
- November 13, 2026
- January 29, 2027
- February 26, 2027
- March 26, 2027
- April 23, 2027

Training Fridays are handled as a separate staffing problem from regular Fridays. Final assignments remain unpublished until day-off requests are collected.

## Current backend

The Friday system uses its own Firebase project:

`friday-rotation-board`

- Public staff requests require no sign-in
- Cloud Firestore collection `fridayOffRequests`
- Admin page remains protected with Google sign-in
- No Cloud Functions required
- No dependency on Dragonswood Firebase

## What the board includes

- Friday day-off request form
- Automatic approval: submitted request = unavailable that Friday
- Central request storage
- Admin request dashboard and conflict warnings
- Hidden draft rotation data for future regeneration
- Coverage grid / workload / calendar tooling to be republished after the real schedule is generated

Public page: `index.html`

Admin page: `admin.html`

`HANDOFF.md` contains the current implementation and scheduling rules.
