# Contributing to Django Clickify

First off, thank you for considering contributing to Django Clickify!
Contributors like you make open source projects successful and enjoyable. 🎉

---

## How Can You Contribute?

Contributions are welcome in many forms:

- **Reporting Bugs:** Open an issue with a clear description, example code, or steps to reproduce.
- **Suggesting Enhancements:** Have a feature idea or improvement? Open an issue to discuss it.
- **Writing Documentation:** Help improve docs, tutorials, or examples.
- **Submitting Code:** Follow the steps below for adding or fixing code.

---

## Getting Started

We use **Poetry** for dependency management and **Ruff** for linting and formatting.

### 1. Clone the repository

```bash
git clone https://github.com/romjanxr/django-clickify.git
cd django-clickify
```

### 2. Install dependencies

```bash
make install
```

This runs `poetry install` and sets up all required packages.

### 3. Optional: Install pre-commit hooks

```bash
make precommit
```

Pre-commit hooks will automatically check formatting and linting before each commit.

---

## Branching & Pull Requests

1. **Create a new branch** for your work:

```bash
git checkout main
git pull
git checkout -b feat/my-feature
```

2. **Make your changes** in the new branch.

3. **Run formatting and lint checks**:

```bash
make format   # Auto-fix formatting and linting
make check    # Verify code style without modifying files
```

4. **Run the test suite** to ensure nothing is broken:

```bash
make test
```

5. **Commit your changes** with a clear message:

```bash
git add .
git commit -m "feat: describe your feature"
```

6. **Push your branch** to your fork:

```bash
git push origin feat/my-feature
```

7. **Open a Pull Request** targeting the `main` branch of the original repository.
   Include a clear title, description, and reference any related issues.

---

## Code Style & Guidelines

- **Formatting:** Ruff handles formatting and linting; contributors only need to run `make format`.
- **Line length:** 88 characters.
- **Docstrings:** Required where meaningful, ignored in tests, migrations, and trivial methods.
- **Excluded folders:** `.venv/`, `venv/`, `migrations/`, `__pycache__/`.

> Following these ensures your code passes automated checks and CI/CD pipelines.

---

Thank you for helping make **Django Clickify** better! 👌
