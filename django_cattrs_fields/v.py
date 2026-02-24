from typing import Callable, overload

from cattrs.v import format_exception
from cattrs import (
    transform_error as _transform_error,
    ClassValidationError,
    IterableValidationError,
)


@overload
def transform_error(
    exc: ClassValidationError | IterableValidationError | BaseException,
    path: str = "",
    format_exception: Callable[[BaseException, type | None], str] = format_exception,
    err_list=False,
) -> dict[str, str]: ...
@overload
def transform_error(
    exc: ClassValidationError | IterableValidationError | BaseException,
    path: str = "",
    format_exception: Callable[[BaseException, type | None], str] = format_exception,
    err_list=True,
) -> list[str]: ...
def transform_error(
    exc: ClassValidationError | IterableValidationError | BaseException,
    path: str = "",
    format_exception: Callable[[BaseException, type | None], str] = format_exception,
    err_list=False,
) -> dict[str, str] | list[str]:
    if err_list:
        return _transform_error(exc=exc, path=path, format_exception=format_exception)

    errors = {}

    if isinstance(exc, IterableValidationError):
        with_notes, without = exc.group_exceptions()

        for exc, note in with_notes:
            p = f"{path}[{note.index!r}]" if path else f"[{note.index!r}]"
            if isinstance(exc, (ClassValidationError, IterableValidationError)):
                errors.update(transform_error(exc, p, format_exception, err_list=False))
            else:
                errors[p] = format_exception(exc, note.type)

        for i, exc in enumerate(without):
            errors[f"{path if path else '$'}#{i}"] = format_exception(exc, None)

    elif isinstance(exc, ClassValidationError):
        with_note, without = exc.group_exceptions()
        for exc, note in with_note:
            p = f"{path}.{note.name}" if path else f"{note.name}"
            if isinstance(exc, (ClassValidationError, IterableValidationError)):
                errors.update(transform_error(exc, p, format_exception, err_list=False))
            else:
                errors[p] = format_exception(exc, note.type)

        for i, exc in enumerate(without):
            errors[f"{path if path else '$'}#{i}"] = format_exception(exc, None)

    else:
        errors[path if path else "$"] = format_exception(exc, None)

    return errors
