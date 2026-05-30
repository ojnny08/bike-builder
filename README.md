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
