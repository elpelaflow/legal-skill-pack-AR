#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path

TEXT_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php", ".cs", ".rs", ".kt", ".swift", ".sql", ".md"}
KEYWORDS = {
    "algoritmos": ["algorithm", "heuristic", "ranking", "optimizer"],
    "ia_datos": ["model", "inference", "dataset", "embedding", "machine learning"],
    "seguridad": ["auth", "oauth", "jwt", "encrypt", "security"],
    "orquestacion": ["workflow", "scheduler", "queue", "pipeline", "state machine"],
    "infraestructura": ["docker", "kubernetes", "terraform", "deploy"],
}


def scan(root: Path) -> dict:
    findings = []
    counts = Counter()
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_EXTS:
            continue
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            content = ""
        labels = [label for label, words in KEYWORDS.items() if any(word in content or word in rel.lower() for word in words)]
        for label in labels:
            counts[label] += 1
        if labels and len(findings) < 100:
            findings.append({"path": rel, "signals": labels})
    return {"project_root": str(root), "signal_counts": dict(counts), "findings": findings}


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Analisis del proyecto",
        "",
        f"- Proyecto: `{data['project_root']}`",
        "",
        "## Senales",
        "",
    ]
    for key, value in sorted(data["signal_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Hallazgos", ""])
    for item in data["findings"]:
        lines.append(f"- `{item['path']}` -> {', '.join(item['signals'])}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = scan(Path(args.project).resolve())
    (out_dir / "AnalisisProyectoPatente.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "AnalisisProyectoPatente.md", data)


if __name__ == "__main__":
    main()
