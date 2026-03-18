#!/usr/bin/env python3
"""
Automated Trigger Test Runner.

Spawns Task subagents for each trigger test, collects skill invocation data,
grades workflow compliance, and generates results reports.

Usage: python run_trigger_tests.py <skill_directory> [--skill-name <name>]

The script will:
1. Load test cases from skill's evals/trigger_tests.json or use defaults
2. Spawn a Task subagent for each test case
3. Monitor skill tool invocation
4. Grade workflow compliance (interview, token granularity, etc.)
5. Generate comprehensive results report
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class TriggerTestResult:
    """Result of a single trigger test."""
    test_name: str
    prompt: str
    should_trigger: bool
    actually_triggered: bool = False
    skill_invoked: bool = False
    skill_md_read: bool = False
    workflow_followed: bool = False
    interview_conducted: bool = False
    code_before_interview: bool = False
    execution_time: float = 0.0
    subagent_output: str = ""
    pass_fail: bool = False
    notes: str = ""


@dataclass
class TriggerTestReport:
    """Complete report of all trigger tests."""
    skill_name: str
    skill_path: str
    test_date: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    trigger_success_rate: float = 0.0
    workflow_compliance_rate: float = 0.0
    total_execution_time: float = 0.0
    results: list[TriggerTestResult] = field(default_factory=list)


# Default trigger test cases based on research findings
DEFAULT_TRIGGER_TESTS = [
    {
        "name": "explicit-need-statement",
        "prompt": "I need a design system for my React app. Can you help me build it?",
        "should_trigger": True,
        "description": "Test the winning formula: 'I need a [domain] for my [context]'"
    },
    {
        "name": "component-library-request",
        "prompt": "I want to create a component library with consistent styling for my dashboard.",
        "should_trigger": True,
        "description": "Test related keyword: 'component library'"
    },
    {
        "name": "ui-consistency-request",
        "prompt": "My app's UI looks inconsistent. I need to make all my components look unified.",
        "should_trigger": True,
        "description": "Test casual mention: 'make my app look consistent'"
    },
    {
        "name": "negative-pdf-task",
        "prompt": "Convert this PDF file to text format so I can read it more easily.",
        "should_trigger": False,
        "description": "Negative case: unrelated task should not trigger design-system skill"
    },
    {
        "name": "negative-python-task",
        "prompt": "Write a Python script to parse CSV files and generate reports.",
        "should_trigger": False,
        "description": "Negative case: programming task should not trigger design-system skill"
    }
]


def load_trigger_tests(skill_path: Path) -> list[dict]:
    """Load trigger tests from skill directory or use defaults."""
    trigger_test_file = skill_path / "evals" / "trigger_tests.json"

    if trigger_test_file.exists():
        try:
            data = json.loads(trigger_test_file.read_text())
            return data.get("tests", DEFAULT_TRIGGER_TESTS)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Failed to load trigger_tests.json: {e}")
            print("Using default test cases instead.")

    return DEFAULT_TRIGGER_TESTS


def spawn_subagent_task(prompt: str, skill_name: Optional[str] = None) -> tuple[str, float]:
    """
    Spawn a Task subagent with the given prompt.

    This function would typically use the Task tool to spawn a subagent.
    For now, it simulates the subagent execution by running a command.

    Returns:
        Tuple of (output_text, execution_time_seconds)
    """
    start_time = time.time()

    # In a real implementation, this would spawn a Task subagent
    # For simulation, we'll use a placeholder approach
    # The actual implementation would depend on the Task tool API

    print(f"  Spawning subagent with prompt: {prompt[:80]}...")

    # Simulate subagent execution (replace with actual Task tool call)
    # This is a placeholder - in production, you'd use the Task tool
    try:
        # Example: Call a test script that simulates subagent behavior
        result = subprocess.run(
            ["python3", "-c", f"print('Simulated subagent response for: {prompt[:50]}')"],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        output = "Error: Subagent execution timed out"
    except Exception as e:
        output = f"Error: {str(e)}"

    elapsed_time = time.time() - start_time
    return output, elapsed_time


def analyze_skill_invocation(subagent_output: str, skill_name: str) -> dict:
    """
    Analyze subagent output to determine if skill was invoked.

    Returns dict with:
    - skill_invoked: bool
    - skill_md_read: bool
    - workflow_followed: bool
    - interview_conducted: bool
    - code_before_interview: bool
    """
    analysis = {
        "skill_invoked": False,
        "skill_md_read": False,
        "workflow_followed": False,
        "interview_conducted": False,
        "code_before_interview": False
    }

    output_lower = subagent_output.lower()

    # Check for skill invocation patterns
    skill_invocation_patterns = [
        f"using the {skill_name} skill",
        f"invoking {skill_name}",
        f"skill: {skill_name}",
        f"loading {skill_name}",
        "i'll use the skill",
        "let me invoke the skill"
    ]
    analysis["skill_invoked"] = any(pattern in output_lower for pattern in skill_invocation_patterns)

    # Check for SKILL.md read patterns
    skill_md_patterns = [
        "reading skill.md",
        "loading skill.md",
        "per skill.md",
        "according to skill.md",
        "the skill specifies",
        "following the skill workflow"
    ]
    analysis["skill_md_read"] = any(pattern in output_lower for pattern in skill_md_patterns)

    # Check for workflow compliance
    workflow_patterns = [
        "step 1", "step 2", "step 3",
        "phase 1", "phase 2",
        "first, i need to",
        "before we proceed",
        "let me start by"
    ]
    analysis["workflow_followed"] = any(pattern in output_lower for pattern in workflow_patterns)

    # Check for interview questions
    interview_patterns = [
        "can you tell me",
        "what kind of",
        "do you prefer",
        "i have a few questions",
        "before i start, i need to understand",
        "let me ask you some questions"
    ]
    analysis["interview_conducted"] = any(pattern in output_lower for pattern in interview_patterns)

    # Check for code before interview (violation)
    # Look for code blocks before interview patterns
    code_block_idx = output_lower.find("```")
    interview_idx = output_lower.find("question")

    if code_block_idx != -1:
        # Check if there's actual code (not just markdown)
        if any(lang in output_lower[code_block_idx:code_block_idx+20]
               for lang in ["python", "javascript", "typescript", "react", "tsx", "jsx"]):
            if interview_idx == -1 or code_block_idx < interview_idx:
                analysis["code_before_interview"] = True

    return analysis


def grade_test_result(result: TriggerTestResult) -> bool:
    """
    Grade a single test result.

    Pass criteria:
    - If should_trigger: skill must be invoked and workflow followed
    - If should_not_trigger: skill must NOT be invoked
    """
    if result.should_trigger:
        # For trigger cases, check:
        # 1. Skill was invoked
        # 2. Workflow was followed (if invoked)
        # 3. No code before interview (if interview required)

        if not result.skill_invoked:
            result.notes = "Skill was not invoked when it should have been"
            return False

        if not result.workflow_followed:
            result.notes = "Skill invoked but workflow not followed"
            return False

        if result.code_before_interview:
            result.notes = "Code generated before interview - workflow violation"
            return False

        return True
    else:
        # For negative cases, skill should NOT be invoked
        if result.skill_invoked:
            result.notes = "Skill was invoked when it should NOT have been"
            return False

        return True


def run_trigger_test(test_case: dict, skill_name: str) -> TriggerTestResult:
    """Run a single trigger test and return results."""
    print(f"\n  Running test: {test_case['name']}")
    print(f"  Description: {test_case.get('description', 'N/A')}")

    result = TriggerTestResult(
        test_name=test_case["name"],
        prompt=test_case["prompt"],
        should_trigger=test_case["should_trigger"]
    )

    # Spawn subagent
    output, elapsed = spawn_subagent_task(test_case["prompt"], skill_name)
    result.subagent_output = output
    result.execution_time = elapsed

    # Analyze skill invocation
    analysis = analyze_skill_invocation(output, skill_name)
    result.skill_invoked = analysis["skill_invoked"]
    result.skill_md_read = analysis["skill_md_read"]
    result.workflow_followed = analysis["workflow_followed"]
    result.interview_conducted = analysis["interview_conducted"]
    result.code_before_interview = analysis["code_before_interview"]

    # Grade the test
    result.pass_fail = grade_test_result(result)

    print(f"  Result: {'✅ PASS' if result.pass_fail else '❌ FAIL'}")
    print(f"  Skill invoked: {result.skill_invoked} (expected: {result.should_trigger})")
    print(f"  Workflow followed: {result.workflow_followed}")
    print(f"  Time: {elapsed:.2f}s")

    return result


def generate_report(report: TriggerTestReport, output_dir: Path) -> Path:
    """Generate comprehensive test report."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON report
    json_report = {
        "skill_name": report.skill_name,
        "skill_path": report.skill_path,
        "test_date": report.test_date,
        "summary": {
            "total_tests": report.total_tests,
            "passed": report.passed_tests,
            "failed": report.failed_tests,
            "trigger_success_rate": report.trigger_success_rate,
            "workflow_compliance_rate": report.workflow_compliance_rate,
            "total_execution_time": report.total_execution_time
        },
        "results": [
            {
                "test_name": r.test_name,
                "prompt": r.prompt,
                "should_trigger": r.should_trigger,
                "pass_fail": r.pass_fail,
                "skill_invoked": r.skill_invoked,
                "workflow_followed": r.workflow_followed,
                "interview_conducted": r.interview_conducted,
                "code_before_interview": r.code_before_interview,
                "execution_time": r.execution_time,
                "notes": r.notes
            }
            for r in report.results
        ]
    }

    json_path = output_dir / "trigger_test_results.json"
    json_path.write_text(json.dumps(json_report, indent=2))

    # Markdown report
    md_content = generate_markdown_report(report)
    md_path = output_dir / "trigger_test_report.md"
    md_path.write_text(md_content)

    # Console summary
    print_console_summary(report)

    return json_path


