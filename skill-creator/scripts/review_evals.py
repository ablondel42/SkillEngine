#!/usr/bin/env python3
"""
Review eval definitions for quality and completeness.

Checks:
- Evals file exists and is valid JSON
- Each eval has required fields
- Expectations are verifiable
- Prompts are realistic
"""

import json
import sys
from pathlib import Path


def review_evals(skill_path: Path) -> dict:
    """Review eval definitions."""
    
    results = {
        "skill_path": str(skill_path),
        "evals_file": None,
        "checks": [],
        "score": 0,
        "max_score": 0
    }

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
    
    results["evals_file"] = str(eval_files) if eval_files else None

    # Check files exist
    results["max_score"] += 10
    if not eval_files:
        results["checks"].append({
            "name": "Evals files exist",
            "passed": False,
            "points": 0,
            "note": "No eval_group*.json or evals/evals.json found"
        })
        return results

    results["score"] += 10
    results["checks"].append({
        "name": "Evals files exist",
        "passed": True,
        "points": 10,
        "note": f"{len(eval_files)} eval file(s) found"
    })

    # Load and parse all eval files
    all_evals = []
    for ef in eval_files:
        try:
            data = json.loads(ef.read_text())
            if "evals" in data and isinstance(data["evals"], list):
                all_evals.extend(data["evals"])
        except json.JSONDecodeError as e:
            results["checks"].append({
                "name": f"Valid JSON: {ef.name}",
                "passed": False,
                "points": 0,
                "note": str(e)
            })
    
    # Check structure
    results["max_score"] += 10
    if all_evals:
        results["score"] += 10
        results["checks"].append({
            "name": "Valid structure",
            "passed": True,
            "points": 10,
            "eval_count": len(all_evals)
        })
    else:
        results["checks"].append({
            "name": "Valid structure",
            "passed": False,
            "points": 0,
            "note": "Missing 'evals' array"
        })
        return results

    # Review each eval
    for i, eval_item in enumerate(all_evals):
        eval_results = review_single_eval(eval_item, i)
        results["checks"].extend(eval_results["checks"])
        results["score"] += eval_results["score"]
        results["max_score"] += eval_results["max_score"]

    # Calculate percentage
    results["percentage"] = round(results["score"] / results["max_score"] * 100, 1) if results["max_score"] > 0 else 0

    return results


def review_single_eval(eval_item: dict, index: int) -> dict:
    """Review a single eval definition."""

    results = {
        "eval_index": index,
        "checks": [],
        "score": 0,
        "max_score": 0
    }

    eval_name = eval_item.get("eval_name", f"eval-{index}")

    # Check required fields
    required = ["id", "prompt", "expected_output"]
    results["max_score"] += len(required) * 5

    for field in required:
        if field in eval_item and eval_item[field]:
            results["score"] += 5
            results["checks"].append({
                "name": f"{eval_name}: {field}",
                "passed": True,
                "points": 5
            })
        else:
            results["checks"].append({
                "name": f"{eval_name}: {field}",
                "passed": False,
                "points": 0,
                "note": "Missing or empty"
            })

    # Check expectations exist and are testable
    results["max_score"] += 20
    if "expectations" not in eval_item or len(eval_item["expectations"]) == 0:
        results["checks"].append({
            "name": f"{eval_name}: expectations",
            "passed": False,
            "points": 0,
            "note": "No expectations defined - cannot grade output"
        })
    else:
        expectations = eval_item["expectations"]
        
        # Check if expectations are actually testable (not vague)
        vague_words = ["good", "proper", "appropriate", "correct", "should", "nice"]
        testable_count = 0
        vague_count = 0
        
        for exp in expectations:
            exp_lower = exp.lower()
            # Testable expectations mention specific outputs, files, or behaviors
            if any(kw in exp_lower for kw in ["file", "create", "include", "has", "contains", "output", "save", "write", ".md", ".json", ".py"]):
                testable_count += 1
            elif any(vw in exp_lower for vw in vague_words):
                vague_count += 1
            else:
                testable_count += 1  # Assume testable if not obviously vague
        
        if testable_count >= len(expectations) * 0.7:  # 70% must be testable
            results["score"] += 20
            results["checks"].append({
                "name": f"{eval_name}: expectations testable",
                "passed": True,
                "points": 20,
                "count": f"{testable_count}/{len(expectations)} testable"
            })
        else:
            results["checks"].append({
                "name": f"{eval_name}: expectations testable",
                "passed": False,
                "points": 0,
                "note": f"Only {testable_count}/{len(expectations)} expectations are testable. Avoid vague terms like 'good', 'proper', 'correct'"
            })

    # Check prompt is substantial enough to test against
    results["max_score"] += 15
    prompt = eval_item.get("prompt", "")
    if len(prompt) >= 50:
        results["score"] += 15
        results["checks"].append({
            "name": f"{eval_name}: prompt length",
            "passed": True,
            "points": 15,
            "length": len(prompt)
        })
    else:
        results["checks"].append({
            "name": f"{eval_name}: prompt length",
            "passed": False,
            "points": 0,
            "note": f"Too short: {len(prompt)} chars (min 50). Prompts must be realistic user requests."
        })

    return results


def print_report(results: dict):
    """Print formatted report."""
    print("\n" + "="*60)
    print("EVAL DEFINITION REVIEW")
    print("="*60)
    print(f"\nSkill: {results['skill_path']}")
    print(f"Evals file: {results['evals_file']}")
    print(f"\nSCORE: {results['score']}/{results['max_score']} ({results['percentage']}%)")
    print("\n" + "-"*60)
    print("CHECKS:")
    print("-"*60)
    
    for check in results["checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"\n{status} {check['name']}")
        if check["passed"]:
            if "eval_count" in check:
                print(f"   Count: {check['eval_count']} evals")
            if "count" in check:
                print(f"   Count: {check['count']} expectations")
            if "length" in check:
                print(f"   Length: {check['length']} chars")
        else:
            if "note" in check:
                print(f"   Note: {check['note']}")
    
    print("\n" + "="*60)
    
    if results["percentage"] >= 80:
        print("✅ EXCELLENT - Eval definitions are well-structured")
    elif results["percentage"] >= 60:
        print("✅ GOOD - Eval definitions are functional")
    else:
        print("⚠️  NEEDS WORK - Eval definitions need improvement")
    
    print(f"\nSuccess Rate: {results['percentage']}%")
    print("="*60 + "\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python review_evals.py <skill_directory>")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    
    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)
    
    results = review_evals(skill_path)
    print_report(results)
    
    # Save results
    output_file = skill_path / "evals" / "review_results.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(results, indent=2))
    print(f"Results saved to: {output_file}")
    
    sys.exit(0 if results["percentage"] >= 60 else 1)


if __name__ == "__main__":
    main()
