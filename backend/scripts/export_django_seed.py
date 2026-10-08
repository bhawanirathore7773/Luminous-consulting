"""
One-time migration helper.

Reads the canonical Django management-command seed data and exports portable
JSON consumed by the Prisma seed. This keeps the migration independent of a
Django runtime during Hostinger deployment.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "backend" / "prisma" / "source-data"

SOURCES = {
    "services": (ROOT / "services/management/commands/seed_services.py", ["SERVICES_DATA"]),
    "solutions": (ROOT / "solutions/management/commands/seed_solutions.py", ["SOLUTIONS_DATA"]),
    "industries": (ROOT / "industries/management/commands/seed_industries.py", ["INDUSTRIES_DATA"]),
    "case_studies": (ROOT / "case_studies/management/commands/seed_case_studies.py", ["CASE_STUDIES_DATA"]),
    "insights": (ROOT / "insights/management/commands/seed_insights.py", ["ARTICLES_DATA"]),
    "expertise": (ROOT / "sap_expertise/management/commands/seed_expertise.py", ["EXPERTISE_DATA"]),
    "legal": (ROOT / "legal/management/commands/seed_legal_pages.py", ["LEGAL_PAGES_DATA"]),
}

CONSTANTS = {
    "Article": {
        "S4HANA": "s4hana", "BTP": "btp", "INTEGRATION": "integration",
        "SECURITY": "security", "FINANCE": "finance", "SUPPLY_CHAIN": "supply_chain",
        "MANUFACTURING": "manufacturing", "DATA_ANALYTICS": "data_analytics",
        "AI": "ai", "AMS": "ams", "TRANSFORMATION": "transformation",
        "ARTICLE": "article", "GUIDE": "guide", "CHECKLIST": "checklist",
        "WHITEPAPER": "whitepaper", "IMPLEMENTATION_GUIDE": "implementation_guide",
        "MIGRATION_GUIDE": "migration_guide", "ARCHITECTURE_INSIGHT": "architecture_insight",
    },
    "ExpertiseItem": {
        "PLATFORMS": "platforms", "TECHNOLOGIES": "technologies",
        "BUSINESS_APPLICATIONS": "business_applications", "FUNCTIONAL_AREAS": "functional_areas",
    },
}

def literal(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal(x) for x in node.elts]
    if isinstance(node, ast.Dict):
        return {literal(k): literal(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -literal(node.operand)
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return CONSTANTS.get(node.value.id, {}).get(node.attr, node.attr)
    if isinstance(node, ast.Name) and node.id in {"True", "False", "None"}:
        return {"True": True, "False": False, "None": None}[node.id]
    raise ValueError(f"Unsupported seed expression: {ast.dump(node)}")

def extract(module, candidates):
    for node in module.body:
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if any(name in candidates for name in names):
                return literal(node.value)
    raise RuntimeError(f"Could not find {candidates}")

OUT.mkdir(parents=True, exist_ok=True)
for name, (path, candidates) in SOURCES.items():
    if not path.exists():
        raise SystemExit(f"Missing source seed: {path}")
    module = ast.parse(path.read_text(encoding="utf-8"))
    data = extract(module, candidates)
    (OUT / f"{name}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Exported {name}: {len(data)} records")
