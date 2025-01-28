import logging

from typing import Any, Optional, Union

from fluent.runtime import FluentBundle, FluentResourceLoader
from fluent.runtime.resolver import Pattern


__all__ = [
    "Localization",
    "localization",
    "setup_localization",
]


logger = logging.getLogger(__name__)


class Localization:
    """
    A class for handling localization using Fluent.
    """

    def __init__(self):
        self.allowed_locales: Optional[list[str]] = None
        self.default_locale: Optional[str] = None
        self.resource_ids: Optional[dict[str, list[str]]] = None
        self.loader: Optional[FluentResourceLoader] = None
        self.locales: Optional[dict[str, FluentBundle]] = None

    def setup(
        self,
        allowed_locales: list[str],
        default_locale: str,
        resource_ids: dict[str, list[str]],
        roots: Union[str, list[str]] = "locales/{locale}",
    ) -> None:
        if default_locale not in allowed_locales:
            allowed_locales.append(default_locale)

        self.allowed_locales = allowed_locales
        self.default_locale = default_locale
        self.resource_ids = resource_ids
        self.loader = FluentResourceLoader(roots=roots)
        self.locales = self._create_bundles()

    def _create_bundles(self) -> dict[str, FluentBundle]:
        locales = {}
        for locale in self.allowed_locales:
            if locale not in self.resource_ids:
                raise ValueError(f"resources for {locale=} not provided")

            locales[locale] = FluentBundle(locales=[locale])
            for resources in self.loader.resources(locale=locale, resource_ids=self.resource_ids.get(locale)):
                for resource in resources:
                    locales[locale].add_resource(resource=resource)

        return locales

    def _resolve_locale(self, locale: str = None) -> str:
        """
        Resolve the locale based on the provided parameters.

        :param locale: The locale to use.
        :type locale: str
        :return: The resolved locale.
        :rtype: str
        """
        if locale is None:
            locale = self.default_locale

        if locale not in self.allowed_locales:
            logger.debug(f"{locale=} not supported, using default locale '{self.default_locale}'")
            locale = self.default_locale

        return locale

    @classmethod
    def find_pattern(cls, msg_id: str, bundle: FluentBundle) -> Union[Pattern, str]:
        """
        Find a pattern in the Fluent bundle.

        :param msg_id: The message ID.
        :type msg_id: str
        :param bundle: The Fluent bundle.
        :type bundle: FluentBundle
        :return: The resolved pattern or the original message ID.
        :rtype: str
        """
        parts = msg_id.split(".")
        if len(parts) > 2:
            raise ValueError(f"'{msg_id=}' has too many parts")

        if not bundle.has_message(parts[0]):
            return msg_id

        msg = bundle.get_message(parts[0])
        if len(parts) == 1:
            return msg.value

        if parts[1] in msg.attributes:
            return msg.attributes.get(parts[1])

        return msg_id

    def gettext(self, msg_id: str, args: dict[str, Any] = None, locale: str = None) -> str:
        """
        Retrieve a localized message.

        :param msg_id: The message ID.
        :type msg_id: str
        :param args: Arguments for message formatting.
        :type args: dict[str, Any]
        :param locale: The locale to use.
        :type locale: str
        :return: The localized message.
        :rtype: str
        """
        locale = self._resolve_locale(locale=locale)
        bundle = self.locales.get(locale)
        pattern = self.find_pattern(msg_id=msg_id, bundle=bundle)

        if isinstance(pattern, str):
            return pattern

        msg, errors = bundle.format_pattern(pattern=pattern, args=args)
        if errors:
            logger.error(f"Error getting pattern with {errors=}")
            return msg_id

        return msg


localization = Localization()
setup_localization = localization.setup
