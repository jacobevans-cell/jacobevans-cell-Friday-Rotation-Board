# Deploy the Friday Request Backend

The public GitHub Pages form and `admin.html` are already wired to Firebase project `dragonswood-9289e`.

From a computer with Firebase CLI access, run from the root of this repository:

```bash
firebase login
firebase deploy --only functions:friday-scheduler --project dragonswood-9289e
```

This deploys only the dedicated `friday-scheduler` functions codebase. It does **not** deploy or replace Dragonswood's other Functions, Hosting, or Firestore rules.

After deployment:

- Staff submit requests on the main GitHub Pages site.
- Each saved request gets a green `Request saved ✓` confirmation.
- Requests are stored centrally in Firestore collection `fridayOffRequests`.
- Admin view: `https://jacobevans-cell.github.io/jacobevans-cell-Friday-Rotation-Board/admin.html`
- Admin sign-in is allowed for `jacob.evans@explore.academy` and `jacobicusjax@gmail.com`.
- The admin page groups requests by Friday and flags a coverage conflict when fewer than two of the five active staff remain available.

A submitted request is automatically treated as approved/unavailable. There is no pending/approval state.
