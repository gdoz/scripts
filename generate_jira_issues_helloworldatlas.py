import argparse
import csv
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Dict, List, Tuple

# Input CSV column names
COL_APPLICATION = "Application"
COL_PRODUCT_CATEGORY = "Product Category"
COL_PRODUCT_TYPE = "Product Type"
COL_PLATFORM = "Platform"
COL_LAYER = "Layer"
COL_OS = "OS"
COL_COMPLEXITY = "Complexity"
COL_LANGUAGE = "Language"
COL_STACK = "Stack"
COL_LABELS = "Labels"


def split_multi(value: str | None) -> List[str]:
    """Split a semicolon-separated string into a cleaned list of values.

    Example:
        " Go ; Python;; JS " -> ["Go", "Python", "JS"]
    """
    if not value:
        return []
    return [v.strip() for v in value.split(";") if v.strip()]


def read_source_rows(input_path: Path) -> List[Dict[str, str]]:
    """Read all rows from the source CSV as a list of dictionaries."""
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def compute_max_multi_counts(
    rows: Iterable[Dict[str, str]]
) -> Tuple[int, int]:
    """Compute the maximum number of Stack and Label values across all rows."""
    max_stack_count = 0
    max_label_count = 0

    for row in rows:
        app = (row.get(COL_APPLICATION) or "").strip()
        if not app:
            # Ignore lines without Application.
            continue

        stack_values = split_multi(row.get(COL_STACK, ""))
        label_values = split_multi(row.get(COL_LABELS, ""))

        max_stack_count = max(max_stack_count, len(stack_values))
        max_label_count = max(max_label_count, len(label_values))

    return max_stack_count, max_label_count


def build_header(max_stack_count: int, max_label_count: int) -> List[str]:
    """Build the header row for the output CSV file."""
    base_columns = [
        "Issue Type",
        "Summary",
        "Description",
        "Application",
        "Product Category",
        "Product Type",
        "Platform",
        "Layer",
        "OS",
        "Complexity",
        "Language",
        "Components",
        "Priority",
    ]

    # Jira multi-value behavior: multiple columns with the same name map to
    # multiple values of the same field (e.g., Stack, Labels).
    stack_columns = ["Stack"] * max_stack_count if max_stack_count > 0 else []
    label_columns = ["Label"] * max_label_count if max_label_count > 0 else []

    return base_columns + stack_columns + label_columns


def build_base_row(
    issue_type: str,
    summary: str,
    description: str,
    app: str,
    product_category: str,
    product_type: str,
    platform: str,
    layer: str,
    os_value: str,
    complexity: str,
    language: str,
    components: str,
    priority: str,
) -> List[str]:
    """Build the fixed part of an issue row (before Stack/Label cells)."""
    return [
        issue_type,
        summary,
        description,
        app,
        product_category,
        product_type,
        platform,
        layer,
        os_value,
        complexity,
        language,
        components,
        priority,
    ]


def generate_issue_rows_for_application(
    row: Dict[str, str],
    max_stack_count: int,
    max_label_count: int,
) -> List[List[str]]:
    """Generate all issue rows for a single application."""
    app = (row.get(COL_APPLICATION) or "").strip()
    if not app:
        return []

    product_category = (row.get(COL_PRODUCT_CATEGORY) or "").strip()
    product_type = (row.get(COL_PRODUCT_TYPE) or "").strip()
    platform = (row.get(COL_PLATFORM) or "").strip()
    layer = (row.get(COL_LAYER) or "").strip()
    os_value = (row.get(COL_OS) or "").strip()
    complexity = (row.get(COL_COMPLEXITY) or "").strip()
    language = (row.get(COL_LANGUAGE) or "").strip()
    stack_raw = (row.get(COL_STACK) or "").strip()
    labels_raw = (row.get(COL_LABELS) or "").strip()

    stack_values = split_multi(stack_raw)
    label_values = split_multi(labels_raw)

    # Fill fixed arrays for repeated Stack/Label columns.
    stack_cells = stack_values + [""] * max(0, max_stack_count - len(stack_values))
    label_cells = label_values + [""] * max(0, max_label_count - len(label_values))

    # All issues share these fields except type/summary/description/components.
    priority = "Low"

    # Data-driven definition of issues per application.
    # (issue_type, summary_template, description, components)
    issue_definitions: List[Tuple[str, str, str, str]] = [
        (
            "Task",
            "[{app}] Conduct product and tech discovery",
            (
                "Define scope, persona, user journey, user story, acceptance criteria "
                "and high-level technical definitions (e.g. language, frameworks, "
                "runtime and deployment approach)."
            ),
            "Discovery",
        ),
        (
            "User Story",
            "[{app}] Implement the solution",
            "Develop the solution according to the defined scope and technical decisions.",
            "Delivery",
        ),
        (
            "Task",
            "[{app}] Establish automated testing baseline",
            (
                "Implement unit tests (minimal required coverage) and initial "
                "integration tests if applicable."
            ),
            "Delivery",
        ),
        (
            "Task",
            "[{app}] Implement security scanning automation",
            (
                "Add automated dependency scanning, code security checks, and "
                "minimal DevSecOps pipeline integration."
            ),
            "Delivery",
        ),
        (
            "Task",
            "[{app}] Implement minimal CI/CD pipeline and deploy the solution",
            (
                "Set up a minimal CI/CD pipeline including test and security scan "
                "automation, and deploy the solution to a demo or production-like "
                "environment."
            ),
            "Delivery",
        ),
    ]

    rows: List[List[str]] = []

    for issue_type, summary_template, description, components in issue_definitions:
        summary = summary_template.format(app=app)
        base_row = build_base_row(
            issue_type=issue_type,
            summary=summary,
            description=description,
            app=app,
            product_category=product_category,
            product_type=product_type,
            platform=platform,
            layer=layer,
            os_value=os_value,
            complexity=complexity,
            language=language,
            components=components,
            priority=priority,
        )
        rows.append(base_row + stack_cells + label_cells)

    return rows


def parse_args() -> Tuple[Path, Path]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Jira issues CSV for HelloWorldAtlas applications."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV file.")
    parser.add_argument("output_csv", type=Path, help="Path to the output CSV file.")
    args = parser.parse_args()
    return args.input_csv, args.output_csv


def main() -> None:
    input_path, output_path = parse_args()

    try:
        source_rows = read_source_rows(input_path)
    except FileNotFoundError:
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied reading: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Early exit if there is no data.
    if not source_rows:
        print("No rows found in input CSV.")
        sys.exit(0)

    max_stack_count, max_label_count = compute_max_multi_counts(source_rows)
    header = build_header(max_stack_count, max_label_count)

    all_rows: List[List[str]] = []

    for row in source_rows:
        issue_rows = generate_issue_rows_for_application(
            row,
            max_stack_count=max_stack_count,
            max_label_count=max_label_count,
        )
        all_rows.extend(issue_rows)

    with output_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)
        writer.writerows(all_rows)

    print(f"File generated successfully: {output_path} ({len(all_rows)} issues)")


if __name__ == "__main__":
    main()
