#!/usr/bin/env python3
"""Two things that made this action unusable, and nothing noticed either.

The file lived at .github/actions/terraform-output/action.yml. GitHub resolves
`uses: owner/repo@ref` only against an action.yml at the repository root, so no
one outside this repository could use it at all, and it could not be listed on
the Marketplace.

Its declared output read `steps.output.outputs.terraform-output` while the step
id was `terraform-output-action`. There is no step called `output`, so the
expression resolved to an empty string on every run. The action did its work,
printed the JSON, and handed the caller nothing. Nothing failed, which is why
it survived.

    python3 scripts/check_action.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEP_REF = re.compile(r"steps\.([A-Za-z0-9_-]+)\.outputs\.")


def main() -> int:
    problems: list[str] = []

    action = ROOT / "action.yml"
    if not action.exists():
        alt = list(ROOT.glob(".github/actions/*/action.yml"))
        problems.append(
            "action.yml is not at the repository root, so `uses: owner/repo@ref` "
            "cannot resolve it"
            + (f" (found {alt[0].relative_to(ROOT)})" if alt else "")
        )
        for line in problems:
            print(line)
        return 1

    text = action.read_text(encoding="utf-8")

    # Step ids, taken from the runs.steps list. A plain parse would need a YAML
    # library; the file is small and the shape is fixed, so a regex is enough
    # and keeps this dependency-free.
    ids = set(re.findall(r"^\s*-?\s*id:\s*([A-Za-z0-9_-]+)\s*$", text, re.M))

    # Everything the outputs block points at must be one of them.
    outputs_block = text.split("outputs:", 1)[1].split("runs:", 1)[0] if "outputs:" in text else ""
    for referenced in set(STEP_REF.findall(outputs_block)):
        if referenced not in ids:
            problems.append(
                f"outputs reference steps.{referenced}, but no step has that id. "
                f"Step ids present: {', '.join(sorted(ids)) or 'none'}. "
                "The output resolves to an empty string."
            )

    if problems:
        for line in problems:
            print(line)
        return 1

    print(f"action.yml is at the root and its outputs name real steps ({', '.join(sorted(ids))}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
