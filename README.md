# Student Performance Analytics System

A Python mini project for the EWB Courses **Python with AI** assignment. It reads student marks and attendance from a CSV file, checks the data, calculates results using NumPy and Pandas, and generates clear terminal and CSV reports.

The supplied dataset contains **25 synthetic students**, **5 subjects**, and **4 departments**. The records are demonstration data, not real examination results. No model training or external service is needed.

## Objective

Turn a student marks sheet into useful answers: Who passed? Who needs support? Which subject has the highest average? Who are the top performers? Which students have low attendance?

## Technologies

- Python 3.11 or later: functions, loops, conditions, lists, dictionaries, and command-line handling.
- NumPy: totals, means, minimum/maximum values, and subject pass calculations.
- Pandas: CSV reading, DataFrames, validation, filtering, grouping, ranking, and CSV export.
- Standard-library `unittest`: automated verification.

Tested environment: Python 3.12.14, NumPy 2.3.5, Pandas 2.2.3. `requirements.txt` allows compatible later releases; those releases were not all tested in this environment.

## Run on Windows (PowerShell)

1. Extract the ZIP. Open the extracted `student-performance-analytics` folder in VS Code.
2. Open **Terminal > New Terminal**. The terminal must be inside the project folder.
3. Run these commands. A virtual environment keeps this project's packages together; activation is unnecessary.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

If Windows does not recognize `python`, try `py` in the first command. Install Python 3.11 or later if neither command is available. Internet is needed to install packages; analysis works offline afterward.

## Run on macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

## Files

| File / folder | Purpose |
| --- | --- |
| `main.py` | Runs loading, processing, analysis, display, and export |
| `functions.py` | Reusable analysis and validation functions; subject/rule constants |
| `students.csv` | 25 synthetic input records |
| `requirements.txt` | NumPy and Pandas dependencies |
| `output/` | Seven CSV reports and one readable text report |
| `tests/test_project.py` | 24 automated tests, with additional boundary subcases |
| `docs/Project_Documentation.md` | Editable project documentation |
| `docs/Project_Documentation.pdf` | Formatted project documentation |
| `docs/EXPLAIN_AND_VIVA.md` | Simple code explanations, practice tasks, and viva answers |
| `docs/GITHUB_SUBMISSION.md` | GitHub upload and assignment submission steps |
| `docs/STUDENT_DETAILS.md` | Student information to complete before submission |

## Dataset

Required columns, with exact spelling:

```csv
Student_ID,Name,Department,Python,Mathematics,Statistics,Computer_Science,English,Attendance
S001,Arun Kumar,AI&DS,92,88,90,94,86,95
```

- `Student_ID`: a nonempty unique identifier; leading zeros are preserved when reading CSV.
- `Name`, `Department`: nonempty text.
- Five subject columns: numeric marks from 0 to 100, inclusive. Decimal marks are accepted.
- `Attendance`: numeric percentage from 0 to 100, inclusive.
- Additional input columns are ignored. Only the required columns are analyzed.
- Blank cells, invalid numbers, out-of-range values, duplicate IDs, missing columns, and empty datasets produce a clear error. No marks are silently filled in or changed.
- The course requires at least 15-20 records. The supplied 25 records meet that requirement. Smaller custom files can be used for experiments, but maintain the required dataset size for submission.

## Calculation rules

These are explicit project assumptions, not an official institutional grading policy.

- **Total:** sum of five subject marks; maximum 500.
- **Average:** total divided by five; subjects have equal weight.
- **Pass:** every subject mark is at least 40.
- **Fail:** at least one subject mark is below 40.
- **Attendance:** 75% or more is sufficient; below 75% is low. Attendance does not change the marks-based result.

| Grade | Condition |
| --- | --- |
| A+ | Passed every subject and average >= 90 |
| A | Passed every subject and 80 <= average < 90 |
| B+ | Passed every subject and 70 <= average < 80 |
| B | Passed every subject and 60 <= average < 70 |
| C | Passed every subject and 50 <= average < 60 |
| D | Passed every subject and 40 <= average < 50 |
| F | Any subject below 40, regardless of average |

Grades and ranks use the unrounded average. Reports display two decimal places. For example, an average of 89.999 displays as 90.00 but remains grade A.

The `Rank` column ranks all students by average. Equal averages use competition ranks: **1, 1, 3, 4, 4, 6**. The top-performer list selects **passed students only** and includes everyone tied at the Nth student's average. Consequently, a top-N report may contain more than N rows. Student ID sorts tied rows for consistent display; it does not break the shared rank.

