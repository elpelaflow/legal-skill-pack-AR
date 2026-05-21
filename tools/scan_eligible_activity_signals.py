#!/usr/bin/env python3
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php", ".cs",
    ".rs", ".kt", ".swift", ".sql", ".md", ".json", ".yaml", ".yml", ".toml",
    ".tf", ".sh", ".dockerfile", ".env", ".txt",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".sql": "SQL",
    ".tf": "Terraform",
    ".sh": "Shell",
}

FRAMEWORK_RULES = {
    "React": ["react", "next", "vite"],
    "Node.js": ["express", "fastify", "nest", "node:"],
    "Python Web": ["django", "flask", "fastapi"],
    "Cloud": ["terraform", "cloudformation", "kubernetes", "docker", "helm"],
    "Data/AI": ["pandas", "numpy", "scikit", "sklearn", "tensorflow", "torch", "openai"],
    "CI/CD": ["github/workflows", "gitlab-ci", "circleci", "dockerfile"],
}

ACTIVITY_RULES = {
    "desarrollo_software": {
        "keywords": ["api", "backend", "frontend", "saas", "servicio", "microservice", "sdk"],
        "frameworks": ["React", "Node.js", "Python Web"],
        "description": "Desarrollo de software y servicios informaticos."
    },
    "cloud_automatizacion": {
        "keywords": ["terraform", "docker", "kubernetes", "deploy", "iac", "pipeline"],
        "frameworks": ["Cloud", "CI/CD"],
        "description": "Infraestructura programable, despliegue y automatizacion."
    },
    "ia_datos": {
        "keywords": ["model", "inference", "analytics", "machine learning", "dataset", "embedding"],
        "frameworks": ["Data/AI"],
        "description": "Soluciones de IA, datos y analitica avanzada."
    },
    "ciberseguridad": {
        "keywords": ["auth", "oauth", "jwt", "encrypt", "security", "audit"],
        "frameworks": [],
        "description": "Controles de identidad, seguridad y trazabilidad."
    },
}


def looks_textual(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    return path.name.lower() == "dockerfile"


def scan_project(project_root: Path) -> dict:
    language_counts = Counter()
    frameworks = Counter()
    keyword_hits = defaultdict(list)
    file_samples = defaultdict(list)
    total_files = 0

    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        total_files += 1

        extension = path.suffix.lower()
        language = LANGUAGE_BY_EXTENSION.get(extension)
        if language:
            language_counts[language] += 1

        if not looks_textual(path):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue

        relative = str(path.relative_to(project_root))
        for framework, needles in FRAMEWORK_RULES.items():
            if any(needle in content or needle in relative.lower() for needle in needles):
                frameworks[framework] += 1
                if len(file_samples[framework]) < 5:
                    file_samples[framework].append(relative)

        if extension == ".tf":
            frameworks["Cloud"] += 1
            if len(file_samples["Cloud"]) < 5:
                file_samples["Cloud"].append(relative)
        if ".github/workflows/" in relative.lower():
            frameworks["CI/CD"] += 1
            if len(file_samples["CI/CD"]) < 5:
                file_samples["CI/CD"].append(relative)

        for activity, rule in ACTIVITY_RULES.items():
            for keyword in rule["keywords"]:
                if keyword in content or keyword in relative.lower():
                    if len(keyword_hits[activity]) < 8:
                        keyword_hits[activity].append(f"{keyword} -> {relative}")

    activities = []
    framework_names = set(frameworks)
    for activity, rule in ACTIVITY_RULES.items():
        score = len(keyword_hits[activity])
        score += sum(1 for name in rule["frameworks"] if name in framework_names)
        if score == 0:
            continue
        strength = "alta" if score >= 5 else "media" if score >= 3 else "baja"
        activities.append({
            "activity": activity,
            "description": rule["description"],
            "score": score,
            "strength": strength,
            "evidence": keyword_hits[activity][:8],
        })

    risks = []
    if total_files < 10:
        risks.append("repositorio_pequeno_o_poco_evidente")
    if not activities:
        risks.append("sin_senales_claras_de_actividad_promovida")

    return {
        "project_root": str(project_root),
        "total_files": total_files,
        "languages": language_counts.most_common(),
        "frameworks": frameworks.most_common(),
        "activities": sorted(activities, key=lambda item: item["score"], reverse=True),
        "framework_samples": file_samples,
        "risks": risks,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Senales de actividad elegible",
        "",
        f"- Proyecto: `{data['project_root']}`",
        f"- Archivos relevados: `{data['total_files']}`",
        "",
        "## Lenguajes",
        "",
    ]
    for language, count in data["languages"] or [("Sin datos", 0)]:
        lines.append(f"- {language}: {count}")

    lines.extend(["", "## Frameworks y patrones", ""])
    for name, count in data["frameworks"] or [("Sin datos", 0)]:
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Actividades sugeridas", ""])
    if data["activities"]:
        for activity in data["activities"]:
            lines.append(f"### {activity['activity']}")
            lines.append(f"- Fuerza: {activity['strength']}")
            lines.append(f"- Puntaje: {activity['score']}")
            lines.append(f"- Sentido: {activity['description']}")
            for evidence in activity["evidence"]:
                lines.append(f"- Evidencia: {evidence}")
            lines.append("")
    else:
        lines.append("- No se detectaron actividades sugeridas.")

    lines.extend(["## Riesgos", ""])
    for risk in data["risks"] or ["sin_riesgos_detectados"]:
        lines.append(f"- {risk}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    project_root = Path(args.project).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = scan_project(project_root)
    json_path = out_dir / "SenalesActividadElegible.json"
    md_path = out_dir / "SenalesActividadElegible.md"
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(data, md_path)


if __name__ == "__main__":
    main()
