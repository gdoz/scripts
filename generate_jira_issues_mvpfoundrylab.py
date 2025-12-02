import argparse
import csv
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Dict, List, Tuple

# Input column names
COL_APPLICATION = "Application"
COL_PRODUCT_CATEGORY = "Product Category"
COL_PRODUCT_TYPE = "Product Type"
COL_PLATFORM = "Platform"
COL_LAYER = "Layer"
COL_OS = "OS"
COL_COMPLEXITY = "Complexity"
COL_LABELS = "Labels"
COL_DESCRIPTION = "Description"

ISSUES_PER_APPLICATION = 12


def read_source_rows(input_path: Path) -> List[Dict[str, str]]:
    """Read the source CSV and return a list of dicts."""
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def compute_max_labels(rows: Iterable[Dict[str, str]]) -> int:
    """Find the maximum number of non-empty labels in any row of the source."""
    max_labels = 0
    for row in rows:
        raw = (row.get(COL_LABELS) or "").strip()
        if not raw:
            continue
        labels = [x.strip() for x in raw.split(";") if x.strip()]
        if len(labels) > max_labels:
            max_labels = len(labels)
    return max_labels


def build_output_header(max_labels: int) -> List[str]:
    """Assemble the header for the output CSV file."""
    base_fields = [
        "Issue Type",
        "Issue Id",
        "Parent",
        "Summary",
        "Priority",
        "Application",
        "Product Category",
        "Product Type",
        "Platform",
        "Layer",
        "OS",
        "Complexity",
        "Components",
        "Description",
    ]
    label_fields = ["Label"] * max_labels  # all columns with the same name
    return base_fields + label_fields


def split_labels(raw: str | None) -> List[str]:
    """Convert string 'a;b;;c' to ['a', 'b', 'c']."""
    if not raw:
        return []
    return [x.strip() for x in raw.split(";") if x.strip()]


