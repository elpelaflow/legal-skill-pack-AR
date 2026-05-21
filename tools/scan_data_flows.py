#!/usr/bin/env python3
"""Escanear un proyecto para detectar señales de tratamiento de datos personales."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


KEYWORDS = {
    "auth": ["login", "signup", "signin", "password", "oauth", "session", "token", "user"],
    "billing": ["invoice", "billing", "payment", "card", "subscription", "checkout"],
    "support": ["ticket", "support", "helpdesk", "chat", "conversation"],
    "marketing": ["lead", "newsletter", "campaign", "crm", "hubspot", "mailchimp"],
    "analytics": ["analytics", "segment", "mixpanel", "amplitude", "tracking", "pixel", "ga4", "posthog"],
    "hr": ["employee", "candidate", "recruit", "payroll", "cv", "resume"],
    "vendors": ["stripe", "sendgrid", "twilio", "intercom", "firebase", "sentry", "datadog", "hubspot", "zendesk", "aws", "gcp", "vercel"],
    "fraud": ["kyc", "aml", "fraud", "risk", "scoring", "transaction"],
    "health": ["patient", "telemedicine", "diagnosis", "medical", "health", "clinic"],
    "surveillance": ["camera", "cctv", "video", "surveillance", "access_control", "badge"],
}

TEXT_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".md", ".yaml", ".yml", ".env", ".txt", ".sql"
}


def iter_files(project: Path):
    for path in project.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "dist", "build", ".next", "coverage", "venv"} for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTS:
            yield path


def read_limited(path: Path, limit: int = 120_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""


def analyze(project: Path) -> dict:
    findings = {key: [] for key in KEYWORDS}
    vendor_hits: dict[str, int] = {}
    files_scanned = 0
    for path in iter_files(project):
        text = read_limited(path).lower()
        if not text:
            continue
        files_scanned += 1
        rel = str(path.relative_to(project))
        for area, words in KEYWORDS.items():
            matched = [word for word in words if re.search(rf"\b{re.escape(word)}\b", text)]
            if matched:
                findings[area].append({"path": rel, "matched_terms": matched[:8]})
                if area == "vendors":
                    for word in matched:
                        vendor_hits[word] = vendor_hits.get(word, 0) + 1
    return {
        "project_root": str(project.resolve()),
        "files_scanned": files_scanned,
        "signals": findings,
        "vendor_summary": dict(sorted(vendor_hits.items(), key=lambda item: (-item[1], item[0]))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/analysis")
    args = parser.parse_args()

    project = Path(args.project)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = analyze(project)
    (out_dir / "data_flows.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK escaneo: {out_dir / 'data_flows.json'}")


if __name__ == "__main__":
    main()
