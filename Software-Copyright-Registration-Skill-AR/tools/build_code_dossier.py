#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php", ".cs", ".rs", ".kt", ".swift", ".sql"}


def build_dossier(project: Path) -> dict:
    entries = []
    for path in project.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in CODE_EXTS:
            continue
        rel = path.relative_to(project).as_posix()
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            lines = []
        entries.append({"path": rel, "lines": len(lines)})
    entries.sort(key=lambda item: (-item["lines"], item["path"]))
    return {"project_root": str(project), "files": entries[:60]}


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Dossier de codigo",
        "",
        f"- Proyecto: `{data['project_root']}`",
        "",
        "## Archivos sugeridos",
        "",
    ]
    for item in data["files"]:
        lines.append(f"- `{item['path']}` -> {item['lines']} lineas")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--scan", required=False)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_dossier(Path(args.project).resolve())
    (out_dir / "DossierCodigoDNDA.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "DossierCodigoDNDA.md", data)


if __name__ == "__main__":
    main()
