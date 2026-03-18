#!/usr/bin/env python3
"""
Performance benchmarks for skill test scripts.

Tracks:
- Test execution time per script
- API quota usage estimation
- Parallel vs sequential execution comparison
- Memory usage (optional)

Usage:
  python benchmark_tests.py <skill_directory> [--output <output_file>]
"""

import cProfile
import json
import pstats
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Callable, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from quick_validate import validate_skill
from static_analysis import analyze_skill
from review_evals import review_evals
from check_structure import check_structure
from trigger_readiness import analyze_trigger_readiness


@dataclass
class BenchmarkResult:
    """Result of a single benchmark."""
    name: str
    execution_time: float
    memory_usage: Optional[float] = None
    api_calls: int = 0
    success: bool = True
    error: Optional[str] = None


@dataclass
class BenchmarkReport:
    """Complete benchmark report."""
    skill_name: str
    skill_path: str
    benchmark_date: str
    total_execution_time: float = 0.0
    results: list[BenchmarkResult] = field(default_factory=list)
    parallel_speedup: float = 1.0
    api_quota_estimate: int = 0


def time_execution(func: Callable, *args, **kwargs) -> tuple:
    """Time the execution of a function.

    Returns:
        Tuple of (result, execution_time_seconds)
    """
    start_time = time.perf_counter()
    try:
        result = func(*args, **kwargs)
        success = True
        error = None
    except Exception as e:
        result = None
        success = False
        error = str(e)
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    return result, elapsed, success, error


def estimate_api_calls(script_name: str, result) -> int:
    """Estimate API calls for a given script."""
    # Static analysis scripts don't use API
    if script_name in ["quick_validate", "static_analysis", "review_evals",
                       "check_structure", "trigger_readiness"]:
        return 0

    # Trigger tests would use API
    if script_name == "run_trigger_tests":
        if result and hasattr(result, 'total_tests'):
            return result.total_tests

    return 0


def benchmark_script(name: str, func: Callable, skill_path: Path,
                     *args, **kwargs) -> BenchmarkResult:
    """Benchmark a single script."""
    result, elapsed, success, error = time_execution(func, skill_path, *args, **kwargs)

    return BenchmarkResult(
        name=name,
        execution_time=elapsed,
        api_calls=estimate_api_calls(name.lower().replace(" ", "_"), result),
        success=success,
        error=error
    )


def run_benchmarks(skill_path: Path) -> BenchmarkReport:
    """Run all benchmarks for a skill."""
    from pathlib import Path

    # Extract skill name
    skill_md = skill_path / "SKILL.md"
    skill_name = skill_path.name
    if skill_md.exists():
        import re
        content = skill_md.read_text()
        name_match = re.search(r'name:\s*["\']?([a-z0-9-]+)["\']?', content[:500])
        if name_match:
            skill_name = name_match.group(1)

    report = BenchmarkReport(
        skill_name=skill_name,
        skill_path=str(skill_path),
        benchmark_date=datetime.now().isoformat()
    )

    # Benchmark each script
    scripts = [
        ("Quick Validation", validate_skill),
        ("Static Analysis", analyze_skill),
        ("Eval Review", review_evals),
        ("Structure Check", check_structure),
        ("Trigger Readiness", analyze_trigger_readiness),
    ]

    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARKS")
    print("="*60)
    print(f"\nSkill: {skill_name}")
    print(f"Path: {skill_path}")
    print("\n" + "-"*60)

    for name, func in scripts:
        print(f"\nBenchmarking: {name}...")
        result = benchmark_script(name, func, skill_path)
        report.results.append(result)
        report.total_execution_time += result.execution_time

        status = "✅" if result.success else "❌"
        print(f"  {status} Time: {result.execution_time:.4f}s")
        if result.error:
            print(f"     Error: {result.error}")

    # Run parallel vs sequential comparison
    print("\n" + "-"*60)
    print("\nParallel vs Sequential Comparison:")
    parallel_result = benchmark_parallel_execution(skill_path)
    report.parallel_speedup = parallel_result

    print(f"\nSequential time: {report.total_execution_time:.4f}s")
    print(f"Parallel time: {parallel_result * report.total_execution_time:.4f}s (estimated)")
    print(f"Speedup: {parallel_result:.2f}x")

    # Calculate API quota estimate
    report.api_quota_estimate = sum(r.api_calls for r in report.results)

    return report


