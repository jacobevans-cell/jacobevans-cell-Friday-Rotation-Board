# Friday Rotation Board

> **Public mode right now:** request days off only. The rotation/schedule is intentionally hidden until availability is collected and a real schedule is generated.

Standalone 2026–2027 Friday campus and staff rotation system for Explore Academy.

## Current active Friday staff

- Lingam
- Evans
- Latoya
- Meda
- Abby

Dorr and McKinley are no longer assigned future Friday duty. Their August assignments remain in the board only as historical records.

## Current backend

The Friday system uses its own Firebase project:

`friday-rotation-board`

- Firebase Authentication for Google sign-in
- Cloud Firestore collection `fridayOffRequests`
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
