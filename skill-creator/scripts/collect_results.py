#!/usr/bin/env python3
"""Collect and aggregate results from Task-based eval execution.

Reads grading results from each eval output directory and produces
a summary report.

After collecting results, run with --cleanup to remove all output files.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil


def collect_results(output_dir: Path) -> dict:
    """Collect results from all eval output directories."""
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest found at {output_dir}")
    
    manifest = json.loads(manifest_path.read_text())
    
    collected = {
        "skill_name": manifest["skill_name"],
        "skill_path": manifest["skill_path"],
        "collection_timestamp": datetime.now().isoformat(),
        "evals": [],
        "summary": {
            "total_evals": manifest["evals_run"],
            "completed_evals": 0,
            "pending_evals": 0,
            "total_expectations": 0,
            "passed_expectations": 0,
            "overall_pass_rate": 0.0,
        },
    }
    
    for result in manifest["results"]:
        eval_id = result["eval_id"]
        eval_name = result["eval_name"]
        eval_output_dir = Path(result["output_dir"])
        
        eval_result = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "status": "pending",
            "grading": None,
            "comparison": None,
        }
        
        # Check for grading results
        grading_path = eval_output_dir / "grading.json"
        if grading_path.exists():
            grading = json.loads(grading_path.read_text())
            eval_result["grading"] = grading
            eval_result["status"] = "graded"
            collected["summary"]["completed_evals"] += 1
            
            # Aggregate expectation stats
            if "summary" in grading:
                summary = grading["summary"]
                collected["summary"]["total_expectations"] += summary.get("total", 0)
                collected["summary"]["passed_expectations"] += summary.get("passed", 0)
        else:
            # Check if outputs exist (execution started but not graded)
            outputs_dir = eval_output_dir / "outputs"
            if outputs_dir.exists() and any(outputs_dir.iterdir()):
                eval_result["status"] = "executed"
                collected["summary"]["completed_evals"] += 1
            else:
                eval_result["status"] = "pending"
                collected["summary"]["pending_evals"] += 1
        
        # Check for comparison results
        comparison_path = eval_output_dir / "comparison.json"
        if comparison_path.exists():
            comparison = json.loads(comparison_path.read_text())
            eval_result["comparison"] = comparison
        
        collected["evals"].append(eval_result)
    
    # Calculate overall pass rate
    total = collected["summary"]["total_expectations"]
    passed = collected["summary"]["passed_expectations"]
    if total > 0:
        collected["summary"]["overall_pass_rate"] = round(passed / total, 3)
    
    return collected


def generate_report(collected: dict) -> str:
    """Generate a text report from collected results."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"Skill Evaluation Report: {collected['skill_name']}")
    lines.append("=" * 60)
    lines.append("")
    
    # Summary
    summary = collected["summary"]
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total evals:        {summary['total_evals']}")
    lines.append(f"Completed evals:    {summary['completed_evals']}")
    lines.append(f"Pending evals:      {summary['pending_evals']}")
    lines.append(f"Total expectations: {summary['total_expectations']}")
    lines.append(f"Passed expectations: {summary['passed_expectations']}")
    lines.append(f"Overall pass rate:  {summary['overall_pass_rate']:.1%}")
    lines.append("")
    
    # Per-eval details
    lines.append("PER-EVAL RESULTS")
    lines.append("-" * 40)
    
    for eval_result in collected["evals"]:
        lines.append(f"\nEval {eval_result['eval_id']}: {eval_result['eval_name']}")
        lines.append(f"  Status: {eval_result['status']}")
        
        if eval_result["grading"]:
            grading = eval_result["grading"]
            if "summary" in grading:
                s = grading["summary"]
                lines.append(f"  Pass rate: {s.get('pass_rate', 0):.1%} ({s.get('passed', 0)}/{s.get('total', 0)})")
        
        if eval_result["comparison"]:
            comparison = eval_result["comparison"]
            lines.append(f"  Comparison winner: {comparison.get('winner', 'N/A')}")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def cleanup_results(output_dir: Path) -> dict:
    """Clean up all result files in output directory."""
    cleaned = []
    
    # Remove collected results
    collected = output_dir / "collected_results.json"
    if collected.exists():
        collected.unlink()
        cleaned.append(str(collected))
    
    # Remove report if exists
    report = output_dir / "eval-report.txt"
    if report.exists():
        report.unlink()
        cleaned.append(str(report))
    
    # Remove grading.json from each eval
    for eval_dir in output_dir.iterdir():
        if eval_dir.is_dir():
            grading = eval_dir / "grading.json"
            if grading.exists():
                grading.unlink()
                cleaned.append(str(grading))
            comparison = eval_dir / "comparison.json"
            if comparison.exists():
                comparison.unlink()
                cleaned.append(str(comparison))
    
    return {"cleaned": cleaned, "count": len(cleaned)}


def main():
    parser = argparse.ArgumentParser(
        description="Collect results from Task-based eval execution"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory containing eval outputs"
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Path to save text report (optional)"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up result files instead of collecting"
    )
    args = parser.parse_args()
    
    # Handle cleanup mode
    if args.cleanup:
        output_dir = Path(args.output_dir)
        result = cleanup_results(output_dir)
        print(f"\n{'='*60}")
        print(f"CLEANUP COMPLETE")
        print(f"{'='*60}")
        print(f"Cleaned {result['count']} items:")
        for item in result['cleaned']:
            print(f"  - {item}")
        print(f"{'='*60}\n")
        return 0
    
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        return 1
    
    collected = collect_results(output_dir)
    
    # Save collected results
    results_path = output_dir / "collected_results.json"
    results_path.write_text(json.dumps(collected, indent=2))
    print(f"Results saved to: {results_path}")
    
    # Generate and print report
    report = generate_report(collected)
    print("\n" + report)
    
    # Save report if requested
    if args.report:
        Path(args.report).write_text(report)
        print(f"\nReport saved to: {args.report}")
    
    return 0


if __name__ == "__main__":
    exit(main())
