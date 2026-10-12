"""Meaningful checks for calculation boundaries, invalid data and CLI use.

Run from the project folder: python -m unittest discover -s tests -v
Only the standard-library unittest package is needed in addition to NumPy/Pandas.
"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from functions import (  # noqa: E402
    REQUIRED_COLUMNS,
    SUBJECTS,
    assign_grade,
    class_summary,
    department_analysis,
    load_data,
    process_students,
    subject_analysis,
    top_performers,
    validate_data,
)


def example_data():
    return pd.DataFrame([
        ["001", "Alpha", "CSE", 90, 90, 90, 90, 90, 90],
        ["002", "Beta", "AI&DS", 90, 90, 90, 90, 90, 80],
        ["003", "Gamma", "CSE", 80, 80, 80, 80, 80, 74],
        ["004", "Delta", "AI&DS", 100, 100, 100, 100, 39, 90],
        ["005", "Epsilon", "CSE", 40, 40, 40, 40, 40, 75],
        ["006", "Zeta", "AI&DS", 20, 20, 20, 20, 20, 70],
    ], columns=REQUIRED_COLUMNS)


class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.students = process_students(example_data())

    def test_totals_and_averages(self):
        self.assertEqual(self.students["Total"].tolist(), [450, 450, 400, 439, 200, 100])
        np.testing.assert_allclose(self.students["Average"], [90, 90, 80, 87.8, 40, 20])

    def test_subject_failure_overrides_high_average(self):
        delta = self.students.iloc[3]
        self.assertEqual(delta["Result"], "Fail")
        self.assertEqual(delta["Grade"], "F")
        self.assertEqual(delta["Failed_Subjects"], "English")

    def test_pass_mark_boundary(self):
        epsilon = self.students.iloc[4]
        self.assertEqual(epsilon["Result"], "Pass")
        self.assertEqual(epsilon["Grade"], "D")
        self.assertEqual(epsilon["Failed_Subjects"], "")

    def test_grade_boundaries(self):
        cases = [(90, "A+"), (89.999, "A"), (80, "A"), (79.999, "B+"),
                 (70, "B+"), (69.999, "B"), (60, "B"), (59.999, "C"),
                 (50, "C"), (49.999, "D"), (40, "D")]
        for average, expected in cases:
            with self.subTest(average=average):
                self.assertEqual(assign_grade(average, True), expected)
        self.assertEqual(assign_grade(99, False), "F")

    def test_grading_uses_unrounded_average(self):
        data = example_data().iloc[:1].copy().astype({subject: float for subject in SUBJECTS})
        data.loc[:, SUBJECTS] = 89.999
        result = process_students(data).iloc[0]
        self.assertAlmostEqual(result["Average"], 89.999)
        self.assertEqual(result["Grade"], "A")

    def test_attendance_boundary_and_independent_result(self):
        self.assertEqual(self.students.iloc[2]["Attendance_Status"], "Low")
        self.assertEqual(self.students.iloc[2]["Result"], "Pass")
        self.assertEqual(self.students.iloc[4]["Attendance_Status"], "Sufficient")

    def test_ranking_and_ties(self):
        self.assertEqual(self.students["Rank"].tolist(), [1, 1, 4, 3, 5, 6])
        top = top_performers(self.students, 1)
        self.assertEqual(top["Student_ID"].tolist(), ["001", "002"])

    def test_top_list_omits_failed_students_and_accepts_large_count(self):
        top = top_performers(self.students, 100)
        self.assertEqual(top["Student_ID"].tolist(), ["001", "002", "003", "005"])
        with self.assertRaises(ValueError):
            top_performers(self.students, 0)

    def test_subject_statistics(self):
        subjects = subject_analysis(self.students).set_index("Subject")
        self.assertAlmostEqual(subjects.loc["Python", "Average"], 70)
        self.assertEqual(subjects.loc["Python", "Highest"], 100)
        self.assertEqual(subjects.loc["Python", "Lowest"], 20)
        self.assertEqual(subjects.loc["Python", "Passed"], 5)
        self.assertEqual(subjects.loc["English", "Failed"], 2)
        self.assertAlmostEqual(subjects.loc["English", "Pass_Percentage"], 400 / 6)

    def test_class_summary_and_tied_leaders(self):
        summary = class_summary(self.students, subject_analysis(self.students))
        self.assertEqual(summary["Total Students"], 6)
        self.assertEqual(summary["Passed Students"], 4)
        self.assertEqual(summary["Failed Students"], 2)
        self.assertAlmostEqual(summary["Class Average"], 407.8 / 6)
        self.assertEqual(summary["Highest Average Students"], "001 - Alpha; 002 - Beta")
        self.assertEqual(summary["Best Subject"], "Python, Mathematics, Statistics, Computer_Science")
        self.assertEqual(summary["Low Attendance Students"], 2)

    def test_department_groups(self):
        groups = department_analysis(self.students).set_index("Department")
        self.assertEqual(groups.loc["CSE", "Students"], 3)
        self.assertEqual(groups.loc["CSE", "Passed"], 3)
        self.assertAlmostEqual(groups.loc["CSE", "Average"], 70)
        self.assertEqual(groups.loc["AI&DS", "Failed"], 2)

    def test_all_failed_dataset_has_empty_top_list(self):
        data = example_data().copy()
        data.loc[:, SUBJECTS] = 20
        students = process_students(data)
        self.assertTrue(top_performers(students).empty)
        self.assertEqual(class_summary(students, subject_analysis(students))["Pass Percentage"], 0)

    def test_all_passed_dataset(self):
        data = example_data().copy()
        data.loc[:, SUBJECTS] = 100
        students = process_students(data)
        summary = class_summary(students, subject_analysis(students))
        self.assertEqual(summary["Pass Percentage"], 100)
        self.assertEqual(len(top_performers(students, 2)), 6)


class ValidationTests(unittest.TestCase):
    def test_missing_columns(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns: Python"):
            validate_data(example_data().drop(columns="Python"))

    def test_duplicate_identifiers_after_trimming(self):
        data = example_data()
        data.loc[1, "Student_ID"] = " 001 "
        with self.assertRaisesRegex(ValueError, "Duplicate Student_ID"):
            validate_data(data)

    def test_empty_identifying_fields(self):
        for column in ["Student_ID", "Name", "Department"]:
            for invalid in ["   ", None]:
                with self.subTest(column=column, value=invalid):
                    data = example_data()
                    data.loc[0, column] = invalid
                    with self.assertRaises(ValueError):
                        validate_data(data)

    def test_invalid_marks_and_attendance(self):
        for column in ["Python", "Attendance"]:
            for invalid in [-1, 101, np.inf, np.nan, "wrong", ""]:
                with self.subTest(column=column, value=invalid):
                    data = example_data().astype(object)
                    data.loc[0, column] = invalid
                    with self.assertRaisesRegex(ValueError, "Check CSV rows: 2"):
                        validate_data(data)

    def test_zero_and_one_hundred_are_valid_values(self):
        data = example_data()
        data.loc[0, SUBJECTS] = 0
        data.loc[1, SUBJECTS] = 100
        result = process_students(data)
        self.assertEqual(result.iloc[0]["Total"], 0)
        self.assertEqual(result.iloc[1]["Total"], 500)

    def test_header_only_and_empty_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.csv"
            for contents in ["", ",".join(REQUIRED_COLUMNS) + "\n"]:
                path.write_text(contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_data(path)

    def test_csv_preserves_identifiers_and_quoted_names(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "students.csv"
            data = example_data()
            data.loc[0, "Name"] = "Tamil, Student"
            data.to_csv(path, index=False, encoding="utf-8-sig")
            loaded = load_data(path)
            self.assertEqual(loaded.iloc[0]["Student_ID"], "001")
            self.assertEqual(loaded.iloc[0]["Name"], "Tamil, Student")


class CommandLineTests(unittest.TestCase):
    def run_cli(self, folder, *args):
        return subprocess.run(
            [sys.executable, str(PROJECT_DIR / "main.py"), *args],
            cwd=folder, capture_output=True, text=True, check=False,
        )

    def test_default_input_runs_from_another_folder_and_exports(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "reports"
            result = self.run_cli(folder, "--output", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(list(destination.iterdir())), 8)
            students = pd.read_csv(destination / "student_results.csv")
            self.assertEqual(len(students), 25)
            self.assertEqual(students["Result"].eq("Pass").sum(), 20)
            summary = pd.read_csv(destination / "class_summary.csv", dtype=str).set_index("Metric")
            self.assertEqual(summary.loc["Class Average", "Value"], "71.44")
            self.assertIn("Highest Average Students: S002 - Priya; S018 - Sneha", result.stdout)

    def test_custom_input_all_failed_exports_empty_top_with_headers(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "custom.csv"
            data = example_data().iloc[:1].copy()
            data.loc[:, SUBJECTS] = 10
            data.to_csv(source, index=False)
            result = self.run_cli(folder, "--input", str(source), "--output", str(Path(folder) / "reports"))
            self.assertEqual(result.returncode, 0, result.stderr)
            top = pd.read_csv(Path(folder) / "reports" / "top_performers.csv")
            self.assertTrue(top.empty)
            self.assertIn("Student_ID", top.columns)

    def test_missing_input_fails_without_reports(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "reports"
            result = self.run_cli(folder, "--input", "missing.csv", "--output", str(destination))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(destination.exists())

    def test_invalid_top_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            for value in ["0", "-2", "abc"]:
                with self.subTest(value=value):
                    result = self.run_cli(folder, "--top", value)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("positive integer", result.stderr)


if __name__ == "__main__":
    unittest.main()
