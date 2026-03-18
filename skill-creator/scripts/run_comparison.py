#!/usr/bin/env python3
"""Run comparison tests (with skill vs without skill).

For each eval, spawns two subagents:
1. WITH skill - Uses the skill
2. WITHOUT skill - Baseline (no skill)

Then spawns a comparator subagent to compare both outputs blindly.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil


def prepare_comparison(eval_set: dict, skill_path: Path, output_dir: Path) -> dict:
    """Prepare comparison test structure."""
    # Handle nested evals format
    if "evals" in eval_set:
        evals_list = eval_set["evals"]
    else:
        evals_list = eval_set
    
    eval_name = eval_set.get("eval_name", "comparison")
    
    results = []
    
    for eval_item in evals_list:
        eval_id = eval_item.get("id", 1)
        prompt = eval_item["prompt"]
        expectations = eval_item.get("expectations", [])
        
        # Create output directories
        eval_output_dir = output_dir / f"eval-{eval_id}-{eval_name}"
        eval_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create with_skill and without_skill subdirectories
        (eval_output_dir / "with_skill" / "outputs").mkdir(parents=True, exist_ok=True)
        (eval_output_dir / "without_skill" / "outputs").mkdir(parents=True, exist_ok=True)
        
        # Save eval metadata
        metadata = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "prompt": prompt,
            "expectations": expectations,
            "skill_path": str(skill_path),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "comparison_type": "with_vs_without_skill"
        }
        (eval_output_dir / "eval_metadata.json").write_text(
            json.dumps(metadata, indent=2)
        )
        
        results.append({
            "eval_id": eval_id,
            "eval_name": eval_name,
            "status": "pending",
            "output_dir": str(eval_output_dir),
            "prompt": prompt,
            "with_skill_dir": str(eval_output_dir / "with_skill"),
            "without_skill_dir": str(eval_output_dir / "without_skill")
        })
    
    # Save manifest
    manifest = {
        "skill_name": eval_set.get("skill_name", "unknown"),
        "skill_path": str(skill_path),
        "evals_run": len(results),
        "timestamp": datetime.now().isoformat(),
        "output_base_dir": str(output_dir),
        "comparison_type": "with_vs_without_skill",
        "results": results
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    return manifest


def cleanup_comparison(output_dir: Path) -> dict:
    """Clean up comparison output directories."""
    cleaned = []
    
    if output_dir.exists():
        # Remove all eval output directories
        for eval_dir in output_dir.iterdir():
            if eval_dir.is_dir() and eval_dir.name.startswith("eval-"):
                shutil.rmtree(eval_dir)
                cleaned.append(str(eval_dir))
        
        # Remove manifest and comparison results
        for f in ["manifest.json", "comparison_results.json"]:
            manifest = output_dir / f
            if manifest.exists():
                manifest.unlink()
                cleaned.append(str(manifest))
    
    return {"cleaned": cleaned, "count": len(cleaned)}


def main():
    parser = argparse.ArgumentParser(
        description="Run comparison tests (with skill vs without skill)"
    )
    parser.add_argument(
        "--eval-set",
        required=False,
        default=None,
        help="Path to eval set JSON file (not required for --cleanup)"
    )
    parser.add_argument(
        "--skill-path",
        required=False,
        default=None,
        help="Path to skill directory (not required for --cleanup)"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for comparison outputs"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up output directories instead of preparing"
    )
    args = parser.parse_args()
    
    # Handle cleanup mode
    if args.cleanup:
        output_dir = Path(args.output_dir)
        result = cleanup_comparison(output_dir)
        print(f"\n{'='*60}")
        print(f"CLEANUP COMPLETE")
        print(f"{'='*60}")
        print(f"Cleaned {result['count']} items:")
        for item in result['cleaned']:
            print(f"  - {item}")
        print(f"{'='*60}\n")
        return 0
    
    # Validate required args for non-cleanup mode
    if not args.eval_set or not args.skill_path:
        print("Error: --eval-set and --skill-path are required for non-cleanup mode")
        return 1
    
    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}")
        return 1
    
    manifest = prepare_comparison(eval_set, skill_path, output_dir)
    
    print(f"\n{'='*60}")
    print(f"Comparison Test Preparation Complete")
    print(f"{'='*60}")
    print(f"Skill: {manifest['skill_name']}")
    print(f"Evals prepared: {manifest['evals_run']}")
    print(f"Output directory: {output_dir}")
    print(f"\nNext steps:")
    print(f"1. Review manifest.json for eval details")
    print(f"2. For each eval, spawn TWO subagents:")
    print(f"   a) WITH skill: 'Execute using the {manifest['skill_name']} skill...'")
    print(f"   b) WITHOUT skill: 'Execute this task WITHOUT using any skills...'")
    print(f"3. After both complete, spawn comparator subagent")
    print(f"4. Run collect_results.py after all comparisons complete")
    print(f"\n{'='*60}\n")
    
    print(json.dumps(manifest, indent=2))
    
    return 0


if __name__ == "__main__":
    exit(main())
