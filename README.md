# High-Performance Data Processing System

A full-stack data processing project combining a C++ processing engine, a FastAPI backend, PostgreSQL persistence, and a React dashboard.

## Tech Stack

- **C++** — Core data processing and benchmarking
- **Python / FastAPI** — REST API
- **PostgreSQL** — Job persistence
- **SQLAlchemy** — Database access
- **React / Vite** — Frontend dashboard
- **Pytest** — Backend testing

## Architecture

```text
React Dashboard
      |
      v
FastAPI Backend
      |
      +----> C++ Processing Engine
      |
      +----> PostgreSQL Database
```

## Features

- Process integer datasets and calculate minimum, maximum, and sum.
- Submit processing jobs through the API.
- Store job results in PostgreSQL.
- Retrieve individual jobs and browse job history with pagination.
- View processing results and job history in a React dashboard.
- Test the C++ processing logic and FastAPI endpoints.

## Project Structure

```text
data-processing-system/
├── backend/
├── cpp-engine/
├── frontend/
├── .gitignore
└── README.md
```

## Running Locally

### 1. C++ Engine

Compile the processing engine using a C++ compiler that supports C++11 or later. Follow the source code's input/output contract when running the executable.

### 2. Backend

Install the backend dependencies listed in your Python environment or dependency file. Configure `DATABASE_URL` in a local `.env` file, create the PostgreSQL database, and start FastAPI:

```bash
python -m uvicorn main:app --reload
```

Run this command from the `backend` directory.

API documentation is available at `http://127.0.0.1:8000/docs` while the server is running.

### 3. Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite in your terminal.

## Testing

Run the backend tests from the `backend` directory:

```bash
python -m pytest -v
```

Compile and run the C++ unit tests from the `cpp-engine` directory:

```bash
g++ -std=c++11 tests.cpp processor.cpp -o tests.exe
./tests.exe
```

## Security

- Keep `.env` files and credentials out of version control.
- Do not commit database passwords or API keys.
- Use local environment variables for sensitive configuration.

## Future Improvements

- Add automated CI checks.
- Improve benchmark methodology and document reproducible results.
- Consider a background job queue for larger workloads.
