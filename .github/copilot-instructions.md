# Airport Flight Tracker - Copilot Instructions

## Project Overview
A full-stack application for tracking takeoffs, landings, and flight manifests at small regional and municipal airports in the United States. Targets general aviation: student pilots, hobbyists, and private aircraft.

## Tech Stack
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, React Query
- **Database**: SQLite (dev), PostgreSQL-ready (prod)
- **Containerization**: Docker, Docker Compose

## Project Structure
```
/backend          - FastAPI application
  /app
    /api          - API route handlers
    /core         - Configuration, database, security
    /models       - SQLAlchemy models
    /schemas      - Pydantic schemas
    /services     - Business logic
/frontend         - React application
  /src
    /components   - Reusable UI components
    /pages        - Page components
    /services     - API client
    /hooks        - Custom React hooks
    /types        - TypeScript types
```

## Key Features
- Airport database (FAA data for non-major US airports)
- Flight log tracking (takeoffs, landings, timestamps, runways)
- Aircraft registry (tail numbers, type, owner info)
- Pilot tracking (certificates, flight hours)
- Search and filtering
- Dashboard with statistics

## Development Guidelines
- Use async/await for all database operations
- Follow REST API conventions
- Use TypeScript strict mode
- Keep components small and focused
- Write descriptive commit messages
