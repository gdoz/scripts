# 📘 GDOZ Scripts Repository

This repository contains small, focused engineering scripts used across different projects in the organization.
Each script is self-contained, written with clean and maintainable code, and designed to be easily executed and adapted.

## 📂 Scripts Overview

This section documents each available script, including purpose, usage instructions, and examples.

## 🧩 `generate_jira_issues_mvpfoundrylab.py`

### **Purpose**

Generates a complete set of **Jira issues** for applications registered in a CSV file from the [**GedozTech Lab's**](http://gedoz.tech) **MVPFoundryLab** product line.
For each application, the script generates a structured workflow of *Discovery*, *MVP Delivery*, *V2 Discovery*, and *V2 Delivery* issues, producing an output CSV ready for Jira import.

The script automatically detects how many `Label` columns are needed, following Jira’s multi-value column behavior.

The code follows **best practices** (e.g. [**PEP 8**](https://peps.python.org/pep-0008/)); check the implemented improvements here in the [CHANGELOG](#-changelog).

### **Usage**

Run the script by providing an input CSV (application definitions) and an output CSV (the generated issues):

```bash
python generate_jira_issues_mvpfoundrylab.py input.csv output.csv
```

To view help options:

```bash
python generate_jira_issues_mvpfoundrylab.py --help
```

## 🧩 `generate_jira_issues_helloworldatlas.py`

### **Purpose**

Generates **Jira issues** for applications in the **HelloWorldAtlas** product line from [**GedozTech Lab**](http://gedoz.tech).
For each application, the script creates a consistent workflow of issues including discovery, development, testing, security, and CI/CD.

It also automatically expands multiple `Stack` and `Label` values into repeated columns in the CSV, matching Jira’s expected structure for multi-value fields.

The code follows **best practices** (e.g. [**PEP 8**](https://peps.python.org/pep-0008/)); check the implemented improvements here in the [CHANGELOG](#-changelog).

### **Usage**

Run the script with:

```bash
python generate_jira_issues_helloworldatlas.py input.csv output.csv
```

To see usage details:

```bash
python generate_jira_issues_helloworldatlas.py --help
```

## 📝 Changelog

This repository maintains a lightweight changelog directly in the README for transparency and traceability.
Each entry links to the corresponding Pull Request, where **detailed notes and refactor explanations are available**.

### **2025-12-02 — Initial Refactors and Best-Practice Improvements**

* Refactored both scripts (`generate_jira_issues_mvpfoundrylab.py` and `generate_jira_issues_helloworldatlas.py`) to align with modern Python best practices.
* Introduced [**PEP 8**](https://peps.python.org/pep-0008/) compliance, type hints, helper functions, constants, argparse-based CLI parsing, and improved error handling.
* Removed code duplication and made the generation logic more declarative.
* Documented Jira multi-value column behavior for repeated `"Label"` and `"Stack"` fields.

🔗 PR Links:

* [**MVPFoundryLab Script Refactor**](https://github.com/gdoz/scripts/pull/1)
* [**HelloWorldAtlas Script Refactor**](https://github.com/gdoz/scripts/pull/2)

## 📄 License

This repository is publicly available and intended for educational purposes, and is licensed under the MIT License — see the [LICENSE](LICENSE) file for details
