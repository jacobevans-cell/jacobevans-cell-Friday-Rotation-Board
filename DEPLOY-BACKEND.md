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
4. Publish the repository's `firestore.rules` once, either manually or through the GitHub deployment bridge below.

## GitHub → Firebase deployment bridge

The repo contains `.github/workflows/deploy-firebase.yml`.

Once the repository secret below exists, any future change to `firestore.rules`, `firebase.json`, or `.firebaserc` on `main` automatically deploys Firestore rules to Firebase project `friday-rotation-board`.

Required repository secret:

`FIREBASE_SERVICE_ACCOUNT_FRIDAY_ROTATION_BOARD`

To create it:

1. Firebase Console → Project settings → Service accounts.
2. Generate a new private key for the Firebase Admin SDK service account.
3. Download the JSON file.
4. GitHub repo → Settings → Secrets and variables → Actions → New repository secret.
5. Name it exactly `FIREBASE_SERVICE_ACCOUNT_FRIDAY_ROTATION_BOARD`.
6. Paste the complete JSON file contents as the secret value.
7. Do **not** commit that JSON file or paste it into chat.

After the secret exists, open GitHub → Actions → `Deploy Friday Firebase Rules` → Run workflow, or simply make a rules change on `main`.

## Manual Firebase CLI fallback

```bash
firebase login
firebase deploy --only firestore:rules --project friday-rotation-board
```

The repository's `.firebaserc` already points to `friday-rotation-board`, so from the repo root this also works after login:

```bash
firebase deploy --only firestore:rules
```

## What happens after rules are live

- Staff submit requests on the main GitHub Pages site.
- Each saved request gets a green `Request saved ✓` confirmation.
- Requests are stored centrally in Firestore collection `fridayOffRequests`.
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
