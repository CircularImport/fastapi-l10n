from dataclasses import dataclass


__all__ = ["LanguagePreference"]


@dataclass(frozen=True)
class LanguagePreference:
    """
    Represents a language and its weight from the `Accept-Language` header.

    :param language: The language code (e.g., "en-US", "fr").
    :param weight: The weight (priority) of the language, default is 1.0.
    """

    language: str
    weight: float = 1.0
