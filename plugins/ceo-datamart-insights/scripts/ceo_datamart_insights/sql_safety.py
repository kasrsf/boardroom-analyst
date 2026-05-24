from __future__ import annotations

import re


class UnsafeSqlError(ValueError):
    """Raised when SQL is outside the pack's read-only query policy."""


MUTATING_KEYWORDS = {
    "ALTER",
    "ATTACH",
    "CALL",
    "COPY",
    "CREATE",
    "DELETE",
    "DETACH",
    "DROP",
    "EXPORT",
    "IMPORT",
    "INSERT",
    "INSTALL",
    "LOAD",
    "MERGE",
    "PRAGMA",
    "SET",
    "TRUNCATE",
    "UPDATE",
    "VACUUM",
}

READ_ONLY_STARTERS = {"SELECT", "WITH", "VALUES"}


def validate_read_only_sql(sql: str) -> str:
    """Return normalized SQL when it is a single read-only statement.

    The policy is intentionally narrow. CEO insight skills should answer from
    documented data, not mutate local state or load external extensions.
    """

    if not isinstance(sql, str):
        raise UnsafeSqlError("SQL must be a string.")

    normalized = sql.strip()
    if not normalized:
        raise UnsafeSqlError("SQL is empty.")

    masked = _mask_literals_and_comments(normalized)
    masked_stripped = masked.strip()

    if masked_stripped.endswith(";"):
        before_trailing = masked_stripped[:-1]
        if ";" in before_trailing:
            raise UnsafeSqlError("Multiple SQL statements are not allowed.")
        normalized = normalized[:-1].strip()
        masked_stripped = before_trailing.strip()
    elif ";" in masked_stripped:
        raise UnsafeSqlError("Multiple SQL statements are not allowed.")

    first_token = _first_keyword(masked_stripped)
    if first_token not in READ_ONLY_STARTERS:
        raise UnsafeSqlError(
            f"Only read-only SELECT/WITH/VALUES statements are allowed, got {first_token or 'nothing'}."
        )

    upper_sql = masked_stripped.upper()
    for keyword in sorted(MUTATING_KEYWORDS):
        if re.search(rf"\b{re.escape(keyword)}\b", upper_sql):
            raise UnsafeSqlError(f"Keyword {keyword} is not allowed in read-only analysis SQL.")

    return normalized


def _first_keyword(masked_sql: str) -> str | None:
    match = re.search(r"[A-Za-z_][A-Za-z0-9_]*", masked_sql)
    if not match:
        return None
    return match.group(0).upper()


def _mask_literals_and_comments(sql: str) -> str:
    chars: list[str] = []
    i = 0
    in_single = False
    in_double = False
    in_line_comment = False
    in_block_comment = False

    while i < len(sql):
        current = sql[i]
        next_char = sql[i + 1] if i + 1 < len(sql) else ""

        if in_line_comment:
            if current == "\n":
                in_line_comment = False
                chars.append("\n")
            else:
                chars.append(" ")
            i += 1
            continue

        if in_block_comment:
            if current == "*" and next_char == "/":
                chars.extend([" ", " "])
                in_block_comment = False
                i += 2
            else:
                chars.append("\n" if current == "\n" else " ")
                i += 1
            continue

        if in_single:
            chars.append(" ")
            if current == "'" and next_char == "'":
                chars.append(" ")
                i += 2
                continue
            if current == "'":
                in_single = False
            i += 1
            continue

        if in_double:
            chars.append(" ")
            if current == '"' and next_char == '"':
                chars.append(" ")
                i += 2
                continue
            if current == '"':
                in_double = False
            i += 1
            continue

        if current == "-" and next_char == "-":
            chars.extend([" ", " "])
            in_line_comment = True
            i += 2
            continue

        if current == "/" and next_char == "*":
            chars.extend([" ", " "])
            in_block_comment = True
            i += 2
            continue

        if current == "'":
            chars.append(" ")
            in_single = True
            i += 1
            continue

        if current == '"':
            chars.append(" ")
            in_double = True
            i += 1
            continue

        chars.append(current)
        i += 1

    return "".join(chars)
