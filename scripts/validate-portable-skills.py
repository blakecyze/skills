#!/usr/bin/env python3
"""Check that each skill carries every linked resource it needs when installed alone."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def check_links(document, boundary):
    errors = []
    # These libraries use inline Markdown links, including optional URL fragments.
    for href in re.findall(r"\]\(([^)]+)\)", document.read_text()):
        link = urlsplit(href.strip("<>"))
        if link.scheme or link.netloc or not link.path:
            continue
        target = (document.parent / unquote(link.path)).resolve()
        if not target.is_relative_to(boundary.resolve()):
            errors.append(f"{document}: link escapes install boundary: {href}")
        elif not target.exists():
            errors.append(f"{document}: missing linked resource: {href}")
    return errors


def validate(library):
    errors = []
    skills = sorted((library / "skills").glob("*/SKILL.md"))
    if not skills:
        return [f"{library}: no skills found"]
    for entry in skills:
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", entry.read_text(), re.S)
        if not match:
            errors.append(f"{entry}: missing frontmatter")
            continue
        try:
            fields = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            errors.append(f"{entry}: {error}")
            continue
        if not isinstance(fields, dict):
            errors.append(f"{entry}: frontmatter must be a mapping")
            continue
        name = fields.get("name", "")
        if name != entry.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{entry}: invalid name or directory mismatch")
        description = fields.get("description")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            errors.append(f"{entry}: description must contain 1-1024 characters")
        for document in entry.parent.rglob("*.md"):
            errors.extend(check_links(document, entry.parent))
    readme = library / "README.md"
    if readme.is_file():
        errors.extend(check_links(readme, library))
    return errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: validate-portable-skills.py LIBRARY [LIBRARY ...]")
    failures = [error for argument in sys.argv[1:] for error in validate(Path(argument))]
    if failures:
        sys.exit("\n".join(failures))
    print(f"Portable skill resources and metadata pass for {len(sys.argv) - 1} libraries")
