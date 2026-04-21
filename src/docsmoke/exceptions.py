"""docsmoke exception hierarchy."""


class DocsmokeError(Exception):
    """Base error for user-facing docsmoke failures."""


class ConfigError(DocsmokeError):
    """Invalid configuration or user input."""


class DirectiveError(DocsmokeError):
    """Invalid docsmoke directive embedded in a snippet."""
