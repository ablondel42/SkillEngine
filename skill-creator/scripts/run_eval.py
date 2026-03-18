#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes Claude to trigger (read the skill)
for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import select
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/.

    Mimics how Claude Code discovers its project root, so the command file
    we create ends up where claude -p will look for it.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def create_command_file(
    project_root: Path,
    skill_name: str,
    skill_description: str,
    unique_id: str,
) -> Path:
    """Create a temporary command file for the skill.

    Args:
        project_root: Root directory of the project.
        skill_name: Name of the skill.
        skill_description: Description of the skill.
        unique_id: Unique identifier for this command file.

    Returns:
        Path to the created command file.
    """
    clean_name = f"{skill_name}-skill-{unique_id}"
    project_commands_dir = project_root / ".claude" / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"

    project_commands_dir.mkdir(parents=True, exist_ok=True)

    # Use YAML block scalar to avoid breaking on quotes in description
    indented_desc = "\n  ".join(skill_description.split("\n"))
    command_content = (
        f"---\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {skill_description}\n"
    )
    command_file.write_text(command_content)

    return command_file


def parse_stream_event(line: str) -> dict | None:
    """Parse a JSON stream event from a line.

    Args:
        line: A line from the stream output.

    Returns:
        Parsed event dictionary, or None if parsing fails.
    """
    line = line.strip()
    if not line:
        return None

    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def check_skill_invocation(event: dict) -> tuple[str | None, bool]:
    """Check if event indicates a skill tool invocation starting.

    Args:
        event: Parsed stream event.

    Returns:
        Tuple of (tool_name, is_skill_related).
        tool_name is "Skill" or "Read" if detected, None otherwise.
        is_skill_related is True if a non-skill tool was found.
    """
    se = event.get("event", {})
    se_type = se.get("type", "")

    if se_type == "content_block_start":
        cb = se.get("content_block", {})
        if cb.get("type") == "tool_use":
            tool_name = cb.get("name", "")
            if tool_name in ("Skill", "Read"):
                return (tool_name, False)
            else:
                return (None, True)

    return (None, False)


def check_skill_md_read(
    accumulated_json: str,
    clean_name: str,
) -> bool:
    """Check if accumulated JSON contains the skill identifier.

    Args:
        accumulated_json: Accumulated JSON from delta events.
        clean_name: The skill's unique identifier name.

    Returns:
        True if the skill identifier is found in the JSON.
    """
    return clean_name in accumulated_json


def check_workflow_followed(
    event: dict,
    clean_name: str,
    pending_tool_name: str | None,
    accumulated_json: str,
) -> tuple[bool | None, str | None, str]:
    """Check if the workflow was followed based on stream events.

    Args:
        event: Parsed stream event.
        clean_name: The skill's unique identifier name.
        pending_tool_name: Currently pending tool name (if any).
        accumulated_json: Accumulated JSON from delta events.

    Returns:
        Tuple of (triggered, new_pending_tool_name, new_accumulated_json).
        triggered is True if skill detected, False if wrong tool,
        or None if still waiting for more data.
    """
    if event.get("type") != "stream_event":
        return (None, pending_tool_name, accumulated_json)

    se = event.get("event", {})
    se_type = se.get("type", "")

    if se_type == "content_block_delta" and pending_tool_name:
        delta = se.get("delta", {})
        if delta.get("type") == "input_json_delta":
            accumulated_json += delta.get("partial_json", "")
            if clean_name in accumulated_json:
                return (True, pending_tool_name, accumulated_json)

    elif se_type in ("content_block_stop", "message_stop"):
        if pending_tool_name:
            return (clean_name in accumulated_json, None, accumulated_json)
        if se_type == "message_stop":
            return (False, None, accumulated_json)

    return (None, pending_tool_name, accumulated_json)


def _check_assistant_message(event: dict, clean_name: str) -> tuple[bool, bool]:
    """Check assistant message for skill trigger.

    Args:
        event: Parsed stream event.
        clean_name: The skill's unique identifier name.

    Returns:
        Tuple of (found_skill, found_other_tool).
    """
    message = event.get("message", {})
    for content_item in message.get("content", []):
        if content_item.get("type") != "tool_use":
            continue
        tool_name = content_item.get("name", "")
        tool_input = content_item.get("input", {})
        if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
            return (True, False)
        elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
            return (True, False)
        return (False, True)
    return (False, False)


