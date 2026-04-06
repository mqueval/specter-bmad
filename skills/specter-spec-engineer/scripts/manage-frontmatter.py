#!/usr/bin/env python3
"""Manage spec file frontmatter state transitions.

Provides deterministic frontmatter operations for the spec-engineer workflow:
- Add a step to stepsCompleted
- Update status
- Read current state
- Check if a step has been completed

Usage:
    python3 manage-frontmatter.py <spec-file> status              # Show current state
    python3 manage-frontmatter.py <spec-file> complete <step>     # Mark step as completed
    python3 manage-frontmatter.py <spec-file> set-status <status> # Update status field
    python3 manage-frontmatter.py <spec-file> next-step           # Show which step is next
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

STEP_ORDER = [
    "step-01-understand",
    "step-02-investigate",
    "step-03-design",
    "step-04-plan",
    "step-05-review",
]

STATUS_MAP = {
    "step-01-understand": "investigating",
    "step-02-investigate": "designing",
    "step-03-design": "designed",
    "step-04-plan": "in-review",
    "step-05-review": "ready",
}


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def parse_steps_completed(content: str) -> list[str]:
    """Extract stepsCompleted array from frontmatter."""
    match = re.search(r"stepsCompleted:\s*\[([^\]]*)\]", content)
    if not match:
        match = re.search(r"stepsCompleted:\s*\n((?:\s*-\s*.+\n)*)", content)
        if match:
            items = re.findall(r"-\s*['\"]?([^'\"'\n]+)['\"]?", match.group(1))
            return [i.strip() for i in items if i.strip()]
        return []
    items = match.group(1)
    if not items.strip():
        return []
    return [i.strip().strip("'\"") for i in items.split(",") if i.strip()]


def update_steps_completed(content: str, steps: list[str]) -> str:
    """Update stepsCompleted in frontmatter."""
    steps_str = ", ".join(f"'{s}'" for s in steps)
    new_value = f"stepsCompleted: [{steps_str}]"

    # Try inline array format first
    if re.search(r"stepsCompleted:\s*\[", content):
        return re.sub(r"stepsCompleted:\s*\[[^\]]*\]", new_value, content)

    # Try YAML list format
    if re.search(r"stepsCompleted:\s*\n(?:\s*-\s*.+\n)*", content):
        return re.sub(
            r"stepsCompleted:\s*\n(?:\s*-\s*.+\n)*",
            new_value + "\n",
            content,
        )

    return content


def update_status(content: str, status: str) -> str:
    """Update status field in frontmatter."""
    return re.sub(
        r"status:\s*['\"]?[^'\"\n]+['\"]?",
        f"status: '{status}'",
        content,
    )


def get_current_state(content: str) -> dict:
    """Get current workflow state from frontmatter."""
    steps = parse_steps_completed(content)
    status_match = re.search(r"status:\s*['\"]?([^'\"'\n]+)", content)
    title_match = re.search(r"title:\s*['\"]?([^'\"'\n]+)", content)
    slug_match = re.search(r"slug:\s*['\"]?([^'\"'\n]+)", content)

    last_step = steps[-1] if steps else None
    next_step = None
    if last_step and last_step in STEP_ORDER:
        idx = STEP_ORDER.index(last_step)
        if idx + 1 < len(STEP_ORDER):
            next_step = STEP_ORDER[idx + 1]
    elif not steps:
        next_step = STEP_ORDER[0]

    return {
        "title": title_match.group(1).strip() if title_match else "",
        "slug": slug_match.group(1).strip() if slug_match else "",
        "status": status_match.group(1).strip() if status_match else "unknown",
        "steps_completed": steps,
        "last_step": last_step,
        "next_step": next_step,
        "is_complete": "step-05-review" in steps,
        "progress": f"{len(steps)}/5",
    }


def main():
    parser = argparse.ArgumentParser(description="Manage spec frontmatter state")
    parser.add_argument("spec_file", help="Path to the spec file")
    parser.add_argument("command", choices=["status", "complete", "set-status", "next-step"])
    parser.add_argument("value", nargs="?", help="Step name or status value")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    path = Path(args.spec_file)

    if args.command == "status":
        if not path.exists():
            result = {"exists": False, "next_step": STEP_ORDER[0]}
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"File not found: {args.spec_file}")
                print(f"Next step: {STEP_ORDER[0]}")
            sys.exit(0)

        content = read_file(path)
        state = get_current_state(content)
        if args.json:
            print(json.dumps(state, indent=2))
        else:
            print(f"Title: {state['title']}")
            print(f"Status: {state['status']}")
            print(f"Progress: {state['progress']}")
            print(f"Completed: {', '.join(state['steps_completed']) or 'none'}")
            print(f"Next step: {state['next_step'] or 'DONE'}")
            print(f"Complete: {state['is_complete']}")

    elif args.command == "complete":
        if not args.value:
            print("Error: step name required", file=sys.stderr)
            sys.exit(2)
        content = read_file(path)
        steps = parse_steps_completed(content)
        step_name = args.value
        if step_name not in steps:
            steps.append(step_name)
        content = update_steps_completed(content, steps)
        # Also update status based on step
        if step_name in STATUS_MAP:
            content = update_status(content, STATUS_MAP[step_name])
        write_file(path, content)
        if args.json:
            print(json.dumps({"completed": step_name, "steps": steps}))
        else:
            print(f"Marked '{step_name}' as completed")
            print(f"Steps: {', '.join(steps)}")

    elif args.command == "set-status":
        if not args.value:
            print("Error: status value required", file=sys.stderr)
            sys.exit(2)
        content = read_file(path)
        content = update_status(content, args.value)
        write_file(path, content)
        if args.json:
            print(json.dumps({"status": args.value}))
        else:
            print(f"Status updated to: {args.value}")

    elif args.command == "next-step":
        if not path.exists():
            result = STEP_ORDER[0]
        else:
            content = read_file(path)
            state = get_current_state(content)
            result = state["next_step"]
        if args.json:
            print(json.dumps({"next_step": result}))
        else:
            print(result or "DONE")


if __name__ == "__main__":
    main()
