

---

```markdown
# 📦 Project Setup

---

# 🏗️ Project Scaffold

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── auth/
│   ├── config.py
│   ├── database.py
│   ├── database_init.py
│   ├── models/
│   ├── operations/
│   └── schemas/
├── docker-compose.yml
├── main.py
├── pytest.ini
├── requirements.txt
├── templates/
│   └── index.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── e2e/
│   ├── integration/
│   └── unit/
```

---

# 🎯 Project Overview

This project implements **user authentication and dependency management** using **FastAPI, SQLAlchemy, and JWT**.  
It includes:

- User model with password hashing and JWT utilities  
- Authentication dependencies (`get_current_user`, `get_current_active_user`)  
- Database initialization and migrations  
- Full test suite (unit, integration, and end‑to‑end)  

✅ **All provided tests pass** (`pytest -v`).

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

---

# 🧩 2. Install and Configure Git

```bash
# Mac
brew install git

# Windows
# Download from https://git-scm.com/download/win
git --version
```

Configure globals:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

---

# 🧩 3. Clone the Repository

```bash
git clone <repository-url>
cd module10_is601
```

---

# 🛠️ 4. Install Python 3.10+

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

```bash
docker build -t module10_is601 .
docker run -it --rm module10_is601
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

- **With Docker**:

```bash
docker run -it --rm module10_is601
```

---

# 🗄️ 7. Database Initialization

Before running tests or the app, initialize the database schema:

```bash
python -m app.database_init
```

---

# 🧪 8. Running Tests

Run the full test suite:

```bash
pytest -v
```

Generate coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

---

# 📝 9. Submission Instructions

1. Ensure all tests pass (`pytest -v`).  
2. Commit and push your changes:

```bash
git add .
git commit -m "Final Module 10 submission: all tests passing"
git push origin main
```

3. Submit the **GitHub repository link** to your professor.

---

# 🔥 Useful Commands Cheat Sheet

| Action                     | Command                                |
|-----------------------------|----------------------------------------|
| Create venv                | `python3 -m venv venv`                 |
| Activate venv (Mac/Linux)  | `source venv/bin/activate`             |
| Activate venv (Windows)    | `venv\Scripts\activate.bat`            |
| Install packages           | `pip install -r requirements.txt`      |
| Init DB                    | `python -m app.database_init`          |
| Run tests                  | `pytest -v`                            |
| Coverage                   | `pytest --cov=app --cov-report=term-missing` |
| Push to GitHub             | `git add . && git commit -m "msg" && git push` |

---

# 📋 Notes

- Use **Python 3.10+**.  
- Always initialize the DB before running tests.  
- `.gitignore` excludes `venv/`, caches, and coverage files.  
- Docker is optional.  

---

# 📎 Quick Links

- [Python Downloads](https://www.python.org/downloads/)  
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)  
```

---

This file is ready to be committed and pushed:

```bash
git add README.md
git commit -m "Add final README with setup and submission instructions"
git push origin main
```

Test trigger Tue Nov  4 10:03:30 EST 2025
Trigger CI Tue Nov  4 10:17:36 EST 2025
