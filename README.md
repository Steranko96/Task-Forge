## Local Development Setup

TaskForge is a server-rendered task management application built with Python and Django.

### Prerequisites

Before starting, ensure you have:

- Python 3.14 installed
- Git installed
- A terminal
- Access to the TaskForge GitHub repository

The project currently uses Django 5.2.18.

### 1. Clone the repository

```bash
git clone https://github.com/Steranko96/Task-Forge.git
cd Task-Forge
```

### 2. Create a virtual environment

Create an isolated Python environment for the project:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Verify the active Python version:

```bash
python --version
```

The project currently targets Python 3.14.

### 3. Install dependencies

Install the project's declared dependencies:

```bash
python -m pip install -r requirements.txt
```

The requirements file pins Django 5.2.18. pip automatically resolves and installs Django's required dependencies.

### 4. Verify the Django configuration

Run Django's system checks:

```bash
python manage.py check
```

A successful check should report:

```text
System check identified no issues (0 silenced).
```

This verifies that Django detects no problems covered by its registered system checks. It does not guarantee that all application functionality works.

### 5. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

You should see Django's default welcome page.

Stop the development server with `Control-C`.

### 6. Deactivate the virtual environment

When finished working:

```bash
deactivate
```

### Development Notes

- The `.venv/` directory contains local environment files and must not be committed to Git.
- Python dependencies are declared in `requirements.txt`.
- Django project configuration is located in `taskforge/`.
- The `tasks/` application will contain TaskForge's task-management functionality.
- The development server is intended for local development only.
- Django may report unapplied migrations during initial setup. Database configuration and migrations will be handled in later engineering tickets.
- A clean-checkout installation test remains outstanding for TSK-003.

### Technology Versions

| Component | Version |
|---|---|
| Python | 3.14 |
| Django | 5.2.18 |
| Package installer | pip |
| Development database | Django's default SQLite configuration, pending PostgreSQL setup |

Production deployment will eventually use PostgreSQL, Docker, Gunicorn and Caddy, as specified in the TaskForge project requirements.

## Development Workflow

TaskForge follows a ticket-based Git workflow to maintain clear project history, isolate changes, and encourage code review.

### Branching Strategy

- `main` is the primary branch and should contain reviewed, working code.
- Each engineering ticket is developed on a dedicated branch created from `main`.
- Branches follow the naming convention `task/TSK-XXX-short-description`.
- Avoid committing development changes directly to `main`.

Example:

`task/TSK-003-python-environment`

### Commit Conventions

Commits follow the format:

`<type>: <short description>`

Common commit types:

- `feat` — New functionality
- `fix` — Bug fixes
- `test` — Automated tests
- `docs` — Documentation changes
- `chore` — Configuration, tooling, and maintenance
- `refactor` — Code restructuring without changing behaviour

Commits should be small, focused, and descriptive. Avoid generic messages such as `updates` or `fixed stuff`.

### Pull Request Workflow

1. Create a ticket-specific branch from the latest `main`.
2. Implement the ticket requirements and add relevant tests.
3. Review changes locally, ensuring no secrets or generated files are included.
4. Commit and push the branch to GitHub.
5. Open a pull request referencing the engineering ticket.
6. Verify acceptance criteria, review the diff, and resolve any identified issues.
7. Merge into `main` only after verification is complete.

### Definition of Ready to Merge

A pull request is ready to merge when:

- Ticket acceptance criteria have been satisfied.
- Relevant tests and checks pass, where available.
- Changes have been reviewed for correctness, security, and maintainability.
- No credentials, local environment files, or generated artifacts are committed.
- Relevant documentation has been updated.

After merging, update the ticket's status in Trello and record verification evidence.