def generate_markdown_report(report: TriggerTestReport) -> str:
    """Generate markdown report for human reading."""
    lines = [
        "# Trigger Test Report",
        "",
        f"**Skill:** {report.skill_name}",
        f"**Path:** {report.skill_path}",
        f"**Date:** {report.test_date}",
        "",
        "## Summary",
        "",
        f"- **Total Tests:** {report.total_tests}",
        f"- **Passed:** {report.passed_tests}",
        f"- **Failed:** {report.failed_tests}",
        f"- **Trigger Success Rate:** {report.trigger_success_rate:.1f}%",
        f"- **Workflow Compliance Rate:** {report.workflow_compliance_rate:.1f}%",
        f"- **Total Execution Time:** {report.total_execution_time:.2f}s",
        "",
        "## Test Results",
        "",
        "| Test | Expected | Triggered | Workflow | Interview | Pass/Fail |",
        "|------|----------|-----------|----------|-----------|-----------|"
    ]

    for r in report.results:
        expected = "Yes" if r.should_trigger else "No"
        triggered = "✅ Yes" if r.skill_invoked else "❌ No"
        workflow = "✅" if r.workflow_followed else "❌"
        interview = "✅" if r.interview_conducted else "N/A"
        status = "✅ PASS" if r.pass_fail else "❌ FAIL"

        lines.append(
            f"| {r.test_name} | {expected} | {triggered} | {workflow} | {interview} | {status} |"
        )

    lines.extend([
        "",
        "## Detailed Results",
        ""
    ])

    for r in report.results:
        lines.extend([
            f"### {r.test_name}",
            "",
            f"**Prompt:** {r.prompt}",
            "",
            f"**Expected to trigger:** {'Yes' if r.should_trigger else 'No'}",
            f"**Actually triggered:** {'Yes' if r.skill_invoked else 'No'}",
            f"**Workflow followed:** {'Yes' if r.workflow_followed else 'No'}",
            f"**Interview conducted:** {'Yes' if r.interview_conducted else 'No'}",
            f"**Code before interview:** {'Yes (VIOLATION)' if r.code_before_interview else 'No'}",
            "",
            f"**Result:** {'✅ PASS' if r.pass_fail else '❌ FAIL'}",
            ""
        ])
        if r.notes:
            lines.append(f"**Notes:** {r.notes}")
            lines.append("")

    lines.extend([
        "## Recommendations",
        "",
    ])

    if report.trigger_success_rate < 100:
        lines.append("- Improve skill description to include more trigger keywords")
    if report.workflow_compliance_rate < 100:
        lines.append("- Review SKILL.md workflow instructions for clarity")
    if report.passed_tests == report.total_tests:
        lines.append("- All tests passed! Skill is ready for production.")

    lines.append("")

    return "\n".join(lines)