## How the program works

1. `main.py` reads the input/output arguments.
2. `load_data()` uses `pd.read_csv()` to create a DataFrame.
3. `validate_data()` checks required columns and data quality.
4. `process_students()` converts marks to a NumPy array; calculates totals/means; applies grades, result, attendance, and rank.
5. `subject_analysis()` computes each subject's highest, lowest, average, pass count, and pass percentage.
6. `department_analysis()` groups students by department and summarizes performance.
7. `top_performers()` selects passed students by average, preserving cutoff ties.
8. `class_summary()` answers the practical class-level questions.
9. `build_report()` prepares readable results; `save_outputs()` writes them to `output/`.

## Verified sample results

| Metric | Value |
| --- | --- |
| Students | 25 |
| Passed / failed | 20 / 5 |
| Pass percentage | 80.00% |
| Overall class average | 71.44 / 100 |
| Highest average | Priya and Sneha, 95.20 |
| Lowest average | Vignesh, 34.80 |
| Best subject by average | English, 75.16 |
| Weakest subject by average | Python, 68.96 |
| Average attendance | 84.40% |
| Students with low attendance | 5 |

Top five passed students: Priya (95.20), Sneha (95.20), Divya (94.80), Arun Kumar (90.00), and Aishwarya (90.00).

Useful edge cases already in the dataset:

- Prakash scores exactly 40 in all subjects and has 75% attendance: Pass, grade D, sufficient attendance.
- Manoj averages 77.00 but scores 35 in Mathematics: Fail, grade F.
- Sanjay passes all subjects but has 74% attendance: Pass with a low-attendance flag.
- Priya and Sneha share rank 1; Arun Kumar and Aishwarya share rank 4.

## Saved results

Each successful run writes these eight files and replaces earlier reports with the same names in the selected output folder.

| Output | Contents |
| --- | --- |
| `student_results.csv` | Input data plus total, average, result, grade, failed subjects, attendance status, rank |
| `subject_analysis.csv` | Highest/lowest/average marks and subject pass rates |
| `department_analysis.csv` | Department size, average, pass/fail counts, pass rate, attendance |
| `top_performers.csv` | Top passed students, including ties |
| `failed_students.csv` | Students with at least one failed subject |
| `attendance_alerts.csv` | Students below 75% attendance |
| `class_summary.csv` | Class metrics in a Metric/Value table |
| `analysis_report.txt` | Readable report matching the terminal analysis |

## Optional commands

Using the virtual-environment Python on Windows:

```powershell
.\.venv\Scripts\python.exe main.py --top 3
.\.venv\Scripts\python.exe main.py --input students.csv --output custom_reports
.\.venv\Scripts\python.exe main.py --help
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The default dataset and output folder are located beside `main.py`, so default input still works if the script is called from another directory. Explicit relative paths for `--input` and `--output` are resolved from the current terminal directory.

## Change the project

- Edit `students.csv` to use your own prepared demonstration records, then run again.
- Change subject column names in both `SUBJECTS` in `functions.py` and the CSV header.
- Change `PASS_MARK` / `MIN_ATTENDANCE` in `functions.py` only when changing the documented rules and related tests. The current grade-D range assumes a 40-mark pass threshold.
- Changing input data changes results. Update the documentation's sample-results tables and PDF if you submit a different dataset or rule set.
- Read `docs/EXPLAIN_AND_VIVA.md`, work through the example calculations, and complete the practice tasks so you can explain your individual implementation.

## Testing

The 24 tests verify totals/means, grade boundaries, subject-based failure, unrounded grading, attendance boundaries, rank ties, subject/department summaries, all-pass/all-fail data, invalid data, CSV identifier handling, and terminal/export behavior. All 24 passed in the tested environment.

## GitHub and final submission

Follow `docs/GITHUB_SUBMISSION.md`. Review your details in `docs/STUDENT_DETAILS.md`, create a repository, upload this project's contents, add the repository URL to the documentation, and submit the link in the trainer's Google Form. The assignment deadline is **15 October 2026**. A repository and form submission are still to be completed by you; no online submission is included in this download.

## Learning references

- [Pandas CSV reading](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Pandas grouping](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [NumPy sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)
- [NumPy mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)
- [Python functions and control flow](https://docs.python.org/3/tutorial/controlflow.html)

## Limitations and possible extensions

The program analyzes one CSV snapshot. It does not predict future results, infer why a student scored poorly, or treat attendance as a cause of marks. Future extensions could add charts, an interactive dashboard, multiple examinations, or configurable grading rules.