def build_issue_rows_for_app(
    app_row: Dict[str, str],
    start_issue_id: int,
    max_labels: int,
) -> Tuple[List[List[str]], int]:
    """
    Generate issues for a single application.

    Returns:
        A tuple (rows, next_issue_id) where:
        - rows is a list of CSV lines (list of values).
        - next_issue_id is the next available issue id after this application.
    """
    rows: List[List[str]] = []

    # Basic application fields
    app_orig = (app_row.get(COL_APPLICATION) or "").strip()
    app_name = app_orig if app_orig else ""
    product_category = (app_row.get(COL_PRODUCT_CATEGORY) or "").strip()
    product_type = (app_row.get(COL_PRODUCT_TYPE) or "").strip()
    platform = (app_row.get(COL_PLATFORM) or "").strip()
    layer = (app_row.get(COL_LAYER) or "").strip()
    os_value = (app_row.get(COL_OS) or "").strip()
    complexity = (app_row.get(COL_COMPLEXITY) or "").strip()
    labels = split_labels((app_row.get(COL_LABELS) or "").strip())
    description_orig = (app_row.get(COL_DESCRIPTION) or "").strip()

    def make_row(
        issue_type: str,
        issue_id: int,
        parent_id: int | None,
        summary: str,
        components: str,
        description: str,
    ) -> List[str]:
        """Assemble a single CSV row for an issue."""
        base = [
            issue_type,
            str(issue_id),
            str(parent_id) if parent_id is not None else "",
            summary,
            "Low",  # Priority
            app_name,
            product_category,
            product_type,
            platform,
            layer,
            os_value,
            complexity,
            components,
            description,
        ]
        # Fill in Label columns
        label_values = labels[:max_labels] + [""] * max(0, max_labels - len(labels))
        return base + label_values

    current_id = start_issue_id

    # ----------- MVP Discovery ----------------------------

    # Issue 1: Discovery Epic
    epic_disc_id = current_id
    summary_epic_disc = f"[{app_name}] Product discovery"
    desc_epic_disc = (
        "Execute the product discovery cycle to understand the opportunity, "
        "validate desirability and feasibility, define the high-level solution, "
        "and shape the initial MVP."
    )
    if description_orig:
        desc_epic_disc += "\n" + f"Initial idea: {description_orig}"

    rows.append(
        make_row(
            issue_type="Epic",
            issue_id=epic_disc_id,
            parent_id=None,
            summary=summary_epic_disc,
            components="Discovery",
            description=desc_epic_disc,
        )
    )
    current_id += 1

    # Issue 2: Discovery Task
    task_disc_id = current_id
    summary_task_disc = f"[{app_name}] Conduct product discovery"
    desc_task_disc = (
        "This task covers the core activities required to define the problem, "
        "the audience, and the product scope:\n"
        "- Market research\n"
        "- Persona definition\n"
        "- User journey mapping\n"
        "- Requirements and user stories\n"
        "- Acceptance criteria\n"
        "- Low-fidelity wireframe\n"
        "- Conceptual prototype\n"
        "- MVP definition and prioritization"
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_disc_id,
            parent_id=epic_disc_id,
            summary=summary_task_disc,
            components="Discovery",
            description=desc_task_disc,
        )
    )
    current_id += 1

    # Issue 3: Tech Discovery Task
    task_tech_disc_id = current_id
    summary_task_tech_disc = f"[{app_name}] Perform tech discovery"
    desc_task_tech_disc = (
        "This task evaluates the technical feasibility and shapes the initial "
        "technical direction of the product:\n"
        "- Technical feasibility assessment\n"
        "- High-level architecture\n"
        "- High-level DDD mapping\n"
        "- Macro technology stack\n"
        "- Conceptual data model\n"
        "- Technical risks & trade-offs"
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_tech_disc_id,
            parent_id=epic_disc_id,
            summary=summary_task_tech_disc,
            components="Discovery",
            description=desc_task_tech_disc,
        )
    )
    current_id += 1

    # ----------- MVP Delivery ----------------------------

    # Issue 4: MVP Epic
    epic_mvp_id = current_id
    summary_epic_mvp = f"[{app_name}] MVP development"
    desc_epic_mvp = "Implement MVP."
    rows.append(
        make_row(
            issue_type="Epic",
            issue_id=epic_mvp_id,
            parent_id=None,
            summary=summary_epic_mvp,
            components="Delivery",
            description=desc_epic_mvp,
        )
    )
    current_id += 1

    # Issue 5: User Story (MVP)
    us_dev_id = current_id
    summary_us_dev = f"[{app_name}] Implement core MVP features"
    desc_us_dev = (
        "Develop the minimum set of features required to validate the product hypothesis."
    )
    rows.append(
        make_row(
            issue_type="User Story",
            issue_id=us_dev_id,
            parent_id=epic_mvp_id,
            summary=summary_us_dev,
            components="Delivery",
            description=desc_us_dev,
        )
    )
    current_id += 1

    # Issue 6: CI/CD & Deployment Task
    task_cicd_id = current_id
    summary_task_cicd = f"[{app_name}] Implement minimal CI/CD pipeline and deploy MVP"
    desc_task_cicd = (
        "Set up a minimal CI/CD pipeline and deliver the MVP to a demo or "
        "production-like environment."
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_cicd_id,
            parent_id=epic_mvp_id,
            summary=summary_task_cicd,
            components="Delivery",
            description=desc_task_cicd,
        )
    )
    current_id += 1

    # ----------- V2 Discovery ----------------------------

    # Issue 7: Discovery Epic (V2)
    epic_disc_v2_id = current_id
    summary_epic_disc_v2 = f"[{app_name}] V2 – Product Discovery"
    desc_epic_disc_v2 = (
        "Conduct discovery to refine the product vision and prepare the scope "
        "for the second version."
    )
    rows.append(
        make_row(
            issue_type="Epic",
            issue_id=epic_disc_v2_id,
            parent_id=None,
            summary=summary_epic_disc_v2,
            components="Discovery",
            description=desc_epic_disc_v2,
        )
    )
    current_id += 1

    # Issue 8: Discovery Task (V2)
    task_disc_v2_id = current_id
    summary_task_disc_v2 = f"[{app_name}] V2 – Conduct product and tech discovery"
    desc_task_disc_v2 = (
        "Define scope, improvements, user stories, and high-level technical "
        "definitions for V2 based on insights from MVP usage and feedback."
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_disc_v2_id,
            parent_id=epic_disc_v2_id,
            summary=summary_task_disc_v2,
            components="Discovery",
            description=desc_task_disc_v2,
        )
    )
    current_id += 1

    # ----------- V2 Delivery ----------------------------

    # Issue 9: Development Epic (V2)
    epic_v2_id = current_id
    summary_epic_v2 = f"[{app_name}] V2 - Development"
    desc_epic_v2 = (
        "Implement improvements, new features, and foundational engineering quality for V2."
    )
    rows.append(
        make_row(
            issue_type="Epic",
            issue_id=epic_v2_id,
            parent_id=None,
            summary=summary_epic_v2,
            components="Delivery",
            description=desc_epic_v2,
        )
    )
    current_id += 1

    # Issue 10: Tests Task (V2)
    task_tests_v2_id = current_id
    summary_task_tests_v2 = f"[{app_name}] Establish automated testing baseline"
    desc_task_tests_v2 = (
        "Implement unit tests (minimal required coverage) and initial integration tests."
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_tests_v2_id,
            parent_id=epic_v2_id,
            summary=summary_task_tests_v2,
            components="Delivery",
            description=desc_task_tests_v2,
        )
    )
    current_id += 1

    # Issue 11: Security Task (V2)
    task_security_v2_id = current_id
    summary_task_security_v2 = (
        f"[{app_name}] Implement security scanning automation"
    )
    desc_task_security_v2 = (
        "Add automated dependency scanning, code security checks, and minimal "
        "DevSecOps pipeline integration."
    )
    rows.append(
        make_row(
            issue_type="Task",
            issue_id=task_security_v2_id,
            parent_id=epic_v2_id,
            summary=summary_task_security_v2,
            components="Delivery",
            description=desc_task_security_v2,
        )
    )
    current_id += 1

    # Issue 12: User Story (V2)
    us_improv_id = current_id
    summary_us_improv = (
        f"[{app_name}] Develop V2 features based on new discovery insights"
    )
    desc_us_improv = (
        "Implement the new features prioritized for V2, following the baseline "
        "of automated tests and security practices."
    )
    rows.append(
        make_row(
            issue_type="User Story",
            issue_id=us_improv_id,
            parent_id=epic_v2_id,
            summary=summary_us_improv,
            components="Delivery",
            description=desc_us_improv,
        )
    )
    current_id += 1

    assert len(rows) == ISSUES_PER_APPLICATION, (
        f"Expected {ISSUES_PER_APPLICATION} issues per application, "
        f"got {len(rows)} for app '{app_name}'"
    )

    return rows, current_id


def parse_args() -> tuple[Path, Path]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Jira issues CSV from applications CSV."
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

    if not source_rows:
        print("No rows found in input CSV.")
        sys.exit(0)

    max_labels = compute_max_labels(source_rows)
    header = build_output_header(max_labels)

    issue_id_counter = 1
    all_rows: list[list[str]] = []

    for app_row in source_rows:
        rows_for_app, issue_id_counter = build_issue_rows_for_app(
            app_row,
            issue_id_counter,
            max_labels,
        )
        all_rows.extend(rows_for_app)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_rows)

    print(f"Generated {len(all_rows)} issues into {output_path}")


if __name__ == "__main__":
    main()
