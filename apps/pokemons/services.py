import re


def change_filter_ordering(ordering: str | None, field: str) -> str:
    if ordering is None:
        ordering = field

    elif field not in ordering:
        ordering = f"{field},{ordering}"

    elif field in ordering:
        if f"-{field}" in ordering:
            new_field_ordering = field
        else:
            new_field_ordering = f"-{field}"

        ordering = re.sub(f"(-*{field},*)", "", ordering)
        ordering = f"{new_field_ordering},{ordering}".rstrip(",")

    return ordering
