# Airport Flight Tracker ✈️

A full-stack application for tracking takeoffs, landings, and flight manifests at small regional and municipal airports in the United States. Targets general aviation: student pilots, hobbyists, and private aircraft.

## Features

- 🔍 **Pilot Flight History Search** - Search pilots by name and view their complete flight history
- 📊 **Dashboard** - Overview statistics of flights, pilots, aircraft, and airports
- ✈️ **Aircraft Registry** - Track aircraft by tail number, type, and owner
- 🛬 **Flight Logs** - Record takeoffs, landings, and touch-and-go operations
- 🏢 **Airport Database** - Regional/municipal airport information

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, React Query
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Deployment**: Docker, Railway

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python seed_data.py  # Optional: add sample data
uvicorn main:app --reload
```

Backend runs at http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

---

## 🚀 Deploy to Railway

### Step 1: Push to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - Airport Flight Tracker"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/airport-flight-tracker.git
git branch -M main
git push -u origin main
```

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `airport-flight-tracker` repository
4. Railway will detect the project structure

### Step 4: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway automatically creates `DATABASE_URL` variable

### Step 5: Configure Backend Service

1. Click on the backend service
2. Go to **Settings** → **Root Directory** → Set to `backend`
3. Go to **Variables** tab and add:
   ```
   SECRET_KEY=<generate-a-secure-random-string>
   DEBUG=false
   ```
   
   Generate a secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. Railway auto-links `DATABASE_URL` from PostgreSQL

### Step 6: Configure Frontend Service

1. Click **"+ New"** → **"GitHub Repo"** (same repo)
2. Go to **Settings** → **Root Directory** → Set to `frontend`
3. Go to **Variables** tab and add:
   ```
   BACKEND_URL=<your-backend-railway-internal-url>
   ```

### Step 7: Generate Domains

1. For each service, go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. You'll get URLs like:
   - Backend: `airport-tracker-backend-xxx.up.railway.app`
   - Frontend: `airport-tracker-frontend-xxx.up.railway.app`

### Step 8: Update CORS

Add your frontend Railway domain to backend variables:
```
FRONTEND_URL=https://your-frontend-xxx.up.railway.app
```

---

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | SQLite (dev) |
| `SECRET_KEY` | JWT signing key | **Must change in prod** |
| `DEBUG` | Enable debug mode | `false` |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:5173` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `/api/v1` |
| `BACKEND_URL` | Backend URL for nginx proxy | Required in prod |

---

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, database
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── hooks/        # Custom hooks
│   │   └── types/        # TypeScript types
│   └── package.json
└── docker-compose.yml
```

## License

MIT
