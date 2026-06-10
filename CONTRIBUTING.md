# Contributing

Thank you for your interest in contributing!

## Setup

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your database credentials.

## Running tests

```bash
pytest tests/ -v
```

## Code style

- Follow PEP 8.
- Add docstrings to all public functions and classes.
- Keep business logic in `roles/`, database logic in `db/`, validation in `utils/`.
- Do not put `print` or `input` calls inside `db/` or `roles/` methods that are not user-facing menus.

## Pull requests

- One feature or fix per PR.
- Reference the issue number in the PR description.
- Ensure all tests pass before submitting.
