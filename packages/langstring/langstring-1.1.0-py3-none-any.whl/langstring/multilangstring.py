"""This module defines the `MultiLangString` class for handling multilingual text strings."""
import warnings
from typing import Any
from typing import Optional

from loguru import logger

from .langstring import LangString


class MultiLangString:
    """MultiLangString class for handling multilingual text strings.

    This class allows the management of multilingual text strings with different language tags.
    Depending on the specified control strategy, the behavior when encountering duplicate language tags can differ.
    The default behavior (using "ALLOW") prevents the addition of duplicate texts for the same language.
    That is, even if multiple identical `LangString` objects with the same text and language are added to
    a `MultiLangString`, the text for that language will not be duplicated in the internal representation.

    :ivar control: The control strategy for handling duplicate language tags.
    :vartype control: str
    :ivar langstrings: A dictionary of LangStrings indexed by language tag.
    :vartype langstrings: dict[str,list[str]]
    :ivar preferred_lang: The preferred language for this MultiLangString.
    :vartype preferred_lang: str

    Valid control strategies are:
        OVERWRITE: Overwrite existing entries with the same language tag.
        ALLOW: Allow multiple entries with the same language tag but prevent duplication of identical texts.
        BLOCK_WARN: Block and log a warning for duplicate language tags.
        BLOCK_ERROR: Block and raise an error for duplicate language tags.

    Example:
        If you have a `MultiLangString` initialized with control="ALLOW" and add two identical
        `LangString` objects (e.g., LangString("Hello", "en") twice), the internal representation
        will only have one "'Hello'@en".
    """

    MULTIPLE_ENTRIES_CONTROLS = ("OVERWRITE", "ALLOW", "BLOCK_WARN", "BLOCK_ERROR")
    """ Valid values are:
        OVERWRITE: Overwrite existing entries with the same language tag.
        ALLOW: Allow multiple entries with the same language tag.
        BLOCK_WARN: Block and log a warning for duplicate language tags.
        BLOCK_ERROR: Block and raise an error for duplicate language tags.
    """

    def _validate_langstring_arg(self, arg: Any) -> None:
        """Private helper method to validate if the argument is a LangString.

        :param arg: Argument to be checked.
        :raises TypeError: If the passed argument is not an instance of LangString.
        """
        if not isinstance(arg, LangString):
            raise TypeError(
                f"MultiLangString received invalid argument. Expected a LangString but "
                f"received '{type(arg).__name__}' with value '{arg}'."
            )

    def __init__(self, *args: LangString, control: str = "ALLOW", preferred_lang: str = "en"):
        """Initialize a new MultiLangString object.

        :param control: The control strategy for handling duplicate language tags, defaults to "ALLOW".
        :type control: str, optional
        :param preferred_lang: The preferred language for this MultiLangString, defaults to "en".
        :type preferred_lang: str, optional
        :param args: LangString objects to initialize the MultiLangString with.
        :type args: LangString
        """
        self._control: str = "ALLOW"  # Used getter and setter. Default value is "ALLOW".
        self._preferred_lang: Optional[str] = None  # Used getter and setter

        self.langstrings: dict[str, list[str]] = {}  # Initialize self.langstrings here

        self.control: str = control  # Used setter to validate
        self.preferred_lang: str = preferred_lang  # Used setter to validate

        for arg in args:
            self._validate_langstring_arg(arg)
            self.add_langstring(arg)

    # Control GETTER
    @property
    def control(self) -> str:
        """Get the control strategy for handling duplicate language tags.

        :return: The control strategy as a string.
        """
        return self._control

    # Control SETTER
    @control.setter
    def control(self, control_value: str) -> None:
        """Set the control strategy for handling duplicate language tags.

        :param control_value: The control strategy as a string.
        :type control_value: str
        :raises ValueError: If control_value is not a valid control strategy.
        """
        if control_value in self.MULTIPLE_ENTRIES_CONTROLS:
            self._control = control_value
        else:
            raise ValueError(
                f"Invalid control value: {control_value}. "
                f"Valid control values are: {self.MULTIPLE_ENTRIES_CONTROLS}."
            )

    # preferred_lang GETTER
    @property
    def preferred_lang(self) -> str:
        """Get the preferred language for this MultiLangString.

        :return: The preferred language as a string.
        """
        return self._preferred_lang

    # preferred_lang SETTER
    @preferred_lang.setter
    def preferred_lang(self, preferred_lang_value: str) -> None:
        """Set the preferred language for this MultiLangString.

        :param preferred_lang_value: The preferred language as a string.
        :type preferred_lang_value: str
        :raises TypeError: If preferred_lang_value is not a string.
        """
        if isinstance(preferred_lang_value, str):
            self._preferred_lang = preferred_lang_value
        else:
            raise TypeError(f"Invalid preferred_lang type. Should be 'str', but is '{type(preferred_lang_value)}'.")

    def add_langstring(self, langstring: LangString) -> None:
        """Add a LangString to the MultiLangString.

        :param langstring: The LangString to add.
        :type langstring: LangString
        """
        self._validate_langstring_arg(langstring)  # Use the helper method

        if self.control == "BLOCK_WARN" and langstring.lang in self.langstrings:
            warn_message = f"Operation not possible, a LangString with language tag {langstring.lang} already exists."
            warnings.warn(warn_message, UserWarning)
            logger.warning(warn_message)
        elif self.control == "BLOCK_ERROR" and langstring.lang in self.langstrings:
            raise ValueError(
                f"Operation not possible, a LangString with language tag {langstring.lang} already exists."
            )
        elif self.control == "OVERWRITE":
            self.langstrings[langstring.lang] = [langstring.text]
        else:  # self.control == ALLOW
            if langstring.text not in self.langstrings.get(langstring.lang, []):
                self.langstrings.setdefault(langstring.lang, []).append(langstring.text)

    def get_langstring(self, lang: str) -> list[str]:
        """Get LangStrings for a specific language tag.

        :param lang: The language tag to retrieve LangStrings for.
        :type lang: str
        :return: List of LangStrings for the specified language tag.
        :rtype: list
        """
        if not isinstance(lang, str):
            raise TypeError(f"Expected a string but received '{type(lang).__name__}'.")
        return self.langstrings.get(lang, [])

    def get_pref_langstring(self) -> Optional[str]:
        """Get the preferred language's LangString.

        :return: The LangString for the preferred language.
        :rtype: str
        """
        return self.langstrings.get(self.preferred_lang, None)

    def remove_langstring(self, langstring: LangString) -> bool:
        """Remove a LangString from the MultiLangString.

        :param langstring: The LangString to remove.
        :type langstring: LangString
        :return: True if the LangString was removed, False otherwise.
        :rtype: bool
        """
        if not isinstance(langstring, LangString):
            raise TypeError(f"Expected a LangString but received '{type(langstring).__name__}'.")

        langstrings = self.langstrings.get(langstring.lang, [])
        if langstring.text in langstrings:
            langstrings.remove(langstring.text)
            if not langstrings:
                del self.langstrings[langstring.lang]
            return True
        return False

    def remove_language(self, language_code: str) -> bool:
        """Remove all LangStrings associated with a specific language code.

        This method attempts to remove all LangStrings that match the given language code. If the
        language code is found and entries are removed, the method returns `True`. If the language
        code isn't found, the method returns `False`. For invalid language_code formats, a
        `ValueError` is raised.

        :param str language_code: The language code (e.g., "en", "fr") for which to remove LangStrings.
        :return: True if the language entries were removed, False otherwise.
        :rtype: bool
        :raises ValueError: If the provided language_code isn't valid or contains non-alphabetical chars.
        """
        # Handling of Invalid Language Formats
        if not isinstance(language_code, str):
            raise TypeError(f"Invalid language format. Expected alphabetic string and received '{language_code}'.")

        if not language_code:
            raise TypeError(
                "Invalid language format. Expected non-empty alphabetic string and received an empty string."
            )

        if not language_code.isalpha():
            raise TypeError(f"Invalid language format. Expected alphabetic string and received '{language_code}'.")

        # Ensure case insensitivity
        language_code = language_code.lower()

        # Check if the language exists
        if language_code in self.langstrings:
            del self.langstrings[language_code]
            return True

        # If language was not found
        return False

    def to_string(self) -> str:
        """Convert the MultiLangString to a string. Syntactical sugar for self.__str()__.

        :return: The string representation of the MultiLangString.
        :rtype: str
        """
        return self.__str__()

    def to_string_list(self) -> list[str]:
        """Convert the MultiLangString to a list of strings.

        :return: List of strings representing the MultiLangString.
        :rtype: list
        """
        return [
            f"{repr(langstring)}@{lang}" for lang, langstrings in self.langstrings.items() for langstring in langstrings
        ]

    def __repr__(self) -> str:
        """Return a string representation of the MultiLangString object.

        :return: A string representation of the MultiLangString.
        :rtype: str
        """
        if not isinstance(self.langstrings, dict):
            raise TypeError("langstrings must be a dictionary.")

        return f"MultiLangString({self.langstrings}, control='{self.control}', preferred_lang='{self.preferred_lang}')"

    def __len__(self) -> int:
        """Return the total number of LangStrings stored in the MultiLangString.

        :return: The total number of LangStrings.
        :rtype: int
        """
        return sum(len(langstrings) for langstrings in self.langstrings.values())

    def __str__(self) -> str:
        """Return a string representation of the MultiLangString, including language tags.

        :return: A string representation of the MultiLangString with language tags.
        :rtype: str
        """
        return ", ".join(
            f"{repr(langstring)}@{lang}" for lang, langstrings in self.langstrings.items() for langstring in langstrings
        )

    def __eq__(self, other: object) -> bool:
        """
        Check equality of this MultiLangString with another MultiLangString.

        This method compares only the 'langstrings' attribute of the two MultiLangString objects.
        The 'control' and 'preferred_lang' attributes, which dictate the behavior for handling duplicate language tags
        and the preferred language, are not considered in this comparison. This design decision is based on the premise
        that two MultiLangString objects are considered equal if they contain the same multilingual content,
        irrespective of their internal handling of duplicates and preferred language.

        :param other: Another MultiLangString object to compare with.
        :type other: MultiLangString
        :return: True if both MultiLangString objects have the same content, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, MultiLangString):
            return False
        return self.langstrings == other.langstrings

    def __hash__(self) -> int:
        """
        Generate a hash value for a MultiLangString object.

        The hash is computed based on the 'langstrings' attribute of the MultiLangString.
        The 'control' and 'preferred_lang' attributes are not included in the hash calculation. This ensures
        that the hash value reflects only the content of the MultiLangString, aligning with the
        equality comparison logic. This approach guarantees that MultiLangString objects with the same content
        will have the same hash value, even if they differ in their duplicate handling strategy and preferred language.

        :return: The hash value of the MultiLangString object.
        :rtype: int
        """
        # Creating a frozenset for the dictionary items to ensure the hash is independent of order
        langstrings_hash = hash(frozenset((lang, frozenset(texts)) for lang, texts in self.langstrings.items()))
        return hash(langstrings_hash)
