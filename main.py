"""Run with: python main.py"""

import argparse
from pathlib import Path
import sys

from functions import (
    build_report,
    class_summary,
    department_analysis,
    load_data,
    process_students,
    save_outputs,
    subject_analysis,
    top_performers,
)


PROJECT_DIR = Path(__file__).resolve().parent


def positive_integer(value):
    """Reject invalid --top values before running the analysis."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use a positive integer for --top.") from error
    if number < 1:
        raise argparse.ArgumentTypeError("Use a positive integer for --top.")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyze student marks and attendance.")
    parser.add_argument("--input", type=Path, default=PROJECT_DIR / "students.csv", help="Input CSV file")
    parser.add_argument("--output", type=Path, default=PROJECT_DIR / "output", help="Folder for saved reports")
    parser.add_argument("--top", type=positive_integer, default=5, help="Top N passed students, including cutoff ties")
    args = parser.parse_args(argv)

    try:
        source = load_data(args.input)
        students = process_students(source)
        subjects = subject_analysis(students)
        departments = department_analysis(students)
        top = top_performers(students, args.top)
        summary = class_summary(students, subjects)
        report = build_report(source, students, subjects, departments, top, summary)
        saved = save_outputs(args.output, students, subjects, departments, top, summary, report)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(report, end="")
    print(f"\nSaved {len(saved)} reports to: {args.output}")
    for path in saved:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
