#!/usr/bin/env python3
"""Validate a spec file against the 'Ready for Development' standard.

Performs deterministic structural checks that don't require LLM judgment:
- All required sections present and non-empty
- Frontmatter fields populated
- AC in Given/When/Then format
- Tasks have file paths
- No TBD/TODO/placeholder text
- files_to_modify coverage in tasks

Usage:
    python3 validate-readiness.py <spec-file> [--json]

Returns exit code 0 if all checks pass, 1 if any fail.
"""

# /// script
# requires-python = ">=3.9"
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "WHY",
    "WHAT —",
    "WHAT NOT",
    "HOW",
    "RISKS",
    "VERIFY",
    "Codebase Context",
    "Implementation Plan",
    "Commands",
]

PLACEHOLDER_PATTERNS = [
    r"\bTBD\b",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"<!--\s*[^>]*-->",  # HTML comments (template placeholders)
    r"\bà définir\b",
    r"\bto be determined\b",
    r"\bplaceholder\b",
]

REQUIRED_FRONTMATTER = [
    "slug",
    "title",
    "status",
    "author",
    "tech_stack",
    "files_to_modify",
    "appetite",
]


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as a simple dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")
            if value == "[]":
                result[key] = []
            elif value.startswith("["):
                # Simple array parsing
                items = value.strip("[]").split(",")
                result[key] = [i.strip().strip("'\"") for i in items if i.strip()]
            else:
                result[key] = value
    return result