def detect_skill_trigger(
    event: dict,
    clean_name: str,
    pending_tool_name: str | None,
    accumulated_json: str,
) -> tuple[bool, str | None, str]:
    """Detect if a stream event indicates skill triggering.

    Args:
        event: Parsed stream event.
        clean_name: The skill's unique identifier name.
        pending_tool_name: Currently pending tool name (if any).
        accumulated_json: Accumulated JSON from delta events.

    Returns:
        Tuple of (triggered, new_pending_tool_name, new_accumulated_json).
        triggered is True if skill was detected, False if wrong tool,
        or None if still waiting for more data.
    """
    # Check for skill invocation start
    if event.get("type") == "stream_event":
        tool_name, is_wrong_tool = check_skill_invocation(event)
        if is_wrong_tool:
            return (False, None, "")
        if tool_name:
            return (None, tool_name, "")

    # Check workflow progress (delta events, stop events)
    triggered, pending_tool_name, accumulated_json = check_workflow_followed(
        event, clean_name, pending_tool_name, accumulated_json
    )
    if triggered is not None:
        return (triggered, pending_tool_name, accumulated_json)

    # Fallback: full assistant message
    if event.get("type") == "assistant":
        found_skill, found_other = _check_assistant_message(event, clean_name)
        if found_skill:
            return (True, None, accumulated_json)
        if found_other:
            return (False, None, accumulated_json)

    if event.get("type") == "result":
        return (False, None, accumulated_json)

    return (None, pending_tool_name, accumulated_json)


def _process_stream_buffer(
    buffer: str,
    clean_name: str,
    pending_tool_name: str | None,
    accumulated_json: str,
) -> tuple[bool | None, str | None, str, str]:
    """Process lines from stream buffer and check for skill trigger.

    Args:
        buffer: Accumulated output buffer.
        clean_name: The skill's unique identifier name.
        pending_tool_name: Currently pending tool name (if any).
        accumulated_json: Accumulated JSON from delta events.

    Returns:
        Tuple of (triggered, new_pending_tool_name, new_accumulated_json, remaining_buffer).
        triggered is True/False if decision reached, None to continue.
    """
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        event = parse_stream_event(line)
        if event is None:
            continue

        triggered, pending_tool_name, accumulated_json = detect_skill_trigger(
            event, clean_name, pending_tool_name, accumulated_json
        )
        if triggered is not None:
            return (triggered, pending_tool_name, accumulated_json, buffer)

    return (None, pending_tool_name, accumulated_json, buffer)


def _read_process_output(process, timeout: float, start_time: float) -> tuple[str, bool]:
    """Read output from process with timeout.

    Args:
        process: Subprocess to read from.
        timeout: Timeout in seconds.
        start_time: Start time of the process.

    Returns:
        Tuple of (output_chunk, process_ended).
    """
    if process.poll() is not None:
        remaining = process.stdout.read()
        if remaining:
            return (remaining.decode("utf-8", errors="replace"), True)
        return ("", True)

    ready, _, _ = select.select([process.stdout], [], [], 1.0)
    if not ready:
        return ("", False)

    chunk = os.read(process.stdout.fileno(), 8192)
    if not chunk:
        return ("", True)

    return (chunk.decode("utf-8", errors="replace"), False)


def _setup_process(cmd: list[str], project_root: str) -> subprocess.Popen:
    """Set up subprocess for command execution.

    Args:
        cmd: Command to execute.
        project_root: Root directory for execution.

    Returns:
        Configured subprocess.Popen instance.
    """
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=project_root,
        env=env,
    )


