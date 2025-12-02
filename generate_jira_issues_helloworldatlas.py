import csv
import sys
from pathlib import Path

def split_multi(value: str):
    if not value:
        return []
    return [v.strip() for v in value.split(";") if v.strip()]

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.csv output.csv")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # 1) Read all rows from the source spreadsheet.
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        source_rows = [row for row in reader]

    # 2) Calculate the maximum number of Stacks and Labels that exist.
    max_stack_count = 0
    max_label_count = 0

    for row in source_rows:
        app = (row.get("Application") or "").strip()
        if not app:
            # Ignore lines without Application.
            continue

        stack_values = split_multi(row.get("Stack", ""))
        label_values = split_multi(row.get("Labels", ""))

        max_stack_count = max(max_stack_count, len(stack_values))
        max_label_count = max(max_label_count, len(label_values))

    # 3) Define base columns + extra columns Stack/Label
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

    stack_columns = [f"Stack" for i in range(max_stack_count)] if max_stack_count > 0 else []
    label_columns = [f"Label" for i in range(max_label_count)] if max_label_count > 0 else []

    header = base_columns + stack_columns + label_columns

    # 4) Generate the output spreadsheet
    with Path(output_path).open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)

        for row in source_rows:
            app = (row.get("Application") or "").strip()
            if not app:
                continue  # Ignore empty lines.

            product_category = (row.get("Product Category") or "").strip()
            product_type     = (row.get("Product Type") or "").strip()
            platform         = (row.get("Platform") or "").strip()
            layer            = (row.get("Layer") or "").strip()
            os_              = (row.get("OS") or "").strip()
            complexity       = (row.get("Complexity") or "").strip()
            language         = (row.get("Language") or "").strip()
            stack_raw        = (row.get("Stack") or "").strip()
            labels_raw       = (row.get("Labels") or "").strip()

            stack_values = split_multi(stack_raw)
            label_values = split_multi(labels_raw)

            # Fill fixed arrays for Stack_N / Label_N columns.
            stack_cells = stack_values + [""] * (max_stack_count - len(stack_values))
            label_cells = label_values + [""] * (max_label_count - len(label_values))

            # ----------- Discovery ----------------------------

            # Issue 1: Discovery
            issue_type = "Task"
            summary = f"[{app}] Conduct product and tech discovery"
            description = (
                "Define scope, persona, user journey, user story, acceptance criteria "
                "and high-level technical definitions (e.g. language, frameworks, runtime and deployment approach)."
            )
            components = "Discovery"
            priority = "Low"

            base_row = [
                issue_type,
                summary,
                description,
                app,
                product_category,
                product_type,
                platform,
                layer,
                os_,
                complexity,
                language,
                components,
                priority,
            ]
            writer.writerow(base_row + stack_cells + label_cells)

            # ----------- Delivery ----------------------------

            # Issue 2: Implement
            issue_type = "User Story"
            summary = f"[{app}] Implement the solution"
            description = "Develop the solution according to the defined scope and technical decisions."
            components = "Delivery"

            base_row = [
                issue_type,
                summary,
                description,
                app,
                product_category,
                product_type,
                platform,
                layer,
                os_,
                complexity,
                language,
                components,
                priority,
            ]
            writer.writerow(base_row + stack_cells + label_cells)

            # Issue 3: Testing baseline
            issue_type = "Task"
            summary = f"[{app}] Establish automated testing baseline"
            description = (
                "Implement unit tests (minimal required coverage) and initial "
                "integration tests if applicable."
            )
            components = "Delivery"

            base_row = [
                issue_type,
                summary,
                description,
                app,
                product_category,
                product_type,
                platform,
                layer,
                os_,
                complexity,
                language,
                components,
                priority,
            ]
            writer.writerow(base_row + stack_cells + label_cells)

            # Issue 4: Security scanning
            issue_type = "Task"
            summary = f"[{app}] Implement security scanning automation"
            description = (
                "Add automated dependency scanning, code security checks, and "
                "minimal DevSecOps pipeline integration."
            )
            components = "Delivery"

            base_row = [
                issue_type,
                summary,
                description,
                app,
                product_category,
                product_type,
                platform,
                layer,
                os_,
                complexity,
                language,
                components,
                priority,
            ]
            writer.writerow(base_row + stack_cells + label_cells)

            # Issue 5: CI/CD & Deploy
            issue_type = "Task"
            summary = f"[{app}] Implement minimal CI/CD pipeline and deploy the solution"
            description = (
                "Set up a minimal CI/CD pipeline including test and security scan "
                "automation, and deploy the solution to a demo or production-like environment."
            )
            components = "Delivery"

            base_row = [
                issue_type,
                summary,
                description,
                app,
                product_category,
                product_type,
                platform,
                layer,
                os_,
                complexity,
                language,
                components,
                priority,
            ]
            writer.writerow(base_row + stack_cells + label_cells)

    print(f"File generated successfully: {output_path}")

if __name__ == "__main__":
    main()
