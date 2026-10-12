"""Reusable functions for a beginner-friendly student analytics project."""

from pathlib import Path

import numpy as np
import pandas as pd


# Each subject is marked out of 100. Change this list when changing the CSV.
SUBJECTS = ["Python", "Mathematics", "Statistics", "Computer_Science", "English"]
DETAIL_COLUMNS = ["Student_ID", "Name", "Department"]
REQUIRED_COLUMNS = DETAIL_COLUMNS + SUBJECTS + ["Attendance"]
PASS_MARK = 40
MIN_ATTENDANCE = 75


def validate_data(data):
    """Check the required columns and values, returning a clean copy.

    Invalid data is rejected instead of silently changing a student's marks.
    CSV row numbers in messages include the header row.
    """
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if data.empty:
        raise ValueError("The dataset has no student records.")

    clean = data[REQUIRED_COLUMNS].copy().reset_index(drop=True)
    for column in DETAIL_COLUMNS:
        if clean[column].isna().any():
            raise ValueError(f"{column} cannot be empty.")
        clean[column] = clean[column].astype(str).str.strip()
        if clean[column].eq("").any():
            raise ValueError(f"{column} cannot be empty.")

    duplicates = clean.loc[clean["Student_ID"].duplicated(), "Student_ID"].tolist()
    if duplicates:
        raise ValueError("Duplicate Student_ID values: " + ", ".join(duplicates))

    # A loop is useful because each numeric column needs the same checks.
    for column in SUBJECTS + ["Attendance"]:
        numbers = pd.to_numeric(clean[column], errors="coerce")
        valid = np.isfinite(numbers.to_numpy(dtype=float)) & numbers.between(0, 100)
        if not valid.all():
            rows = [str(index + 2) for index in clean.index[~valid]]
            raise ValueError(
                f"{column} must contain numbers from 0 to 100. "
                f"Check CSV rows: {', '.join(rows)}"
            )
        clean[column] = numbers
    return clean


