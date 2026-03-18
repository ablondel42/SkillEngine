#!/usr/bin/env python3
"""
Full Test Suite - Includes subagent execution tests.

Runs both static analysis AND subagent-based execution tests.
Use when you have quota available and want complete validation.

Usage: python test_suite.py <skill_directory> [--static-only]

Options:
  --static-only   Run only static tests (no subagents)
"""

import subprocess
import sys
import time
from pathlib import Path


def run_test(name: str, command: list) -> tuple:
    """Run a test and return (success, output)."""
    print(f"\n{name}")
    print("-" * 40)
    
    start = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    elapsed = time.time() - start
    
    print(result.stdout)
    if result.stderr and "Traceback" not in result.stderr:
        print(result.stderr)
    
    return result.returncode == 0, elapsed


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_suite.py <skill_directory> [--static-only]")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    script_dir = Path(__file__).parent
    
    static_only = "--static-only" in sys.argv
    
    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)
    
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)
    
    print("="*60)
    if static_only:
        print("STATIC TEST SUITE (No Subagents)")
    else:
        print("FULL TEST SUITE (With Subagents)")
    print("="*60)
    print(f"\nSkill: {skill_path.name}")
    print(f"Path: {skill_path}")
    
    # Static tests (always run)
    tests = [
        ("TEST 1: Quick Validation (syntax)", 
         ["python3", script_dir / "quick_validate.py", skill_path]),
        
        ("TEST 2: Static Analysis (quality)",
         ["python3", script_dir / "static_analysis.py", skill_path]),
        
        ("TEST 3: Trigger Readiness (optimization)",
         ["python3", script_dir / "trigger_readiness.py", skill_path]),
        
        ("TEST 4: Eval Definitions (structure)",
         ["python3", script_dir / "review_evals.py", skill_path]),
        
        ("TEST 5: File Structure (organization)",
         ["python3", script_dir / "check_structure.py", skill_path]),
    ]
    
    # Subagent tests (only if not --static-only)
    if not static_only:
        print("\n" + "="*60)
        print("SUBAGENT EXECUTION TESTS")
        print("="*60)

        # Import subagent test functions
        from run_trigger_tests import (
            load_trigger_tests,
            run_trigger_test,
            TriggerTestReport,
            generate_report
        )
        from datetime import datetime

        # Load and run trigger tests
        test_cases = load_trigger_tests(skill_path)
        print(f"\nLoaded {len(test_cases)} trigger test cases")

        # Run trigger tests with subagent spawning
        trigger_report = TriggerTestReport(
            skill_name=skill_path.name,
            skill_path=str(skill_path),
            test_date=datetime.now().isoformat()
        )

        for test_case in test_cases:
            print(f"\nRunning: {test_case['name']}")
            result = run_trigger_test(test_case, skill_path.name)
            trigger_report.results.append(result)
            trigger_report.total_tests += 1
            trigger_report.total_execution_time += result.execution_time

            if result.pass_fail:
                trigger_report.passed_tests += 1
            else:
                trigger_report.failed_tests += 1

        # Add trigger test results to main test suite
        tests.append((
            "TEST 6: Subagent Trigger Tests (execution)",
            ["python3", script_dir / "run_trigger_tests.py", skill_path, "--skill-name", skill_path.name]
        ))
    
    results = []
    times = []
    
    for name, command in tests:
        success, elapsed = run_test(name, command)
        results.append(success)
        times.append(elapsed)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    # Store test results for summary table
    test_results = []
    for i, (name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        pct = "100%" if results[i] else "0%"
        test_results.append((status, name, pct, times[i]))
        print(f"{status} - {name} ({times[i]:.2f}s) - {pct}")
    
    print("-"*60)
    total_time = sum(times)
    overall_pct = round(passed / total * 100, 1) if total > 0 else 0
    
    if passed == total:
        print(f"OVERALL: ✅ ALL {total} TESTS PASSED ({overall_pct}%)")
    else:
        print(f"OVERALL: ⚠️  {passed}/{total} TESTS PASSED ({overall_pct}%)")
    
    print("="*60)
    print(f"\nTotal time: {total_time:.2f} seconds")
    
    if static_only:
        print(f"Subagents used: 0 (static-only mode)")
        print(f"API calls: 0")
    else:
        print(f"Subagents used: {trigger_report.total_tests}")
        print(f"Trigger success rate: {trigger_report.trigger_success_rate}%")
        print(f"Workflow compliance: {trigger_report.workflow_compliance_rate}%")
        print(f"API calls: {trigger_report.total_tests} (one per trigger test)")
    
    # Cleanup test artifacts
    print("\n" + "-"*60)
    print("CLEANUP:")
    print("-"*60)
    
    test_artifacts = [
        skill_path / "static_analysis_results.json",
        skill_path / "structure_results.json",
        skill_path / "evals" / "review_results.json",
    ]
    
    cleaned = 0
    for artifact in test_artifacts:
        if artifact.exists():
            artifact.unlink()
            cleaned += 1
            print(f"✅ Removed: {artifact.name}")
    
    # Remove empty test output directories (except trigger-tests when subagents ran)
    test_dirs = [
        skill_path / "eval-outputs" / "fast-test-outputs",
        skill_path / "eval-outputs" / "parallel-test-outputs",
    ]

    # Only clean eval-outputs if static-only mode
    if static_only:
        test_dirs.append(skill_path / "eval-outputs")

    for test_dir in test_dirs:
        if test_dir.exists() and test_dir.is_dir():
            import shutil
            shutil.rmtree(test_dir)
            cleaned += 1
            print(f"✅ Removed: {test_dir.name}/")
    
    if cleaned == 0:
        print("No test artifacts to clean")
    
    print("-"*60)
    print(f"Cleaned: {cleaned} artifacts")
    
    # Final summary table
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    print(f"{'Test':<40} {'Status':<10} {'Success':<10} {'Time':<10}")
    print("-"*60)
    for status, name, pct, time in test_results:
        # Truncate name if too long
        display_name = name[:38] + ".." if len(name) > 40 else name
        print(f"{display_name:<40} {status:<10} {pct:<10} {time:.2f}s")
    print("-"*60)
    print(f"{'OVERALL':<40} {'✅ PASS' if passed == total else '⚠️ FAIL':<10} {overall_pct}%{'':<9} {total_time:.2f}s")
    print("="*60)
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
