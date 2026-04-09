from __future__ import annotations

import re


def refactor_source(source: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    updated = source

    stripped_lines = [line.rstrip() for line in updated.splitlines()]
    if stripped_lines != updated.splitlines():
        notes.append("Removed trailing whitespace.")
        updated = "\n".join(stripped_lines)

    if "\t" in updated:
        notes.append("Replaced tab characters with four spaces.")
        updated = updated.replace("\t", "    ")

    none_eq = re.sub(r"([A-Za-z0-9_)\]]+)\s*==\s*None", r"\1 is None", updated)
    if none_eq != updated:
        notes.append("Converted `== None` checks to `is None`.")
        updated = none_eq

    none_neq = re.sub(r"([A-Za-z0-9_)\]]+)\s*!=\s*None", r"\1 is not None", updated)
    if none_neq != updated:
        notes.append("Converted `!= None` checks to `is not None`.")
        updated = none_neq

    if updated and not updated.endswith("\n"):
        notes.append("Added a trailing newline at end of file.")
        updated = f"{updated}\n"

    if not notes:
        notes.append("No safe automatic refactor rules were applied.")

    return updated, notes
