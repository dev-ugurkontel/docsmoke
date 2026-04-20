# docsmoke

`docsmoke` validates executable documentation snippets before they drift out of
sync with reality.

The project is a production-focused CLI for running shell and Python examples
embedded in Markdown files, asserting on expected output, and failing CI when
docs stop matching the software they describe.

The repository is intentionally structured like a release-ready open source
project: typed Python package, test suite, governance docs, CI, release
automation, and a GitHub Action.