def _execute_command_and_monitor(
    cmd: list[str],
    project_root: str,
    timeout: int,
    clean_name: str,
) -> bool:
    """Execute command and monitor output for skill trigger.

    Args:
        cmd: Command to execute.
        project_root: Root directory for execution.
        timeout: Timeout in seconds.
        clean_name: The skill's unique identifier name.

    Returns:
        True if skill was triggered, False otherwise.
    """
    process = _setup_process(cmd, project_root)

    start_time = time.time()
    buffer = ""
    pending_tool_name: str | None = None
    accumulated_json = ""

    try:
        while time.time() - start_time < timeout:
            chunk, ended = _read_process_output(process, timeout, start_time)
            buffer += chunk
            if ended:
                break

            triggered, pending_tool_name, accumulated_json, buffer = _process_stream_buffer(
                buffer, clean_name, pending_tool_name, accumulated_json
            )
            if triggered is not None:
                return triggered
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()

    return False


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a command file in .claude/commands/ so it appears in Claude's
    available_skills list, then runs `claude -p` with the raw query.
    Uses --include-partial-messages to detect triggering early from
    stream events (content_block_start) rather than waiting for the
    full assistant message, which only arrives after tool execution.

    Args:
        query: The query to test.
        skill_name: Name of the skill.
        skill_description: Description of the skill.
        timeout: Timeout in seconds.
        project_root: Root directory of the project.
        model: Optional model override.

    Returns:
        True if the skill was triggered, False otherwise.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    command_file = create_command_file(
        Path(project_root), skill_name, skill_description, unique_id
    )

    try:
        cmd = [
            "claude",
            "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd.extend(["--model", model])

        return _execute_command_and_monitor(cmd, project_root, timeout, clean_name)
    finally:
        if command_file.exists():
            command_file.unlink()


def _collect_future_results(
    future_to_info: dict,
) -> tuple[dict[str, list[bool]], dict[str, dict]]:
    """Collect results from completed futures.

    Args:
        future_to_info: Mapping of futures to (item, run_idx) tuples.

    Returns:
        Tuple of (query_triggers, query_items) dictionaries.
    """
    query_triggers: dict[str, list[bool]] = {}
    query_items: dict[str, dict] = {}

    for future in as_completed(future_to_info):
        item, _ = future_to_info[future]
        query = item["query"]
        query_items[query] = item
        if query not in query_triggers:
            query_triggers[query] = []
        try:
            query_triggers[query].append(future.result())
        except Exception as e:
            print(f"Warning: query failed: {e}", file=sys.stderr)
            query_triggers[query].append(False)

    return query_triggers, query_items


def _submit_eval_tasks(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    timeout: int,
    project_root: str,
    num_workers: int,
    runs_per_query: int,
    model: str | None,
) -> tuple[dict, dict]:
    """Submit evaluation tasks to process pool and collect results.

    Args:
        eval_set: List of evaluation queries.
        skill_name: Name of the skill.
        description: Skill description.
        timeout: Timeout per query in seconds.
        project_root: Root directory of the project.
        num_workers: Number of parallel workers.
        runs_per_query: Number of runs per query.
        model: Optional model override.

    Returns:
        Tuple of (query_triggers, query_items) dictionaries.
    """
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

    return _collect_future_results(future_to_info)


def _build_result_entry(
    query: str,
    triggers: list[bool],
    item: dict,
    trigger_threshold: float,
) -> dict:
    """Build a result entry for a single query.

    Args:
        query: The query string.
        triggers: List of trigger results from multiple runs.
        item: Original evaluation item.
        trigger_threshold: Threshold for determining pass/fail.

    Returns:
        Dictionary containing query result data.
    """
    trigger_rate = sum(triggers) / len(triggers)
    should_trigger = item["should_trigger"]
    if should_trigger:
        did_pass = trigger_rate >= trigger_threshold
    else:
        did_pass = trigger_rate < trigger_threshold

    return {
        "query": query,
        "should_trigger": should_trigger,
        "trigger_rate": trigger_rate,
        "triggers": sum(triggers),
        "runs": len(triggers),
        "pass": did_pass,
    }


def _build_eval_output(
    skill_name: str,
    description: str,
    results: list[dict],
) -> dict:
    """Build the final evaluation output dictionary.

    Args:
        skill_name: Name of the skill.
        description: Skill description.
        results: List of result entries.

    Returns:
        Dictionary containing skill_name, description, results, and summary.
    """
    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results.

    Args:
        eval_set: List of evaluation queries.
        skill_name: Name of the skill.
        description: Skill description.
        num_workers: Number of parallel workers.
        timeout: Timeout per query in seconds.
        project_root: Root directory of the project.
        runs_per_query: Number of runs per query.
        trigger_threshold: Threshold for determining pass/fail.
        model: Optional model override.

    Returns:
        Dictionary containing skill_name, description, results, and summary.
    """
    query_triggers, query_items = _submit_eval_tasks(
        eval_set=eval_set,
        skill_name=skill_name,
        description=description,
        timeout=timeout,
        project_root=str(project_root),
        num_workers=num_workers,
        runs_per_query=runs_per_query,
        model=model,
    )

    results = [
        _build_result_entry(query, triggers, query_items[query], trigger_threshold)
        for query, triggers in query_triggers.items()
    ]

    return _build_eval_output(skill_name, description, results)


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use for claude -p (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
