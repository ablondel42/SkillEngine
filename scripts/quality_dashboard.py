#!/usr/bin/env python3
"""Generate code quality dashboard and trend reports.

Creates visual HTML dashboard showing:
- Quality score trends over time
- Issue distribution by category/severity
- File-level quality metrics
- Improvement recommendations

Usage:
    python scripts/quality_dashboard.py [--output dashboard.html]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_audit_history(history_file: Path) -> list[dict]:
    """Load historical audit results."""
    if not history_file.exists():
        return []

    with open(history_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_audit_history(history: list[dict], history_file: Path) -> None:
    """Save audit results to history."""
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def generate_trend_chart_data(history: list[dict]) -> str:
    """Generate Chart.js data for trend chart."""
    if not history:
        return "[]"

    labels = []
    scores = []

    for entry in history[-30:]:  # Last 30 audits
        date = entry.get("timestamp", "")[:10]
        labels.append(f'"{date}"')
        scores.append(str(entry.get("score", 0)))

    return f"""
        labels: [{', '.join(labels)}],
        datasets: [{{
            label: 'Quality Score',
            data: [{', '.join(scores)}],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
            fill: true
        }}]
    """


def generate_category_chart(summary: dict) -> str:
    """Generate Chart.js data for category distribution."""
    by_category = summary.get("by_category", {})

    if not by_category:
        return "[]"

    labels = [f'"{k}"' for k in by_category.keys()]
    data = [str(v) for v in by_category.values()]
    colors = [
        "rgba(255, 99, 132, 0.7)",
        "rgba(255, 159, 64, 0.7)",
        "rgba(255, 205, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(153, 102, 255, 0.7)",
    ]

    return f"""
        labels: [{', '.join(labels)}],
        datasets: [{{
            data: [{', '.join(data)}],
            backgroundColor: [{', '.join(colors[:len(data)])}]
        }}]
    """


def generate_severity_chart(summary: dict) -> str:
    """Generate Chart.js data for severity distribution."""
    by_severity = summary.get("by_severity", {})

    if not by_severity:
        return "[]"

    labels = [f'"{k.upper()}"' for k in by_severity.keys()]
    data = [str(v) for v in by_severity.values()]
    colors = {
        "critical": "rgba(220, 53, 69, 0.7)",
        "high": "rgba(255, 193, 7, 0.7)",
        "medium": "rgba(255, 167, 38, 0.7)",
        "low": "rgba(40, 167, 69, 0.7)",
    }

    bg_colors = [colors.get(k.lower(), "rgba(108, 117, 125, 0.7)") for k in by_severity.keys()]

    return f"""
        labels: [{', '.join(labels)}],
        datasets: [{{
            data: [{', '.join(data)}],
            backgroundColor: [{', '.join(bg_colors)}]
        }}]
    """


def generate_dashboard_html(
    current_result: dict,
    history: list[dict],
    output_path: Path,
) -> None:
    """Generate HTML dashboard."""
    trend_data = generate_trend_chart_data(history)
    category_data = generate_category_chart(current_result.get("summary", {}))
    severity_data = generate_severity_chart(current_result.get("summary", {}))

    score = current_result.get("score", 0)
    score_class = "excellent" if score >= 90 else "good" if score >= 70 else "needs-work" if score >= 50 else "poor"

    # Generate findings table rows
    findings_rows = ""
    for finding in current_result.get("findings", [])[:50]:
        severity_icon = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }.get(finding.get("severity", ""), "⚪")

        findings_rows += f"""
            <tr class="finding-row">
                <td><span class="severity-badge {finding.get('severity', '')}">{severity_icon} {finding.get('severity', '').upper()}</span></td>
                <td>{finding.get('category', '')}</td>
                <td><code>{finding.get('file', '')}:{finding.get('line', 0)}</code></td>
                <td>{finding.get('message', '')}</td>
                <td><em>{finding.get('suggestion', '')}</em></td>
            </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Quality Dashboard - SkillEngine</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #faf9f5;
            --bg-card: #ffffff;
            --text-primary: #141413;
            --text-secondary: #6b6b6a;
            --border: #e8e6dc;
            --success: #788c5d;
            --warning: #d97706;
            --danger: #c44;
            --info: #6a9bcc;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Lora', Georgia, serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            background: var(--bg-card);
            padding: 20px 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }}
        h1 {{ font-family: 'Poppins', sans-serif; font-size: 1.75rem; }}
        .timestamp {{ color: var(--text-secondary); font-size: 0.875rem; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 20px;
            border: 1px solid var(--border);
        }}
        .card h2 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            margin-bottom: 15px;
            color: var(--text-secondary);
        }}
        .score-display {{
            text-align: center;
            padding: 30px;
        }}
        .score-number {{
            font-size: 4rem;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
        }}
        .score-number.excellent {{ color: var(--success); }}
        .score-number.good {{ color: var(--info); }}
        .score-number.needs-work {{ color: var(--warning); }}
        .score-number.poor {{ color: var(--danger); }}
        .score-label {{
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-top: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: var(--bg-primary);
            border-radius: 6px;
        }}
        .stat-value {{
            font-size: 1.5rem;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
        }}
        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
        }}
        .chart-container {{
            position: relative;
            height: 250px;
        }}
        .findings-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }}
        .findings-table th {{
            background: var(--bg-primary);
            padding: 12px;
            text-align: left;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            border-bottom: 2px solid var(--border);
        }}
        .findings-table td {{
            padding: 12px;
            border-bottom: 1px solid var(--border);
        }}
        .findings-table tr:hover {{
            background: var(--bg-primary);
        }}
        .severity-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
        }}
        .severity-badge.critical {{ background: #fceaea; color: var(--danger); }}
        .severity-badge.high {{ background: #fef3c7; color: var(--warning); }}
        .severity-badge.medium {{ background: #fffbeb; color: #d97706; }}
        .severity-badge.low {{ background: #f0fdf4; color: var(--success); }}
        code {{
            background: var(--bg-primary);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.8rem;
        }}
        .table-container {{
            overflow-x: auto;
        }}
        .recommendations {{
            background: var(--bg-primary);
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}
        .recommendations h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }}
        .recommendations ul {{
            margin-left: 20px;
        }}
        .recommendations li {{
            margin-bottom: 5px;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Code Quality Dashboard</h1>
            <p class="timestamp">Generated: {current_result.get('timestamp', 'N/A')}</p>
        </header>

        <div class="grid">
            <div class="card">
                <h2>Overall Score</h2>
                <div class="score-display">
                    <div class="score-number {score_class}">{score}</div>
                    <div class="score-label">out of 100</div>
                </div>
            </div>

            <div class="card">
                <h2>Project Stats</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">{current_result.get('total_files', 0)}</div>
                        <div class="stat-label">Files</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{current_result.get('total_lines', 0):,}</div>
                        <div class="stat-label">Lines</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{current_result.get('summary', {}).get('functions_total', 0)}</div>
                        <div class="stat-label">Functions</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{current_result.get('summary', {}).get('doc_coverage', 0)}%</div>
                        <div class="stat-label">Doc Coverage</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Issues by Severity</h2>
                <div class="chart-container">
                    <canvas id="severityChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Issues by Category</h2>
                <div class="chart-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 20px;">
            <h2>Quality Trend</h2>
            <div class="chart-container" style="height: 300px;">
                <canvas id="trendChart"></canvas>
            </div>
        </div>

        <div class="card">
            <h2>Findings ({len(current_result.get('findings', []))} total)</h2>
            <div class="table-container">
                <table class="findings-table">
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Category</th>
                            <th>Location</th>
                            <th>Issue</th>
                            <th>Suggestion</th>
                        </tr>
                    </thead>
                    <tbody>
                        {findings_rows}
                    </tbody>
                </table>
            </div>

            <div class="recommendations">
                <h3>📋 Recommended Actions</h3>
                <ul>
                    {generate_recommendations(current_result)}
                </ul>
            </div>
        </div>

        <footer>
            <p>SkillEngine Code Quality Dashboard | Run 'python scripts/quality_dashboard.py' to update</p>
        </footer>
    </div>

    <script>
        // Trend Chart
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                {trend_data}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});

        // Severity Chart
        new Chart(document.getElementById('severityChart'), {{
            type: 'doughnut',
            data: {{
                {severity_data}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                {category_data}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def generate_recommendations(result: dict) -> str:
    """Generate prioritized recommendations based on audit results."""
    recommendations = []
    summary = result.get("summary", {})

    # Check for critical issues
    if summary.get("by_severity", {}).get("critical", 0) > 0:
        recommendations.append(
            "<strong>🔴 Critical:</strong> Fix bare except clauses immediately - "
            "they hide important errors"
        )

    # Check doc coverage
    doc_coverage = summary.get("doc_coverage", 0)
    if doc_coverage < 50:
        recommendations.append(
            f"<strong>📝 Documentation:</strong> Only {doc_coverage}% of functions have "
            "docstrings - aim for 90%+"
        )
    elif doc_coverage < 80:
        recommendations.append(
            f"<strong>📝 Documentation:</strong> {doc_coverage}% doc coverage - "
            "add docstrings to public functions"
        )

    # Check for complexity issues
    by_category = summary.get("by_category", {})
    if by_category.get("complexity", 0) > 5:
        recommendations.append(
            "<strong>🔧 Complexity:</strong> Multiple long functions detected - "
            "consider extracting helper functions"
        )

    # Check for duplication
    if by_category.get("duplication", 0) > 0:
        recommendations.append(
            "<strong>🔄 Duplication:</strong> Duplicate code found - "
            "extract to shared modules"
        )

    # General recommendations based on score
    score = result.get("score", 0)
    if score >= 90:
        recommendations.append(
            "<strong>✅ Excellent!</strong> Maintain current standards and "
            "address remaining low-priority items"
        )
    elif score >= 70:
        recommendations.append(
            "<strong>👍 Good progress!</strong> Focus on high-priority findings "
            "to reach excellent status"
        )
    else:
        recommendations.append(
            "<strong>⚠️ Needs attention:</strong> Run 'python scripts/fix_quality.py' "
            "to auto-fix common issues"
        )

    if not recommendations:
        recommendations.append("<em>No critical recommendations at this time</em>")

    return "\n".join(f"<li>{r}</li>" for r in recommendations)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate code quality dashboard"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="quality-dashboard.html",
        help="Output HTML file (default: quality-dashboard.html)",
    )
    parser.add_argument(
        "--history",
        default=".quality-history.json",
        help="History file for trends (default: .quality-history.json)",
    )
    parser.add_argument(
        "--audit-input",
        default="quality-audit.json",
        help="Input audit JSON file (default: quality-audit.json)",
    )

    args = parser.parse_args()

    # Load current audit result
    audit_path = Path(args.audit_input)
    if not audit_path.exists():
        print(f"❌ Audit file not found: {audit_path}")
        print("Run 'python scripts/audit_quality.py --output quality-audit.json' first")
        sys.exit(1)

    with open(audit_path, "r", encoding="utf-8") as f:
        current_result = json.load(f)

    # Load history
    history_path = Path(args.history)
    history = load_audit_history(history_path)

    # Add current result to history
    history.append({
        "timestamp": current_result.get("timestamp", datetime.now().isoformat()),
        "score": current_result.get("score", 0),
        "total_files": current_result.get("total_files", 0),
        "total_lines": current_result.get("total_lines", 0),
    })

    # Keep last 100 entries
    history = history[-100:]
    save_audit_history(history, history_path)

    # Generate dashboard
    output_path = Path(args.output)
    generate_dashboard_html(current_result, history, output_path)

    print(f"✅ Dashboard generated: {output_path}")
    print(f"📈 History updated: {history_path}")
    print(f"\nOpen {output_path} in your browser to view the dashboard")


if __name__ == "__main__":
    main()
