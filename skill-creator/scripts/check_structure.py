#!/usr/bin/env python3
"""
Check skill file structure - CRITICAL checks only.

Only checks that can find real errors that would break skill functionality.
"""

import json
import sys
from pathlib import Path


def check_structure(skill_path: Path) -> dict:
    """Check skill directory structure - critical items only."""

    results = {
        "skill_path": str(skill_path),
        "checks": [],
        "score": 0,
        "max_score": 0
    }

    # CRITICAL: SKILL.md must exist
    results["max_score"] += 40
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        results["score"] += 40
        results["checks"].append({
            "name": "SKILL.md",
            "passed": True,
            "points": 40,
            "type": "critical"
        })
    else:
        results["checks"].append({
            "name": "SKILL.md",
            "passed": False,
            "points": 0,
            "type": "critical",
            "note": "CRITICAL: Skill cannot function without SKILL.md"
        })
        # Can't continue - no point checking other things
        results["percentage"] = 0
        return results

    # CRITICAL: evals/evals.json or eval_group*.json must exist
    results["max_score"] += 40
    evals_dir = skill_path / "evals"
    eval_files = []
    
    # Look for split eval group files first
    if evals_dir.exists():
        for f in evals_dir.glob("eval_group*.json"):
            eval_files.append(f)
        # Also check for original evals.json
        original_evals = evals_dir / "evals.json"
        if original_evals.exists() and original_evals not in eval_files:
            eval_files.append(original_evals)
    
    if eval_files:
        # Validate each eval file
        total_evals = 0
        valid_files = 0
        for ef in eval_files:
            try:
                data = json.loads(ef.read_text())
                count = len(data.get("evals", []))
                total_evals += count
                valid_files += 1
            except:
                pass
        
        if valid_files > 0 and total_evals >= 1:
            results["score"] += 40
            results["checks"].append({
                "name": "eval definitions",
                "passed": True,
                "points": 40,
                "type": "critical",
                "note": f"{total_evals} evals in {valid_files} file(s)"
            })
        else:
            results["checks"].append({
                "name": "eval definitions",
                "passed": False,
                "points": 0,
                "type": "critical",
                "note": "CRITICAL: Eval files exist but have no evals defined"
            })
    else:
        results["checks"].append({
            "name": "eval definitions",
            "passed": False,
            "points": 0,
            "type": "critical",
            "note": "CRITICAL: Cannot test skill without evals (need eval_group*.json or evals.json)"
        })

    # IMPORTANT: evals/ directory
    results["max_score"] += 20
    evals_dir = skill_path / "evals"
    if evals_dir.exists() and evals_dir.is_dir():
        results["score"] += 20
        results["checks"].append({
            "name": "evals/ directory",
            "passed": True,
            "points": 20,
            "type": "important"
        })
    else:
        results["checks"].append({
            "name": "evals/ directory",
            "passed": False,
            "points": 0,
            "type": "important",
            "note": "IMPORTANT: evals/ directory missing"
        })

    # Calculate percentage
    results["percentage"] = round(results["score"] / results["max_score"] * 100, 1) if results["max_score"] > 0 else 0

    return results


def print_report(results: dict):
    """Print formatted report."""
    print("\n" + "="*60)
    print("FILE STRUCTURE CHECK (Critical Only)")
    print("="*60)
    print(f"\nSkill: {results['skill_path']}")
    print(f"\nSCORE: {results['score']}/{results['max_score']} ({results['percentage']}%)")
    print("\n" + "-"*60)
    print("STRUCTURE:")
    print("-"*60)

    for check in results["checks"]:
        status = "✅" if check["passed"] else "❌"
        type_indicator = {"critical": "🔴", "important": "🟡", "optional": "🟢"}
        type_color = type_indicator.get(check.get("type", ""), "⚪")

        print(f"\n{status} {type_color} {check['name']} ({check.get('type', 'unknown')})")
        if check["passed"]:
            if "note" in check:
                print(f"   {check['note']}")
        else:
            if "note" in check:
                print(f"   ⚠️  {check['note']}")

    print("\n" + "="*60)

    if results["percentage"] >= 100:
        print("✅ PASS - All critical structure checks passed")
    elif results["percentage"] >= 80:
        print("⚠️  WARNING - Some important checks failed")
    else:
        print("❌ FAIL - Critical structure issues found")

    print(f"\nSuccess Rate: {results['percentage']}%")
    print("="*60 + "\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_structure.py <skill_directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)

    results = check_structure(skill_path)
    print_report(results)

    # Save results
    output_file = skill_path / "structure_results.json"
    output_file.write_text(json.dumps(results, indent=2))
    print(f"Results saved to: {output_file}")

    sys.exit(0 if results["percentage"] >= 80 else 1)


if __name__ == "__main__":
    main()
