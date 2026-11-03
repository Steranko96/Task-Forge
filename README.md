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

### Configure Environment Variables

TaskForge uses environment variables to manage application settings and credentials.

Copy the example configuration file:

```bash
cp .env.example .env
```

Open `.env` and replace `SECRET_KEY=change-me` with a unique secret key.

You can generate one using Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

For local development, use:

```dotenv
APP_ENV=development
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
```

TaskForge uses SQLite in development, so PostgreSQL connection variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) are not required locally.

In production, set `APP_ENV=production`, `DEBUG=false`, configure the permitted hostnames, and supply valid PostgreSQL credentials.

**Security:** Never commit `.env` or real credentials to Git. Only `.env.example`, containing safe examples and placeholders, should be tracked.

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

## Local PostgreSQL Development Setup

TaskForge uses PostgreSQL as its relational database. Django accesses PostgreSQL through its ORM and the `psycopg` database adapter.

### Prerequisites

- macOS (Apple Silicon)
- Homebrew
- Python and the project's virtual environment
- PostgreSQL 17

### 1. Install and start PostgreSQL

```bash
brew install postgresql@17
brew services start postgresql@17
```

Add the PostgreSQL command-line tools to your shell path if required:

```bash
echo 'export PATH="$(brew --prefix)/opt/postgresql@17/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

Verify the installation:

```bash
psql --version
pg_isready -h 127.0.0.1 -p 5432
```

### 2. Create the development database

Connect to the default PostgreSQL database:

```bash
psql -d postgres
```

Create a dedicated database role:

```sql
CREATE ROLE taskforge_user WITH LOGIN;
```

Set the role's password securely using the PostgreSQL interactive command:

```text
\password taskforge_user
```

Create the application database:

```sql
CREATE DATABASE taskforge_dev OWNER taskforge_user;
```

Exit PostgreSQL with `\q`.

The dedicated database role owns the development database, allowing Django to create and modify tables through migrations without using a PostgreSQL administrator account.

### 3. Configure environment variables

TaskForge reads its database configuration from environment variables.

The development configuration requires:

| Variable | Development value |
|---|---|
| `DB_NAME` | `taskforge_dev` |
| `DB_USER` | `taskforge_user` |
| `DB_PASSWORD` | Locally configured secret |
| `DB_HOST` | `127.0.0.1` |
| `DB_PORT` | `5432` |

Use the project's existing environment-loading mechanism to supply these values.

Do not commit database passwords, `.env` files containing secrets, or production credentials to Git.

### 4. Install Python dependencies

Activate the project's virtual environment and install the dependencies recorded in the project dependency file.

The PostgreSQL database adapter is `psycopg` version 3.

Verify its installation:

```bash
python -m pip show psycopg
```

### 5. Initialise the database schema

Run Django's system checks:

```bash
python manage.py check --database default
```

Inspect pending migrations:

```bash
python manage.py migrate --plan
```

Apply migrations:

```bash
python manage.py migrate
```

Inspect migration history:

```bash
python manage.py showmigrations
```

Applied migrations appear with `[X]`.

### 6. Verify PostgreSQL connectivity

```bash
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor, connection.settings_dict['NAME'])"
```

Expected output for the documented development configuration:

```text
postgresql taskforge_dev
```

### 7. Verify data persistence

Create a temporary record through the Django ORM, restart the application, and retrieve the record from a new Django process.

For stronger verification, restart the PostgreSQL service without deleting its database files:

```bash
brew services restart postgresql@17
```

Then query the same record again.

After confirming persistence, remove the temporary record.

Application restarts should not remove PostgreSQL data because the database server stores records independently of the Django process.

### Troubleshooting

| Problem | Possible cause |
|---|---|
| Connection refused | PostgreSQL stopped or incorrect host/port |
| Authentication failed | Incorrect database username or password |
| Database does not exist | Database not created or incorrect name |
| Permission denied | Insufficient database privileges |
| Missing `psycopg` module | Database adapter not installed in the active virtual environment |

### Architecture note

Local development uses a PostgreSQL installation managed by Homebrew.

Docker Compose integration, including container networking and persistent volumes, is handled separately in TSK-028.

## Database Design

### Task Model

TaskForge uses a relational database model in which each task belongs to exactly one user.

The application uses Django's built-in User model for authentication and task ownership.

### Task Schema

| Field | Django Field Type | Constraints / Behaviour |
|---|---|---|
| `id` | BigAutoField | Auto-generated primary key |
| `owner` | ForeignKey(User) | Required, non-null, `on_delete=CASCADE` |
| `title` | CharField | `max_length=50`, required |
| `description` | TextField | Optional, `blank=True`, empty string rather than NULL |
| `is_completed` | BooleanField | Required, `default=False` |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

### Ownership Relationship

The relationship between User and Task is one-to-many:

- One user can own multiple tasks.
- Each task must belong to exactly one existing user.
- Tasks cannot exist without an owner.
- The `owner` foreign key maintains referential integrity.
- Deleting a user cascades deletion to all tasks owned by that user.

### Validation and Data Integrity

- Task titles are required and limited to 50 characters.
- Empty and whitespace-only titles must be rejected through application validation.
- Task descriptions are optional and may contain an empty string.
- New tasks default to an incomplete state.
- Database constraints enforce non-null ownership and valid user references.
- Model/form validation provides additional input checks. Direct ORM writes must not be assumed to invoke model validation automatically.

### Security Considerations

Database ownership does not automatically provide authorisation.

TaskForge must enforce user isolation at the application layer:

- Authenticated users may access only their own tasks.
- Task queries must be scoped to the authenticated user.
- Task ownership must be assigned server-side rather than trusted from client input.
- Cross-user read, update, and delete operations must be prevented.

These authorisation controls will be implemented and tested in subsequent tickets.

### Design Decisions

- Use Django's built-in User model to avoid unnecessary complexity.
- Use `CASCADE` deletion to keep ownership management simple.
- Use a maximum title length of 50 characters.
- Store absent descriptions as empty strings rather than NULL.
- Include creation and update timestamps for basic record tracking.
- Defer task model implementation and migrations to TSK-008.

**Status:** Schema design agreed in TSK-007. Implementation and database verification are pending subsequent tickets.