def get_body(content: str) -> str:
    """Get content after frontmatter."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:]


def find_sections(body: str) -> dict[str, str]:
    """Find H2 sections and their content."""
    sections = {}
    current_header = None
    current_content = []

    for line in body.split("\n"):
        if line.startswith("## "):
            if current_header:
                sections[current_header] = "\n".join(current_content).strip()
            current_header = line[3:].strip()
            current_content = []
        elif current_header:
            current_content.append(line)

    if current_header:
        sections[current_header] = "\n".join(current_content).strip()

    return sections


def check_section_present(sections: dict[str, str], required: str) -> bool:
    """Check if a required section exists and has non-template content."""
    for header, content in sections.items():
        if required.lower() in header.lower():
            # Remove HTML comments and check if real content exists
            cleaned = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
            # Remove sub-headers and horizontal rules
            cleaned = re.sub(r"^###.*$", "", cleaned, flags=re.MULTILINE).strip()
            cleaned = re.sub(r"^---$", "", cleaned, flags=re.MULTILINE).strip()
            return len(cleaned) > 10
    return False


def check_given_when_then(body: str) -> tuple[int, int]:
    """Count AC entries and how many use Given/When/Then format."""
    ac_pattern = re.compile(r"\*\*AC-?\d+", re.IGNORECASE)
    gwt_pattern = re.compile(r"\*\*Given\*\*.*\*\*When\*\*.*\*\*Then\*\*", re.DOTALL | re.IGNORECASE)

    ac_count = len(ac_pattern.findall(body))
    # Also count Given blocks as AC even without AC-N prefix
    given_count = len(re.findall(r"\*\*Given\*\*", body, re.IGNORECASE))
    total_ac = max(ac_count, given_count)

    gwt_count = 0
    # Split by AC markers or Given markers
    chunks = re.split(r"(?=\*\*(?:AC-?\d+|Given\*\*))", body, flags=re.IGNORECASE)
    for chunk in chunks:
        if re.search(r"\*\*Given\*\*", chunk, re.IGNORECASE) and \
           re.search(r"\*\*When\*\*", chunk, re.IGNORECASE) and \
           re.search(r"\*\*Then\*\*", chunk, re.IGNORECASE):
            gwt_count += 1

    return total_ac, gwt_count


def check_tasks_have_files(body: str) -> tuple[int, int]:
    """Count tasks and how many reference file paths."""
    task_pattern = re.compile(r"(?:^|\n)\s*-\s*\[[ x]\]\s*\*\*Task", re.IGNORECASE)
    tasks = task_pattern.findall(body)
    task_count = len(tasks)

    # Check for file paths in task blocks
    file_ref_pattern = re.compile(r"`[^\s`]+\.[a-zA-Z]+`")
    task_blocks = re.split(r"(?=\s*-\s*\[[ x]\]\s*\*\*Task)", body, flags=re.IGNORECASE)
    tasks_with_files = sum(1 for block in task_blocks if file_ref_pattern.search(block))

    return task_count, tasks_with_files


def check_placeholders(body: str) -> list[tuple[int, str]]:
    """Find placeholder text, return list of (line_number, match)."""
    findings = []
    for i, line in enumerate(body.split("\n"), 1):
        for pattern in PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                findings.append((i, match))
    return findings


def check_files_coverage(fm: dict, body: str) -> tuple[int, int]:
    """Check if files_to_modify entries appear in tasks."""
    files = fm.get("files_to_modify", [])
    if isinstance(files, str):
        files = [files] if files else []

    covered = 0
    for f in files:
        if isinstance(f, str) and f in body:
            covered += 1

    return len(files), covered


def validate(spec_path: str) -> dict:
    """Run all validation checks and return structured results."""
    path = Path(spec_path)
    if not path.exists():
        return {"error": f"File not found: {spec_path}", "passed": False}

    content = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    body = get_body(content)
    sections = find_sections(body)

    findings = []

    # 1. Frontmatter checks
    for field in REQUIRED_FRONTMATTER:
        value = fm.get(field, "")
        if not value or value == "[]":
            findings.append({
                "criterion": "complete",
                "severity": "high",
                "check": f"Frontmatter field '{field}' is empty",
                "fix": f"Set '{field}' in frontmatter",
            })

    # 2. Required sections present and non-empty
    for section in REQUIRED_SECTIONS:
        if not check_section_present(sections, section):
            findings.append({
                "criterion": "complete",
                "severity": "critical",
                "check": f"Section '{section}' is missing or empty (only template placeholders)",
                "fix": f"Fill in the '{section}' section with concrete content",
            })

    # 3. AC format check
    ac_total, gwt_count = check_given_when_then(body)
    if ac_total == 0:
        findings.append({
            "criterion": "testable",
            "severity": "critical",
            "check": "No acceptance criteria found",
            "fix": "Add Given/When/Then acceptance criteria in the VERIFY section",
        })
    elif gwt_count < ac_total:
        findings.append({
            "criterion": "testable",
            "severity": "high",
            "check": f"{ac_total - gwt_count} of {ac_total} AC entries don't use Given/When/Then format",
            "fix": "Rewrite AC entries to use Given/When/Then format",
        })

    # 4. Tasks have file paths
    task_count, tasks_with_files = check_tasks_have_files(body)
    if task_count == 0:
        findings.append({
            "criterion": "actionable",
            "severity": "critical",
            "check": "No implementation tasks found",
            "fix": "Add ordered tasks with file paths in the Implementation Plan section",
        })
    elif tasks_with_files < task_count:
        findings.append({
            "criterion": "actionable",
            "severity": "high",
            "check": f"{task_count - tasks_with_files} of {task_count} tasks don't reference file paths",
            "fix": "Add specific file paths to each task",
        })

    # 5. Placeholder check
    placeholders = check_placeholders(body)
    if placeholders:
        findings.append({
            "criterion": "complete",
            "severity": "high",
            "check": f"Found {len(placeholders)} placeholder(s): {', '.join(m for _, m in placeholders[:5])}",
            "fix": "Replace all placeholders with concrete content",
            "locations": [{"line": ln, "text": m} for ln, m in placeholders],
        })

    # 6. Files coverage
    files_total, files_covered = check_files_coverage(fm, body)
    if files_total > 0 and files_covered < files_total:
        findings.append({
            "criterion": "actionable",
            "severity": "medium",
            "check": f"{files_total - files_covered} of {files_total} files_to_modify entries not referenced in tasks",
            "fix": "Ensure every file in files_to_modify appears in at least one task",
        })

    # 7. Self-contained checks
    see_refs = re.findall(r"(?:see|voir)\s+(?:the|le|la)\s+\w+\s+(?:for|pour)", body, re.IGNORECASE)
    if see_refs:
        findings.append({
            "criterion": "self-contained",
            "severity": "medium",
            "check": f"Found {len(see_refs)} external reference(s) — spec should be self-contained",
            "fix": "Inline all referenced content into the spec",
        })

    # 8. Alternatives check
    alt_section = False
    for header in sections:
        if "alternative" in header.lower():
            content_text = sections[header]
            cleaned = re.sub(r"<!--.*?-->", "", content_text, flags=re.DOTALL).strip()
            if len(cleaned) > 20:
                alt_section = True
    if not alt_section:
        findings.append({
            "criterion": "complete",
            "severity": "medium",
            "check": "No alternatives documented in HOW section",
            "fix": "Document at least one rejected alternative with reason",
        })

    passed = all(f["severity"] not in ("critical", "high") for f in findings)

    return {
        "passed": passed,
        "spec_file": str(spec_path),
        "stats": {
            "sections_filled": sum(1 for s in REQUIRED_SECTIONS if check_section_present(sections, s)),
            "sections_required": len(REQUIRED_SECTIONS),
            "ac_count": ac_total,
            "ac_gwt_format": gwt_count,
            "task_count": task_count,
            "tasks_with_files": tasks_with_files,
            "files_to_modify": files_total,
            "files_covered_in_tasks": files_covered,
            "placeholders_found": len(placeholders),
        },
        "findings": findings,
        "criteria_summary": {
            "actionable": all(f["criterion"] != "actionable" or f["severity"] not in ("critical", "high") for f in findings),
            "logical": True,  # DAG validation requires semantic understanding — left to LLM
            "testable": all(f["criterion"] != "testable" or f["severity"] not in ("critical", "high") for f in findings),
            "complete": all(f["criterion"] != "complete" or f["severity"] not in ("critical", "high") for f in findings),
            "self_contained": all(f["criterion"] != "self-contained" or f["severity"] not in ("critical", "high") for f in findings),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Validate spec readiness for development")
    parser.add_argument("spec_file", help="Path to the spec markdown file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = validate(args.spec_file)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"ERROR: {result['error']}")
            sys.exit(2)

        stats = result["stats"]
        print(f"Spec: {result['spec_file']}")
        print(f"Sections: {stats['sections_filled']}/{stats['sections_required']}")
        print(f"Tasks: {stats['task_count']} ({stats['tasks_with_files']} with file paths)")
        print(f"AC: {stats['ac_count']} ({stats['ac_gwt_format']} in Given/When/Then)")
        print(f"Placeholders: {stats['placeholders_found']}")
        print()

        criteria = result["criteria_summary"]
        for name, passed in criteria.items():
            icon = "PASS" if passed else "FAIL"
            print(f"  [{icon}] {name}")

        if result["findings"]:
            print(f"\nFindings ({len(result['findings'])}):")
            for f in result["findings"]:
                print(f"  [{f['severity'].upper()}] {f['check']}")
                print(f"    Fix: {f['fix']}")

        print(f"\nResult: {'READY' if result['passed'] else 'NOT READY'}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
