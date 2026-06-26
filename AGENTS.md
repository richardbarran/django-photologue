# AGENTS.md

## Running the Full Test Matrix

Run tox from the repository root:

```bash
tox
```

## Running Unit Tests

Run the Django unit tests from the example project directory:

```bash
cd example_project
./manage.py test photologue
```

Alternatively, use the helper script from the repository root:

```bash
python scripts/run_tests.py
```

Any extra arguments are passed through to `manage.py test`:

```bash
python scripts/run_tests.py photologue.tests.test_models
```