def benchmark_parallel_execution(skill_path: Path) -> float:
    """Benchmark parallel execution vs sequential.

    Returns:
        Speedup factor (parallel_time / sequential_time)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    scripts = [
        ("quick", validate_skill),
        ("static", analyze_skill),
        ("eval", review_evals),
        ("structure", check_structure),
        ("trigger", analyze_trigger_readiness),
    ]

    # Sequential execution
    seq_start = time.perf_counter()
    for _, func in scripts:
        try:
            func(skill_path)
        except Exception:
            pass
    seq_time = time.perf_counter() - seq_start

    # Parallel execution
    par_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(func, skill_path): name for name, func in scripts}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass
    par_time = time.perf_counter() - par_start

    # Calculate speedup
    if par_time > 0:
        speedup = seq_time / par_time
    else:
        speedup = 1.0

    return speedup


def profile_script(func: Callable, skill_path: Path, script_name: str) -> str:
    """Profile a script and return profiling stats."""
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        func(skill_path)
    except Exception:
        pass

    profiler.disable()

    # Get stats
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions

    return stream.getvalue()


def generate_report(report: BenchmarkReport, output_file: Optional[Path] = None):
    """Generate benchmark report."""
    # Console output
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)

    print(f"\nSkill: {report.skill_name}")
    print(f"Date: {report.benchmark_date}")
    print(f"\nTotal Execution Time: {report.total_execution_time:.4f}s")
    print(f"Parallel Speedup: {report.parallel_speedup:.2f}x")
    print(f"Estimated API Calls: {report.api_quota_estimate}")

    print("\n" + "-"*60)
    print(f"{'Script':<30} {'Time (s)':<12} {'Status':<10}")
    print("-"*60)

    for result in report.results:
        status = "✅ PASS" if result.success else "❌ FAIL"
        print(f"{result.name:<30} {result.execution_time:<12.4f} {status}")

    print("="*60)

    # JSON output
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        json_data = {
            "skill_name": report.skill_name,
            "skill_path": report.skill_path,
            "benchmark_date": report.benchmark_date,
            "summary": {
                "total_execution_time": report.total_execution_time,
                "parallel_speedup": report.parallel_speedup,
                "api_quota_estimate": report.api_quota_estimate
            },
            "results": [
                {
                    "name": r.name,
                    "execution_time": r.execution_time,
                    "success": r.success,
                    "error": r.error,
                    "api_calls": r.api_calls
                }
                for r in report.results
            ]
        }

        output_file.write_text(json.dumps(json_data, indent=2))
        print(f"\nReport saved to: {output_file}")


def compare_execution_modes(skill_path: Path, num_iterations: int = 3):
    """Compare sequential vs parallel execution over multiple iterations."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    scripts = [
        ("quick", validate_skill),
        ("static", analyze_skill),
        ("eval", review_evals),
        ("structure", check_structure),
        ("trigger", analyze_trigger_readiness),
    ]

    sequential_times = []
    parallel_times = []

    print("\n" + "="*60)
    print(f"EXECUTION MODE COMPARISON ({num_iterations} iterations)")
    print("="*60)

    for i in range(num_iterations):
        # Sequential
        seq_start = time.perf_counter()
        for _, func in scripts:
            try:
                func(skill_path)
            except Exception:
                pass
        seq_time = time.perf_counter() - seq_start
        sequential_times.append(seq_time)

        # Parallel
        par_start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(func, skill_path): name for name, func in scripts}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    pass
        par_time = time.perf_counter() - par_start
        parallel_times.append(par_time)

        print(f"\nIteration {i+1}:")
        print(f"  Sequential: {seq_time:.4f}s")
        print(f"  Parallel:   {par_time:.4f}s")
        print(f"  Speedup:    {seq_time/par_time:.2f}x" if par_time > 0 else "  Speedup: N/A")

    # Averages
    avg_seq = sum(sequential_times) / len(sequential_times)
    avg_par = sum(parallel_times) / len(parallel_times)

    print("\n" + "-"*60)
    print(f"\nAverage Sequential: {avg_seq:.4f}s")
    print(f"Average Parallel:   {avg_par:.4f}s")
    print(f"Average Speedup:    {avg_seq/avg_par:.2f}x" if avg_par > 0 else "Average Speedup: N/A")

    return {
        "sequential_avg": avg_seq,
        "parallel_avg": avg_par,
        "speedup": avg_seq / avg_par if avg_par > 0 else 1.0,
        "iterations": num_iterations
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python benchmark_tests.py <skill_directory> [--output <file>] [--profile] [--compare]")
        print("\nOptions:")
        print("  --output <file>  Save results to JSON file")
        print("  --profile        Run profiler on each script")
        print("  --compare        Run detailed comparison of execution modes")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    # Parse options
    output_file = None
    run_profile = False
    run_compare = False

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = Path(sys.argv[idx + 1])

    if "--profile" in sys.argv:
        run_profile = True

    if "--compare" in sys.argv:
        run_compare = True

    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)

    # Run benchmarks
    report = run_benchmarks(skill_path)

    # Run comparison if requested
    if run_compare:
        compare_execution_modes(skill_path)

    # Run profiling if requested
    if run_profile:
        print("\n" + "="*60)
        print("PROFILING RESULTS")
        print("="*60)

        scripts = [
            ("Quick Validation", validate_skill),
            ("Static Analysis", analyze_skill),
            ("Eval Review", review_evals),
        ]

        for name, func in scripts:
            print(f"\n{name}:")
            print("-"*40)
            profile_output = profile_script(func, skill_path, name)
            print(profile_output)

    # Generate report
    generate_report(report, output_file)

    # Exit with appropriate code
    all_success = all(r.success for r in report.results)
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
