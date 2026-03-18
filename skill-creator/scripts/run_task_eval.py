#!/usr/bin/env python3
"""Run execution evaluation using Task tool instead of claude -p.

Prepares eval structure and manifests for Task-based execution testing.
The actual subagent spawning happens in the Claude Code session.

After tests complete, run with --cleanup to remove all output files.
"""

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime


def prepare_evals(eval_set: list[dict], skill_path: Path, output_dir: Path) -> dict:
    """Prepare eval structure and return manifest for execution."""
    # Handle nested evals format
    if "evals" in eval_set:
        evals_list = eval_set["evals"]
    else:
        evals_list = eval_set
    
    results = []
    
    for eval_item in evals_list:
        eval_id = eval_item.get("id", len(results))
        eval_name = eval_item.get("eval_name", f"eval-{eval_id}")
        prompt = eval_item["prompt"]
        # Support both 'expectations' and 'expected_output' fields
        expectations = eval_item.get("expectations", [])
        if not expectations and "expected_output" in eval_item:
            expectations = [eval_item["expected_output"]]
        files = eval_item.get("files", [])
        
        # Create output directory for this eval
        eval_output_dir = output_dir / f"eval-{eval_id}-{eval_name}"
        eval_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create outputs subdirectory
        (eval_output_dir / "outputs").mkdir(exist_ok=True)
        
        # Save eval metadata
        metadata = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "prompt": prompt,
            "expectations": expectations,
            "files": files,
            "skill_path": str(skill_path),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
        }
        (eval_output_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2)
        )
        
        results.append({
            "eval_id": eval_id,
            "eval_name": eval_name,
            "status": "pending",
            "output_dir": str(eval_output_dir),
            "prompt": prompt,
        })
    
    # Save run manifest
    manifest = {
        "skill_name": skill_path.name,
        "skill_path": str(skill_path),
        "evals_run": len(results),
        "timestamp": datetime.now().isoformat(),
        "output_base_dir": str(output_dir),
        "results": results,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    return manifest


def cleanup_evals(output_dir: Path) -> dict:
    """Clean up eval output directories."""
    cleaned = []
    
    if output_dir.exists():
        # Remove all eval output directories
        for eval_dir in output_dir.iterdir():
            if eval_dir.is_dir() and eval_dir.name.startswith("eval-"):
                shutil.rmtree(eval_dir)
                cleaned.append(str(eval_dir))
        
        # Remove manifest
        manifest = output_dir / "manifest.json"
        if manifest.exists():
            manifest.unlink()
            cleaned.append(str(manifest))
    
    return {"cleaned": cleaned, "count": len(cleaned)}


def main():
    parser = argparse.ArgumentParser(
        description="Prepare Task-based execution evaluation"
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
        help="Directory for eval outputs"
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
        result = cleanup_evals(output_dir)
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
    
    manifest = prepare_evals(eval_set, skill_path, output_dir)
    
    print(f"\n{'='*60}")
    print(f"Task-based Eval Preparation Complete")
    print(f"{'='*60}")
    print(f"Skill: {skill_path.name}")
    print(f"Evals prepared: {manifest['evals_run']}")
    print(f"Output directory: {output_dir}")
    print(f"\nNext steps:")
    print(f"1. Review manifest.json for eval details")
    print(f"2. Spawn subagents for each eval (see instructions below)")
    print(f"3. Run collect_results.py after all evals complete")
    print(f"\n{'='*60}\n")
    
    # Print execution instructions
    print("EXECUTION INSTRUCTIONS:")
    print("-" * 60)
    for result in manifest["results"]:
        print(f"\nEval {result['eval_id']}: {result['eval_name']}")
        print(f"  Prompt: {result['prompt'][:100]}...")
        print(f"  Output dir: {result['output_dir']}")
        print(f"  Command: Spawn subagent with task instruction")
    
    print(f"\n{'='*60}\n")
    print(json.dumps(manifest, indent=2))
    
    return 0


if __name__ == "__main__":
    exit(main())
