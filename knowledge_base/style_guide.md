# Code Style Guide

## Python Conventions

This project targets Python 3.11 and follows PEP 8 with a line length of 100 characters. Formatting is enforced by `ruff format` and linting is handled by `ruff check`. Both run as part of the pre-commit hook, so style violations should never reach the main branch. Type hints are required on every public function and on any private helper whose signature is not obvious from a single glance.

Prefer standard library modules over third-party dependencies whenever the standard library can do the job within ten lines of additional code. The dependency footprint for this project is small on purpose; new packages should be justified in the pull request description.

## Naming

Module names are lowercase with underscores. Classes use `CamelCase`, functions and variables use `snake_case`, and module-level constants use `UPPER_SNAKE_CASE`. Avoid abbreviations except for widely understood ones such as `cfg`, `idx`, or `req`. Function names should read as verbs (`load_index`, `resolve_path`) and boolean variables should read as predicates (`is_indexed`, `has_excerpt`).

## Error Handling

Catch exceptions at the boundary between the transport layer and the tools layer. Inside the tools layer, raise specific exception types (`FileNotFoundError`, `PermissionError`, `ValueError`) and let the transport layer translate them into MCP error responses with appropriate error codes. Never catch a bare `Exception` except at the outermost handler, and never swallow an exception silently. If a caller cannot recover from a failure, the failure should be visible in the logs.

## Documentation

Every public function carries a one-line docstring describing what it does, not how. Implementation details belong in inline comments, and only when the code itself does not already make the intent clear. README and onboarding documentation lives at the repository root; internal architectural notes live under `knowledge_base/` so that the server can serve them back to the LLM during development.
