# 🤖 Copilot Instructions for AI Agents

## Project Overview
- This is a FastAPI-based Python project with modular structure under `app/`.
- Key submodules: `auth/`, `models/`, `operations/`, `schemas/`, and database logic in `database.py`/`database_init.py`.
- Entry point: `main.py` (runs FastAPI app).
- Uses SQLAlchemy for database access and `psycopg2-binary` for PostgreSQL.

## Directory Structure
- `app/` — Main application code
  - `auth/` — Authentication logic (dependencies, hashing, etc.)
  - `models/` — SQLAlchemy models (e.g., `user.py`)
  - `schemas/` — Pydantic schemas for request/response validation
  - `operations/` — Business logic and service layer
  - `config.py` — App configuration
  - `database.py`, `database_init.py` — DB connection and setup
- `tests/` — Organized into `unit/`, `integration/`, and `e2e/`
- `templates/` — Jinja2 HTML templates
- `requirements.txt` — Python dependencies
- `Dockerfile`, `docker-compose.yml` — Containerization support

## Developer Workflows
- **Install dependencies:** `pip install -r requirements.txt`
- **Run app locally:** `python main.py`
- **Run tests:** Use `pytest` (tests in `tests/`)
- **Docker:**
  - Build: `docker build -t <image-name> .`
  - Run: `docker run -it --rm <image-name>`

## Patterns & Conventions
- All API logic is routed through FastAPI in `main.py`.
- Models and schemas are separated for clarity (see `app/models/` and `app/schemas/`).
- Authentication and hashing logic is in `app/auth/`.
- Use dependency injection via FastAPI's `Depends` for auth and DB access.
- Test files mirror app structure and are grouped by type.
- Use environment variables/config for DB and secrets (see `config.py`).

## Integration Points
- Database: PostgreSQL via SQLAlchemy/psycopg2.
- Web: FastAPI (Starlette under the hood), Jinja2 for HTML rendering.
- Docker: For reproducible local/dev environments.

## Examples
- To add a new model: create in `app/models/`, add schema in `app/schemas/`, update DB logic in `database.py`.
- To add a new API route: define in `main.py` or a submodule, register with FastAPI app.

## References
- See `README.md` for full setup, workflow, and troubleshooting details.
- Use `pytest` for all test types; structure new tests to match app modules.

---

**Update this file if you introduce new major modules, workflows, or conventions.**
