#!/usr/bin/env python3
"""
Trigger Readiness Analysis - No subagent required.

Analyzes skill description for trigger optimization.
Based on Cycle 5 research findings for what actually triggers skills.
"""

import json
import re
import sys
from pathlib import Path


def analyze_trigger_readiness(skill_path: Path) -> dict:
    """Analyze skill for trigger readiness based on research findings."""

    results = {
        "skill_path": str(skill_path),
        "skill_name": None,
        "description": None,
        "checks": [],
        "score": 0,
        "max_score": 0
    }

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return results

    content = skill_md.read_text()

    # Extract description from frontmatter
    desc_match = re.search(r'description:\s*(.+?)(?:\n---|\n\n)', content[:1000], re.DOTALL)
    if not desc_match:
        results["checks"].append({
            "name": "Description found",
            "passed": False,
            "points": 0,
            "note": "No description in frontmatter"
        })
        return results

    description = desc_match.group(1).strip()
    results["description"] = description

    # Extract skill name
    name_match = re.search(r'name:\s*["\']?([a-z0-9-]+)["\']?', content[:500])
    if name_match:
        results["skill_name"] = name_match.group(1)

    # Check 1: Description length (50-500 chars optimal) - from research
    results["max_score"] += 15
    if 50 <= len(description) <= 500:
        results["score"] += 15
        results["checks"].append({
            "name": "Description length (50-500 chars)",
            "passed": True,
            "points": 15,
            "length": len(description)
        })
    else:
        results["checks"].append({
            "name": "Description length (50-500 chars)",
            "passed": False,
            "points": 0,
            "note": f"Current: {len(description)} chars (optimal: 50-500)"
        })

    # Check 2: Contains "I need a..." pattern (from Cycle 5 research)
    results["max_score"] += 25
    # The winning formula was: "I need a [domain] for my [context]"
    need_patterns = [
        r'\bi need\b',
        r'\bi want\b',
        r'\bi.*build\b',
        r'\bi.*create\b',
        r'help.*(?:build|create)',
    ]
    need_score = sum(1 for pattern in need_patterns if re.search(pattern, description.lower()))
    
    if need_score >= 1:
        results["score"] += 25
        results["checks"].append({
            "name": "User intent pattern",
            "passed": True,
            "points": 25,
            "note": "Description matches user intent patterns ('I need', 'I want')"
        })
    else:
        results["checks"].append({
            "name": "User intent pattern",
            "passed": False,
            "points": 0,
            "note": "Missing user intent patterns - may not trigger reliably"
        })

    # Check 3: Domain-specific keywords (CRITICAL)
    results["max_score"] += 25
    # Must have at least 3 domain terms from the skill's actual domain
    domain_keywords = [
        "design system", "design systems",
        "component", "components",
        "tokens", "UI", "interface",
        "building blocks", "reusable",
        "patterns", "style guide"
    ]
    domain_count = sum(1 for kw in domain_keywords if kw in description.lower())
    
    if domain_count >= 3:
        results["score"] += 25
        results["checks"].append({
            "name": "Domain keywords (3+ required)",
            "passed": True,
            "points": 25,
            "found": domain_count
        })
    else:
        results["checks"].append({
            "name": "Domain keywords (3+ required)",
            "passed": False,
            "points": 0,
            "note": f"Found {domain_count}/3 - skill may not trigger for domain queries"
        })

    # Check 4: Trigger conditions - when to use the skill
    results["max_score"] += 20
    # Must explicitly state when the skill should be used
    trigger_patterns = [
        r'(?:use|trigger|when).*?(?:user|users)',
        r'(?:should|must|will).*?trigger',
        r'(?:mention|mentions|phrases?|phrases like)',
        r'(?:casual|explicit|direct)',
        r'even.*(?:casual|mention)',
    ]
    trigger_score = sum(1 for pattern in trigger_patterns if re.search(pattern, description.lower()))
    
    if trigger_score >= 1:
        results["score"] += 20
        results["checks"].append({
            "name": "Trigger conditions defined",
            "passed": True,
            "points": 20,
            "note": "Skill defines when it should trigger"
        })
    else:
        results["checks"].append({
            "name": "Trigger conditions defined",
            "passed": False,
            "points": 0,
            "note": "No trigger conditions - agent may not know when to use skill"
        })

    # Check 5: Example trigger phrases (from research)
    results["max_score"] += 15
    # Must include at least one example phrase that should trigger
    example_patterns = [
        r'(?:like|such as|phrases? like|for example|e\.g\.)',
        r'["\'].*?["\']',  # Quoted examples
        r'(?:casual mentions|even)',
    ]
    example_score = sum(1 for pattern in example_patterns if re.search(pattern, description.lower()))
    
    if example_score >= 1:
        results["score"] += 15
        results["checks"].append({
            "name": "Example trigger phrases",
            "passed": True,
            "points": 15,
            "note": "Includes example phrases that should trigger"
        })
    else:
        results["checks"].append({
            "name": "Example trigger phrases",
            "passed": False,
            "points": 0,
            "note": "No example phrases - harder to understand trigger scope"
        })

    # Calculate percentage
    results["percentage"] = round(results["score"] / results["max_score"] * 100, 1) if results["max_score"] > 0 else 0

    return results


def print_report(results: dict):
    """Print formatted report."""
    print("\n" + "="*60)
    print("TRIGGER READINESS ANALYSIS")
    print("="*60)
    print(f"\nSkill: {results.get('skill_name', 'Unknown')}")
    print(f"Description length: {len(results.get('description', ''))} chars")
    print(f"\nSCORE: {results['score']}/{results['max_score']} ({results['percentage']}%)")
    print("\n" + "-"*60)
    print("TRIGGER OPTIMIZATION CHECKS:")
    print("-"*60)

    for check in results["checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"\n{status} {check['name']}")
        if check["passed"]:
            if "length" in check:
                print(f"   Length: {check['length']} chars")
            if "found" in check:
                print(f"   Found: {check['found']}")
            if "note" in check:
                print(f"   {check['note']}")
        else:
            if "note" in check:
                print(f"   ⚠️  {check['note']}")

    print("\n" + "="*60)

    if results["percentage"] >= 90:
        print("✅ EXCELLENT - Description optimized for triggering (based on Cycle 5 research)")
    elif results["percentage"] >= 70:
        print("✅ GOOD - Description should trigger reliably")
    elif results["percentage"] >= 50:
        print("⚠️  FAIR - Description may have trigger issues")
    else:
        print("❌ POOR - Description needs trigger optimization")

    print(f"\nSuccess Rate: {results['percentage']}%")
    print("="*60 + "\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python trigger_readiness.py <skill_directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)

    results = analyze_trigger_readiness(skill_path)
    print_report(results)

    sys.exit(0 if results["percentage"] >= 70 else 1)


if __name__ == "__main__":
    main()
