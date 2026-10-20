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
