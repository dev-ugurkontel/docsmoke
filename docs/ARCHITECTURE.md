# Architecture

`docsmoke` is organized as a small typed Python application with four layers:

1. `cli.py`: user interface and exit-code policy
2. `runner.py`: file discovery and scan orchestration
3. `markdown.py` and `executor.py`: snippet discovery and execution
4. `reporting/`: format-specific output rendering

## Core flow

1. Load configuration from `docsmoke.toml` or `pyproject.toml`
2. Resolve Markdown files from explicit paths or configured include globs
3. Discover runnable fenced blocks
4. Strip and parse leading `docsmoke` directives
5. Execute snippets with the matching executor
6. Evaluate expectations and render the final report

## Safety model

- Supported executors are intentionally small and explicit
- Snippets are opt-in by default
- Each snippet has a timeout
- Execution occurs relative to the project root unless overridden

## Extension points

- Add new executors
- Add new report formats
- Add richer discovery heuristics for docs linting and drift risk analysis
