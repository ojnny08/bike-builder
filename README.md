# BikeBuilder

## Prerequisites

- Python 3.11+
- Node 18+
- PostgreSQL

## Backend Setup

```bash
cd bikebuilder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE bikebuilder;
```

Add your Firebase credentials file at:

```
bikebuilder/firebase/firebase-credentials.json
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Backend runs at `http://localhost:8000`

## Frontend Setup

```bash
cd bikebuilder-frontend
npm install
```

Create a `.env` file in `bikebuilder-frontend/`:

```
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
```

Start the dev server:

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

## Project structure

```
bikebuilder/                  Django project
  bikebuilder/                settings, urls, wsgi
  apps/
    core/                     Firebase JWT authentication
    components/               catalogue, compatibility, image normalization
    builds/                   user builds + image upload
    category/                 bike types and their rules
    comments/  users/  vote/
  scripts/                    scrapers + loaders (see scripts/README.md)
  backups/                    local dumpdata snapshots (gitignored)

bikebuilder-frontend/         React (Vite)
  src/
    api/                      axios instance, firebase config
    assets/                   images
    bike3d/                   three.js scene + canvas
    components/               shared UI, one folder per component
    context/                  auth + build providers
    hooks/  services/  utils/
    pages/                    one folder per route, CSS colocated
```

Conventions: CSS lives beside the component or page it styles; API routes are
prefixed with `/api/`; compatibility filtering happens server-side.

## Environment

Backend config is read from `bikebuilder/.env` — see `bikebuilder/.env.example`
for the full list. `DEBUG`, `ALLOWED_HOSTS` and the database settings are
env-driven, defaulting to local development values.

## Populating the catalogue

The component catalogue is built by the scrapers and loaders in
`bikebuilder/scripts/`. See `bikebuilder/scripts/README.md` for the run order.