def print_console_summary(report: TriggerTestReport):
    """Print summary to console."""
    print("\n" + "="*60)
    print("TRIGGER TEST RESULTS")
    print("="*60)
    print(f"\nSkill: {report.skill_name}")
    print(f"Date: {report.test_date}")
    print(f"\nTotal Tests: {report.total_tests}")
    print(f"Passed: {report.passed_tests}")
    print(f"Failed: {report.failed_tests}")
    print(f"Trigger Success Rate: {report.trigger_success_rate:.1f}%")
    print(f"Workflow Compliance Rate: {report.workflow_compliance_rate:.1f}%")
    print(f"Total Execution Time: {report.total_execution_time:.2f}s")
    print("\n" + "-"*60)

    for r in report.results:
        status = "✅ PASS" if r.pass_fail else "❌ FAIL"
        print(f"{status} - {r.test_name}")
        if r.notes:
            print(f"       Note: {r.notes}")

    print("="*60)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python run_trigger_tests.py <skill_directory> [--skill-name <name>]")
        print("\nOptions:")
        print("  --skill-name <name>  Override skill name (default: from SKILL.md)")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    script_dir = Path(__file__).parent

    # Parse optional arguments
    skill_name_override = None
    if "--skill-name" in sys.argv:
        idx = sys.argv.index("--skill-name")
        if idx + 1 < len(sys.argv):
            skill_name_override = sys.argv[idx + 1]

    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        sys.exit(1)

    # Extract skill name from SKILL.md or use override
    if skill_name_override:
        skill_name = skill_name_override
    else:
        import re
        content = (skill_path / "SKILL.md").read_text()
        name_match = re.search(r'name:\s*["\']?([a-z0-9-]+)["\']?', content[:500])
        skill_name = name_match.group(1) if name_match else skill_path.name

    print("="*60)
    print("AUTOMATED TRIGGER TEST RUNNER")
    print("="*60)
    print(f"\nSkill: {skill_name}")
    print(f"Path: {skill_path}")

    # Load test cases
    test_cases = load_trigger_tests(skill_path)
    print(f"\nLoaded {len(test_cases)} test cases")

    # Run tests
    report = TriggerTestReport(
        skill_name=skill_name,
        skill_path=str(skill_path),
        test_date=datetime.now().isoformat()
    )

    for test_case in test_cases:
        result = run_trigger_test(test_case, skill_name)
        report.results.append(result)
        report.total_tests += 1
        report.total_execution_time += result.execution_time

        if result.pass_fail:
            report.passed_tests += 1
        else:
            report.failed_tests += 1

        if result.should_trigger and result.skill_invoked:
            report.trigger_success_rate += (100 / max(1, sum(1 for t in test_cases if t["should_trigger"])))

        if result.skill_invoked and result.workflow_followed:
            report.workflow_compliance_rate += (100 / max(1, sum(1 for t in test_cases if t["should_trigger"] and t.get("should_trigger", True))))

    # Round rates
    report.trigger_success_rate = round(report.trigger_success_rate, 1)
    report.workflow_compliance_rate = round(report.workflow_compliance_rate, 1)
    report.total_execution_time = round(report.total_execution_time, 2)

    # Generate report
    output_dir = skill_path / "eval-outputs" / "trigger-tests"
    report_path = generate_report(report, output_dir)

    print(f"\nReport saved to: {report_path}")

    # Exit with appropriate code
    sys.exit(0 if report.passed_tests == report.total_tests else 1)


if __name__ == "__main__":
    main()
