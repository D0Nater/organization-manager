"""Pydantic validators."""

from re import compile as re_compile

from pydantic import AfterValidator, BeforeValidator


def not_empty(s: str) -> str:
    """Ensures the given string is not empty.

    Args:
        s (str): The input string.

    Returns:
        str: The original string if it is not empty.

    Raises:
        ValueError: If the string is empty.
    """
    if not s:
        raise ValueError("cannot be empty")
    return s


def strip(s: str) -> str:
    """Strips leading and trailing whitespace from the given string.

    Args:
        s (str): The input string.

    Returns:
        str: The stripped string.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(s, str):
        raise ValueError("must be a string")
    return s.strip()


def check_special_characters(s: str) -> str:
    """Validates that the string does not contain special characters (newline, carriage return, tab).

    Args:
        s (str): The input string.

    Returns:
        str: The original string if it contains no disallowed characters.

    Raises:
        ValueError: If the string contains any of the forbidden characters.
    """
    for i, c in enumerate(["\n", "\r", "\t"]):
        if c in s:
            raise ValueError(f"cannot contain special characters (debug: elem at index {i})")
    return s


def check_text(text: str) -> str:
    """Performs a sequence of validations on the given text (not empty, stripped, no special characters).

    Args:
        text (str): The input text.

    Returns:
        str: The validated and stripped text.

    Raises:
        ValueError: If the text is empty or contains invalid characters.
    """
    return check_special_characters(strip(not_empty(text)))


def python_regex(
    regex: str,
    flags: int = 0,
    include_regex_in_error_message: bool = True,
    limit_length: int | None = None,
) -> AfterValidator:
    """Creates a validator that enforces regex matching using Python's regex engine.

    Unlike Pydantic's Rust-based regex backend, this validator supports the full Python regex feature set
    and avoids issues with FastAPI OpenAPI schema generation.

    Args:
        regex (str): The regex pattern to validate against.
        flags (int, optional): Regex flags (e.g., re.IGNORECASE). Defaults to 0.
        include_regex_in_error_message (bool, optional): Whether to include the
            regex pattern in error messages. Defaults to True.
        limit_length (int | None, optional): Maximum allowed string length.
            If provided, string must be shorter or equal. Defaults to None.

    Returns:
        AfterValidator: A Pydantic `AfterValidator` instance enforcing the regex rule.

    Raises:
        ValueError: If the input string exceeds the length limit or does not match the regex pattern.

    Example:
        >>> RecipeName = Annotated[str, python_regex("^[a-zA-Z0-9_ -]+$")]
        >>> class Recipe(BaseModel):
        ...     name: RecipeName = Field(max_length=32)
    """
    compiled = re_compile(regex, flags)

    def python_regex_inner(s: str | None) -> str | None:
        if s is None:
            return s
        if limit_length is not None and len(s) > limit_length:
            raise ValueError(f"length must be less than or equal to {limit_length}")
        if not compiled.match(s):
            raise ValueError(
                ("does not match regex: " + regex) if include_regex_in_error_message else "does not match regex"
            )
        return s

    return AfterValidator(python_regex_inner)


NotEmptyValidator = AfterValidator(not_empty)
StripValidator = BeforeValidator(strip)
CheckSpecialCharactersValidator = AfterValidator(check_special_characters)
CheckTextValidator = BeforeValidator(check_text)
