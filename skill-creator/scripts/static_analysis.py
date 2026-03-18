#!/usr/bin/env python3
"""
Static Skill Analysis - No subagent required.

Analyzes skill files for quality, completeness, and best practices.
Only includes checks that can actually find real errors.
"""

import json
import re
from pathlib import Path


def analyze_skill(skill_path: Path) -> dict:
    """Analyze a skill directory for quality metrics."""

    results = {
        "skill_path": str(skill_path),
        "skill_name": None,
        "checks": [],
        "score": 0,
        "max_score": 0
    }

    # Check 1: SKILL.md exists (CRITICAL)
    results["max_score"] += 20
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        results["score"] += 20
        results["checks"].append({
            "name": "SKILL.md exists",
            "passed": True,
            "points": 20
        })
    else:
        results["checks"].append({
            "name": "SKILL.md exists",
            "passed": False,
            "points": 0,
            "note": "Required file missing - skill cannot function"
        })
        return results

    content = skill_md.read_text()

    # Check 2: Has workflow structure (CRITICAL)
    results["max_score"] += 20
    # Look for actual workflow patterns, not just keywords
    workflow_patterns = [
        r'(?:step|phase)\s*\d*[:\s]',  # "Step 1:" or "Phase 1:"
        r'(?:MANDATORY|REQUIRED|MUST|NON-NEGOTIABLE)',  # Strong requirements
        r'(?:before|after|then|finally)',  # Sequential instructions
    ]
    workflow_score = sum(1 for pattern in workflow_patterns if re.search(pattern, content, re.IGNORECASE))
    
    if workflow_score >= 2:
        results["score"] += 20
        results["checks"].append({
            "name": "Workflow structure defined",
            "passed": True,
            "points": 20,
            "note": f"Found {workflow_score} workflow patterns"
        })
    else:
        results["checks"].append({
            "name": "Workflow structure defined",
            "passed": False,
            "points": 0,
            "note": "No clear workflow structure - agent may not follow proper sequence"
        })

    # Check 3: Has interview/gathering phase (IMPORTANT for interactive skills)
    results["max_score"] += 15
    interview_patterns = [
        r'(?:interview|questions?|ask|gather)',
        r'(?:before.*(?:write|code|generate)|before.*proceed)',
        r'(?:wait.*response|wait.*answer)',
    ]
    interview_score = sum(1 for pattern in interview_patterns if re.search(pattern, content, re.IGNORECASE))
    
    if interview_score >= 1:
        results["score"] += 15
        results["checks"].append({
            "name": "Information gathering phase",
            "passed": True,
            "points": 15,
            "note": "Skill requires gathering info before acting"
        })
    else:
        results["checks"].append({
            "name": "Information gathering phase",
            "passed": False,
            "points": 0,
            "note": "No interview phase - may produce generic output"
        })

    # Check 4: Has output format specification (IMPORTANT)
    results["max_score"] += 15
    # Look for actual format specs, not just the word "example"
    format_patterns = [
        r'```[a-z]*\n',  # Code blocks with language
        r'(?:output|result|format)[:\s]',  # "Output:" or "Format:"
        r'(?:save|write|create).*\.(?:md|json|py|txt|ts|tsx|js)',  # File creation
    ]
    format_score = sum(1 for pattern in format_patterns if re.search(pattern, content, re.IGNORECASE))
    
    if format_score >= 2:
        results["score"] += 15
        results["checks"].append({
            "name": "Output format specified",
            "passed": True,
            "points": 15,
            "note": "Clear output format defined"
        })
    else:
        results["checks"].append({
            "name": "Output format specified",
            "passed": False,
            "points": 0,
            "note": "No clear output format - agent may produce inconsistent output"
        })

    # Check 5: Has error handling or edge cases (IMPORTANT)
    results["max_score"] += 15
    error_patterns = [
        r'(?:if.*fail|fail.*if|error|fallback|handle)',
        r'(?:edge.*case|corner.*case|exception)',
        r'(?:cannot|unable|skip|alternative)',
    ]
    error_score = sum(1 for pattern in error_patterns if re.search(pattern, content, re.IGNORECASE))
    
    if error_score >= 2:
        results["score"] += 15
        results["checks"].append({
            "name": "Error handling defined",
            "passed": True,
            "points": 15,
            "note": "Skill handles errors/edge cases"
        })
    else:
        results["checks"].append({
            "name": "Error handling defined",
            "passed": False,
            "points": 0,
            "note": "No error handling - may fail silently on edge cases"
        })

    # Check 6: Evals exist and are valid (CRITICAL)
    # Check for split eval files (eval_group1.json, etc.) or original evals.json
    results["max_score"] += 20
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
            results["score"] += 20
            results["checks"].append({
                "name": "Eval definitions",
                "passed": True,
                "points": 20,
                "count": f"{total_evals} evals in {valid_files} file(s)"
            })
        else:
            results["checks"].append({
                "name": "Eval definitions",
                "passed": False,
                "points": 0,
                "note": "Eval files exist but no evals defined"
            })
    else:
        results["checks"].append({
            "name": "Eval definitions",
            "passed": False,
            "points": 0,
            "note": "No eval_group*.json or evals.json - cannot test skill"
        })

    # Check 7: Description quality (from frontmatter)
    results["max_score"] += 15
    desc_match = re.search(r'description:\s*(.+?)(?:\n---|\n\n)', content[:1000], re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()
        
        # Check length AND trigger content
        length_ok = 50 <= len(description) <= 500
        has_trigger = any(kw in description.lower() for kw in ["when", "trigger", "use"])
        has_domain = any(kw in description.lower() for kw in ["system", "component", "design", "build"])
        
        if length_ok and has_trigger and has_domain:
            results["score"] += 15
            results["checks"].append({
                "name": "Description quality",
                "passed": True,
                "points": 15,
                "length": len(description),
                "note": "Description has proper length and trigger content"
            })
        else:
            issues = []
            if not length_ok:
                issues.append(f"length={len(description)}")
            if not has_trigger:
                issues.append("no trigger words")
            if not has_domain:
                issues.append("no domain keywords")
            
            results["checks"].append({
                "name": "Description quality",
                "passed": False,
                "points": 0,
                "note": f"Issues: {', '.join(issues)}"
            })
    else:
        results["checks"].append({
            "name": "Description quality",
            "passed": False,
            "points": 0,
            "note": "No description found in frontmatter"
        })

    # Calculate percentage
    results["percentage"] = round(results["score"] / results["max_score"] * 100, 1) if results["max_score"] > 0 else 0

    return results


def print_report(results: dict):
    """Print a formatted analysis report."""
    print("\n" + "="*60)
    print(f"STATIC ANALYSIS REPORT")
    print("="*60)
    print(f"\nSkill: {results.get('skill_name', 'Unknown')}")
    print(f"Path: {results['skill_path']}")
    print(f"\nSCORE: {results['score']}/{results['max_score']} ({results['percentage']}%)")
    print("\n" + "-"*60)
    print("CRITICAL CHECKS:")
    print("-"*60)

    for check in results["checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"\n{status} {check['name']}")
        if check["passed"]:
            if "count" in check:
                print(f"   Count: {check['count']}")
            if "length" in check:
                print(f"   Length: {check['length']} chars")
            if "note" in check:
                print(f"   {check['note']}")
        else:
            if "note" in check:
                print(f"   ⚠️  {check['note']}")

    print("\n" + "="*60)

    # Quality assessment based on critical checks
    critical_passed = sum(1 for c in results["checks"] if c["passed"] and c["points"] >= 15)
    critical_total = len(results["checks"])
    
    if results["percentage"] >= 90:
        print("✅ EXCELLENT - Skill has proper structure and error handling")
    elif results["percentage"] >= 70:
        print("✅ GOOD - Skill is functional but may have edge case issues")
    elif results["percentage"] >= 50:
        print("⚠️  FAIR - Skill missing critical elements")
    else:
        print("❌ POOR - Skill needs major work")

    print(f"\nCritical checks passed: {critical_passed}/{critical_total}")
    print(f"Success Rate: {results['percentage']}%")
    print("="*60 + "\n")


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python static_analysis.py <skill_directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)

    results = analyze_skill(skill_path)
    print_report(results)

    # Save results to JSON
    output_file = skill_path / "static_analysis_results.json"
    output_file.write_text(json.dumps(results, indent=2))
    print(f"Results saved to: {output_file}")

    # Exit with error code if score < 50%
    sys.exit(0 if results["percentage"] >= 70 else 1)


if __name__ == "__main__":
    main()
