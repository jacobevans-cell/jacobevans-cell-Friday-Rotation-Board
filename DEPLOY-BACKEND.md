# Friday Rotation Board — Firebase Setup

This project now uses its own Firebase project:

`friday-rotation-board`

It does **not** use Dragonswood Firebase.

## Architecture

- GitHub Pages hosts `index.html` and `admin.html`.
- Firebase Authentication handles Google sign-in.
- Cloud Firestore stores `fridayOffRequests`.
- No Cloud Functions are required.
- A submitted request is automatically treated as an approved day off.

## One-time Firebase Console setup

1. In Firebase project `friday-rotation-board`, create a Firestore database in Production mode.
2. Authentication → Sign-in method → enable Google.
3. Authentication → Settings → Authorized domains → add `jacobevans-cell.github.io`.
4. Publish the repository's `firestore.rules`.

From Firebase CLI, the rules-only deploy is:

```bash
firebase login
firebase deploy --only firestore:rules --project friday-rotation-board
```

The repository's `.firebaserc` already points to `friday-rotation-board`, so from the repo root this also works after login:

```bash
firebase deploy --only firestore:rules
```

## What happens after rules are live

- Staff open the public Friday request page.
- They choose a staff name, Friday, and whether they can work another Friday instead.
- Google sign-in identifies the submitting account.
- The request is saved to Firestore collection `fridayOffRequests`.
- The page shows a green `Request saved ✓` confirmation.
- Duplicate submissions for the same staff/date overwrite the same deterministic record instead of creating duplicates.

## Admin view

`https://jacobevans-cell.github.io/jacobevans-cell-Friday-Rotation-Board/admin.html`

Admin data access is restricted by Firestore rules to:

- `jacob.evans@explore.academy`
- `jacobicusjax@gmail.com`

The admin page shows all requests, groups them by Friday, counts remaining available staff, flags coverage conflicts, and can remove a request.

## Active staff

- Lingam
- Evans
- Latoya
- Meda
- Abby

Dorr and McKinley are not part of future Friday scheduling.
