from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".txt", ".ini"}
OLD_NAME = "Jubílio Filiano Mausse"
NEW_NAME = "Jubílio Filiano Maússe"


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "VERSION"}:
            yield path


def main() -> int:
    changed = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        updated = text.replace(OLD_NAME, NEW_NAME)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT))

    for path in changed:
        print(f"Updated: {path}")
    print(f"Files updated: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
