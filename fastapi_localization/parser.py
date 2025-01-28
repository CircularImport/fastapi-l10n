import logging

from fastapi_localization.types import LanguagePreference


__all__ = ["accept_language_parser"]


logger = logging.getLogger(__name__)


def accept_language_parser(accept_language: str) -> list[LanguagePreference]:
    """
    Parses the `Accept-Language` header and returns a list of `LanguagePreference` objects,
    sorted by weight in descending order.

    :param accept_language: The value of the `Accept-Language` header.
    :return: A list of `LanguagePreference` objects, sorted by weight in descending order.

    E.g::

        >>> accept_language_parser("en-US,en;q=0.9,fr;q=0.8,de;q=0.7")
        [
            LanguagePreference(language='en-US', weight=1.0),
            LanguagePreference(language='en', weight=0.9),
            LanguagePreference(language='fr', weight=0.8),
            LanguagePreference(language='de', weight=0.7)
        ]
    """
    languages = []

    # Split the header by commas to get individual language entries
    for entry in accept_language.split(","):
        entry = entry.strip()
        if not entry:
            continue

        # Split into language and weight (if present)
        parts = entry.split(";")
        language = parts[0].strip()

        # Default weight is 1.0 if not specified
        weight = 1.0
        for part in parts[1:]:
            if part.strip().startswith("q="):
                raw_weight = part.strip()[2:]
                try:
                    weight = float(raw_weight)
                except ValueError:
                    # If the weight is invalid, use the default
                    logger.debug(f"Weight '{raw_weight}' is invalid, use the default {weight=}")
                    weight = 1.0

        languages.append(LanguagePreference(language=language, weight=weight))

    # Sort by weight in descending order
    languages.sort(key=lambda x: x.weight, reverse=True)

    return languages