def load_data(csv_path):
    """Read a UTF-8 CSV using Pandas, preserving identifiers such as 001."""
    try:
        data = pd.read_csv(csv_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    except pd.errors.EmptyDataError as error:
        raise ValueError("The CSV file is empty.") from error
    except (pd.errors.ParserError, UnicodeDecodeError) as error:
        raise ValueError("Use a valid UTF-8 CSV with the required columns.") from error
    return validate_data(data)


def assign_grade(average, passed):
    """Assign a grade using the original, unrounded average.

    F overrides the average when any subject is below the pass mark.
    """
    if not passed:
        return "F"
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B+"
    if average >= 60:
        return "B"
    if average >= 50:
        return "C"
    return "D"


def process_students(data):
    """Add totals, averages, grades, result, rank and attendance status."""
    result = validate_data(data)
    marks = result[SUBJECTS].to_numpy(dtype=float)

    # axis=1 means across the subjects in each student's row.
    result["Total"] = np.sum(marks, axis=1)
    result["Average"] = np.mean(marks, axis=1)
    passed = np.all(marks >= PASS_MARK, axis=1)
    result["Result"] = np.where(passed, "Pass", "Fail")

    grades = []
    failed_subjects = []
    for row_number, average in enumerate(result["Average"]):
        grades.append(assign_grade(average, passed[row_number]))
        failures = []
        for subject_number, subject in enumerate(SUBJECTS):
            if marks[row_number, subject_number] < PASS_MARK:
                failures.append(subject)
        failed_subjects.append(", ".join(failures))

    result["Grade"] = grades
    result["Failed_Subjects"] = failed_subjects
    result["Attendance_Status"] = np.where(
        result["Attendance"] >= MIN_ATTENDANCE, "Sufficient", "Low"
    )
    # Competition ranking: equal averages receive ranks 1, 1, 3, ...
    result["Rank"] = result["Average"].rank(method="min", ascending=False).astype(int)
    return result


def subject_analysis(students):
    """Find the minimum, maximum, mean and pass rate for every subject."""
    rows = []
    for subject in SUBJECTS:
        marks = students[subject].to_numpy(dtype=float)
        pass_count = int(np.sum(marks >= PASS_MARK))
        rows.append({
            "Subject": subject,
            "Highest": float(np.max(marks)),
            "Lowest": float(np.min(marks)),
            "Average": float(np.mean(marks)),
            "Passed": pass_count,
            "Failed": len(students) - pass_count,
            "Pass_Percentage": 100 * pass_count / len(students),
        })
    return pd.DataFrame(rows)


def department_analysis(students):
    """Group records by department using Pandas."""
    rows = []
    for department, group in students.groupby("Department", sort=True):
        pass_count = int(group["Result"].eq("Pass").sum())
        rows.append({
            "Department": department,
            "Students": len(group),
            "Average": float(group["Average"].mean()),
            "Passed": pass_count,
            "Failed": len(group) - pass_count,
            "Pass_Percentage": 100 * pass_count / len(group),
            "Average_Attendance": float(group["Attendance"].mean()),
        })
    return pd.DataFrame(rows)


def top_performers(students, count=5):
    """Select the top N passed students, including ties at the cutoff."""
    if not isinstance(count, int) or count < 1:
        raise ValueError("The number of top students must be a positive integer.")
    eligible = students.loc[students["Result"].eq("Pass")].copy()
    eligible = eligible.sort_values(["Average", "Student_ID"], ascending=[False, True])
    if eligible.empty:
        return eligible
    cutoff = eligible.iloc[min(count, len(eligible)) - 1]["Average"]
    return eligible.loc[eligible["Average"] >= cutoff].copy()


def class_summary(students, subjects):
    """Build the class summary, preserving all tied leaders."""
    averages = students["Average"].to_numpy(dtype=float)
    highest = float(np.max(averages))
    lowest = float(np.min(averages))
    pass_count = int(students["Result"].eq("Pass").sum())

    def names_at(value):
        names = students.loc[students["Average"].eq(value), ["Student_ID", "Name"]]
        return "; ".join(f"{row.Student_ID} - {row.Name}" for row in names.itertuples(index=False))

    best_mean = subjects["Average"].max()
    weakest_mean = subjects["Average"].min()
    return {
        "Total Students": len(students),
        "Passed Students": pass_count,
        "Failed Students": len(students) - pass_count,
        "Pass Percentage": 100 * pass_count / len(students),
        "Class Average": float(np.mean(averages)),
        "Highest Average": highest,
        "Highest Average Students": names_at(highest),
        "Lowest Average": lowest,
        "Lowest Average Students": names_at(lowest),
        "Best Subject": ", ".join(subjects.loc[subjects["Average"].eq(best_mean), "Subject"]),
        "Best Subject Average": float(best_mean),
        "Weakest Subject": ", ".join(subjects.loc[subjects["Average"].eq(weakest_mean), "Subject"]),
        "Weakest Subject Average": float(weakest_mean),
        "Average Attendance": float(students["Attendance"].mean()),
        "Low Attendance Students": int(students["Attendance_Status"].eq("Low").sum()),
    }


def format_table(data):
    """Print a readable table without modifying stored numeric values."""
    if data.empty:
        return "No records."
    display = data.copy()
    display.columns = [column.replace("_", " ") for column in display.columns]
    return display.to_string(index=False, float_format=lambda value: f"{value:.2f}")


def build_report(source, students, subjects, departments, top, summary):
    """Create the same clear report for the terminal and a saved text file."""
    lines = [
        "STUDENT PERFORMANCE ANALYTICS SYSTEM",
        "Python | NumPy | Pandas",
        "Dataset: synthetic demonstration records, not real student results.",
        f"Pass rule: at least {PASS_MARK} in EVERY subject; each subject is out of 100.",
        f"Attendance: below {MIN_ATTENDANCE}% is flagged independently of marks.",
        "Grades: A+ >=90; A >=80; B+ >=70; B >=60; C >=50; D >=40; any failed subject = F.",
        "Rank: overall average, with competition ties; top list includes passed students only.",
        "Averages are rounded only for display and export; grading uses full precision.",
        "", "1. DATASET INFORMATION",
        f"Records: {len(source)} | Required columns: {len(source.columns)}",
        "Columns: " + ", ".join(source.columns),
        "Data types: " + ", ".join(f"{column}={dtype}" for column, dtype in source.dtypes.items()),
        "", "2. INPUT DATA", format_table(source),
        "", "3. STUDENT RESULTS",
        format_table(students[DETAIL_COLUMNS + ["Total", "Average", "Grade", "Result", "Rank", "Attendance_Status"]]),
        "", "4. CLASS SUMMARY",
    ]
    for label, value in summary.items():
        shown = f"{value:.2f}" if isinstance(value, float) else str(value)
        lines.append(f"{label}: {shown}")
    lines.extend([
        "", "5. SUBJECT-WISE PERFORMANCE", format_table(subjects),
        "", "6. DEPARTMENT-WISE PERFORMANCE", format_table(departments),
        "", "7. TOP PASSED STUDENTS (CUTOFF TIES INCLUDED)",
        format_table(top[["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade"]]),
        "", "8. FAILED STUDENTS",
        format_table(students.loc[students["Result"].eq("Fail"), ["Student_ID", "Name", "Average", "Failed_Subjects"]]),
        "", "9. LOW ATTENDANCE",
        format_table(students.loc[students["Attendance_Status"].eq("Low"), ["Student_ID", "Name", "Attendance", "Result"]]),
    ])
    return "\n".join(lines) + "\n"


def save_outputs(output_dir, students, subjects, departments, top, summary, report):
    """Save analysis tables as CSV files and the readable report as text."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "student_results.csv": students,
        "subject_analysis.csv": subjects,
        "department_analysis.csv": departments,
        "top_performers.csv": top,
        "failed_students.csv": students.loc[students["Result"].eq("Fail")],
        "attendance_alerts.csv": students.loc[students["Attendance_Status"].eq("Low")],
        "class_summary.csv": pd.DataFrame(
            [(label, f"{value:.2f}" if isinstance(value, float) else value)
             for label, value in summary.items()],
            columns=["Metric", "Value"],
        ),
    }
    saved = []
    for filename, table in tables.items():
        path = output_dir / filename
        table.to_csv(path, index=False, float_format="%.2f", encoding="utf-8")
        saved.append(path)
    report_path = output_dir / "analysis_report.txt"
    report_path.write_text(report, encoding="utf-8")
    saved.append(report_path)
    return saved
