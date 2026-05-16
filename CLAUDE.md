# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **OS**: Windows with PowerShell
- **Python**: 3.11+ (detected from venv)
- **Venv location**: `.venv/` at repo root
- **Database**: SQLite (file: `expense_tracker.db`)

When running commands, use PowerShell syntax:
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run Flask app
python app.py

# Run tests
pytest
```

## Project Overview

**Spendly** is a personal finance tracker built with Flask. It's a student project where features are implemented incrementally across "steps".

### Tech Stack
- **Backend**: Flask 3.1.3, Werkzeug 3.1.6
- **Frontend**: Jinja2 templates, HTML, CSS (fully designed), vanilla JavaScript
- **Testing**: pytest 8.3.5, pytest-flask 1.3.0
- **Database**: SQLite (not yet integrated into Python)

### Architecture

**Routing (app.py)**
- `/` — landing page (fully implemented)
- `/register` → GET shows form, POST should validate and create user
- `/login` → GET shows form, POST should validate and authenticate
- `/logout`, `/profile` — placeholders for future steps
- `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` — placeholders

**Database Layer (database/db.py)**
- Currently a placeholder with comments
- Must implement three functions (per comments):
  - `get_db()` — returns SQLite connection with row_factory and foreign keys enabled
  - `init_db()` — creates all tables using CREATE TABLE IF NOT EXISTS
  - `seed_db()` — inserts sample data for development
- Database file: `expense_tracker.db` (created at runtime)

**Templates (templates/)**
- `base.html` — master layout with navbar, footer, shared styles and scripts
- All pages extend `base.html` using Jinja2 blocks: `{% block title %}`, `{% block content %}`, `{% block scripts %}`
- `landing.html` — marketing/homepage with hero, features, CTA
- `login.html`, `register.html` — auth forms with error display (`{% if error %}`)

**Static Assets (static/)**
- `css/style.css` — complete design system with CSS variables (--ink, --accent, --paper, etc.), responsive grid layouts, form styles, button states
- `js/main.js` — placeholder for frontend logic

## Common Commands

```powershell
# Install/update dependencies
pip install -r requirements.txt

# Run the Flask app locally (debug mode on port 5001)
python app.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=.

# Initialize the database (once database/db.py is implemented)
python -c "from database.db import init_db; init_db()"
```

## Key Implementation Details

### Routing Convention
- Routes are defined directly in `app.py` using `@app.route()` decorator
- Template rendering uses `render_template("template_name.html", context_vars)`
- All HTML responses go through Jinja2 templating

### Template Inheritance Pattern
Every page extends `base.html`:
```jinja2
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}<main content here>{% endblock %}
```

### Form Handling
- Forms use `method="POST"` with Flask routes
- Error messages displayed via `{% if error %}<div class="auth-error">{{ error }}</div>{% endif %}`
- Inputs follow the class pattern: `.form-input` (styled in CSS)

### Database (Future)
- The `database/db.py` must provide `get_db()` function that returns a connection
- All database schemas should be created in `init_db()` with IF NOT EXISTS clauses
- Foreign keys must be enabled: `PRAGMA foreign_keys = ON`

### CSS System
- All colors, fonts, spacing are CSS custom properties (`:root { --variable: value }`)
- Grid-based responsive layout with `max-width: var(--max-width)` container
- Button classes: `.btn-primary` (dark), `.btn-ghost` (outlined)
- Form styles: `.form-group`, `.form-input`, `.btn-submit`

## Testing Strategy

Tests use `pytest` and `pytest-flask`. Example test file structure:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Spendly' in response.data
```

## Git & Deployment

- Remote: `https://github.com/sourav7890iit/spendly.git`
- Branch: `master`
- Before pushing: ensure tests pass (`pytest`) and app runs locally (`python app.py`)

## Notes for Implementation

1. **Database Setup is Step 1** — Many features depend on `database/db.py` being implemented first
2. **Auth Routes** (login, register) need form processing logic + hashing (e.g., werkzeug.security)
3. **Form Validation** — validate email format, password length (comment in register.html says "Min. 8 characters")
4. **Session Management** — Flask sessions or JWT tokens needed for `/logout` and `/profile`
5. **Expense CRUD** — Routes exist but need database queries + template views
