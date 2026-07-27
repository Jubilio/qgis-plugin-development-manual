"""Generate Quarto book chapters from the canonical Markdown manual.

The repository keeps one canonical source in ``manual/manual.md``. This script
splits that source into a small number of generated Quarto chapters, avoiding
content duplication while providing a navigable web book.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manual" / "manual.md"
OUTPUT = ROOT / "chapters"

PART_FILES = {
    "I": "01-fundamentos.qmd",
    "II": "02-primeiro-plugin.qmd",
    "III": "03-desenvolvimento-intermedio.qmd",
    "IV": "04-desenvolvimento-avancado.qmd",
    "V": "05-estudos-de-caso.qmd",
    "VI": "06-projecto-pratico.qmd",
}


def strip_front_matter(text: str) -> str:
    """Remove a leading YAML front matter block."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def clean_lines(text: str) -> list[str]:
    """Remove print-only markers and trailing whitespace."""
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip() in {r"\newpage", r"\pagebreak"}:
            continue
        lines.append(line)
    return lines


def chapter_relative_paths(line: str) -> str:
    """Adjust project-root resources for generated files in ``chapters/``."""
    return line.replace("](assets/", "](../assets/")


def demote_headings(lines: list[str], first_heading: str) -> str:
    """Create one valid Quarto chapter with a single level-one heading."""
    output = [f"# {first_heading}", ""]
    skipped_first = False
    for raw_line in lines:
        line = chapter_relative_paths(raw_line)
        if line == f"# {first_heading}" and not skipped_first:
            skipped_first = True
            continue
        if line.startswith("# "):
            line = "## " + line[2:]
        elif line.startswith("## "):
            line = "### " + line[3:]
        elif line.startswith("### "):
            line = "#### " + line[4:]
        output.append(line)
    return "\n".join(output).strip() + "\n"


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    """Split the canonical manual into introduction, six parts and appendices."""
    sections: dict[str, list[str]] = {"intro": [], "appendices": []}
    current = "intro"

    for line in lines:
        part_match = re.match(r"^# Parte ([IVX]+)\s*-\s*(.+)$", line)
        if part_match and part_match.group(1) in PART_FILES:
            current = part_match.group(1)
            sections[current] = [line]
            continue

        if line.startswith("# Apêndice "):
            current = "appendices"

        sections.setdefault(current, []).append(line)

    return sections


def introduction_content(lines: list[str]) -> str:
    """Keep the preface and learning roadmap, omitting the print-only index."""
    try:
        start = lines.index("# Prefácio")
    except ValueError:
        start = 0
    selected = lines[start:]
    return demote_headings(selected, "Prefácio e roteiro de aprendizagem")


def write_generated_chapters() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Canonical manual not found: {SOURCE}")

    text = strip_front_matter(SOURCE.read_text(encoding="utf-8"))
    lines = clean_lines(text)
    sections = split_sections(lines)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT.glob("*.qmd"):
        old_file.unlink()

    (OUTPUT / "00-prefacio.qmd").write_text(
        introduction_content(sections["intro"]), encoding="utf-8"
    )

    for roman, filename in PART_FILES.items():
        section_lines = sections.get(roman, [])
        if not section_lines:
            raise ValueError(f"Part {roman} was not found in {SOURCE}")
        title = section_lines[0].removeprefix("# ")
        (OUTPUT / filename).write_text(
            demote_headings(section_lines, title), encoding="utf-8"
        )

    appendices = sections.get("appendices", [])
    if appendices:
        (OUTPUT / "07-apendices.qmd").write_text(
            demote_headings(appendices, "Apêndices e referências"), encoding="utf-8"
        )


if __name__ == "__main__":
    write_generated_chapters()
