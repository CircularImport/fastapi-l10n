import logging

from functools import partial
from typing import Annotated, Callable, Union

from fastapi import Depends, Header

from fastapi_localization.l10n import localization
from fastapi_localization.parser import accept_language_parser


__all__ = ["L10nDepends"]


logger = logging.getLogger(__name__)


async def localization_dependency(
    accept_language: Annotated[Union[str, None], Header()] = None,
) -> Callable[[str, dict], str]:
    """
    Dependency function to determine the localization based on the Accept-Language header.

    :param accept_language: The Accept-Language header value.
    :type accept_language: str | None
    :return: A partially applied gettext function with the selected locale.
    :rtype: Callable[[str, dict], str]
    """
    locale = localization.default_locale

    if accept_language is not None:
        language_preferences = accept_language_parser(accept_language=accept_language)
        for language_preference in language_preferences:
            if language_preference.language in localization.allowed_locales:
                locale = language_preference.language
                logger.debug(f"Selected {locale=}")
                break
        else:
            logger.debug(f"Using default {locale=}")
    else:
        logger.debug(f"Using default {locale=}")
    return partial(localization.gettext, locale=locale)


L10nDepends = Annotated[Callable[[str, dict], str], Depends(dependency=localization_dependency)]
"""
Dependency to determine the localization based on the Accept-Language header.

E.g::

    from fastapi import FastAPI
    from fastapi_localization import L10nDepends

    app = FastAPI()

    @app.get("/")
    async def root(_: L10nDepends):
        return _("hello-message", args={"username": "John"})
"""
