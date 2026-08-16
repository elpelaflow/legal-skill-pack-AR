#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path

TEXT_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php", ".cs", ".rs", ".kt", ".swift", ".sql"}


def scan_project(root: Path) -> dict:
    languages = Counter()
    top_dirs = Counter()
    files = []
    total_lines = 0

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.count("/") >= 1:
            top_dirs[rel.split("/")[0]] += 1
        if path.suffix.lower() in TEXT_EXTS:
            languages[path.suffix.lower()] += 1
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                content = ""
            total_lines += len(content.splitlines())
            if len(files) < 80:
                files.append(rel)

    return {
        "project_root": str(root),
        "languages": dict(languages),
        "top_directories": dict(top_dirs),
        "sample_files": files,
        "estimated_lines": total_lines,
    }


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Analisis del proyecto",
        "",
        f"- Proyecto: `{data['project_root']}`",
        f"- Lineas estimadas: `{data['estimated_lines']}`",
        "",
        "## Lenguajes",
        "",
    ]
    for key, value in sorted(data["languages"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Directorios principales", ""])
    for key, value in sorted(data["top_directories"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Archivos de muestra", ""])
    for item in data["sample_files"]:
        lines.append(f"- `{item}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = scan_project(Path(args.project).resolve())
    (out_dir / "AnalisisProyectoDNDA.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "AnalisisProyectoDNDA.md", data)


if __name__ == "__main__":
    main()
