# Student Performance Analytics System

## 1. Project title and student details

**Title:** Student Performance Analytics System  
**Prepared for:** Mohan Arun R.V. (review course-registration spelling)  
**Degree:** B.Tech Artificial Intelligence and Data Science  
**College:** Paavai College of Engineering  
**Course:** EWB Courses - Python with AI  
**Register number / course student ID:** To be added before submission  
**Repository URL:** To be added after repository creation  
**Assignment deadline:** 15 October 2026

## 2. Objective

Build a Python-based system that loads student data from a CSV, calculates individual results and produces useful performance summaries. It reduces repetitive manual calculations and presents student-level, subject-level and department-level information clearly.

The system answers: Who has the highest average? Which subject has the best average? How many students passed? What is the overall class average? Who has low attendance?

## 3. Technologies used

| Tool | Actual use |
| --- | --- |
| Python | Functions, variables, constants, loops, conditions, lists, dictionaries and command-line execution |
| NumPy | Student totals/averages, all-subject pass checks, subject minimum/maximum/average and pass counts |
| Pandas | CSV input, DataFrames, numeric conversion, filtering, grouping, ranking, CSV export |
| `unittest` | Automated boundary, validation and end-to-end checks |
| Git / GitHub | Planned repository and submission workflow; online repository not created in this package |

The implementation was tested on Python 3.12.14 with NumPy 2.3.5 and Pandas 2.2.3. The analysis itself has only NumPy and Pandas as third-party dependencies. The accompanying PDF was formatted with ReportLab outside the analysis program.

## 4. Dataset description

`students.csv` contains **25 synthetic student records**, **9 required columns**, **5 subjects** and **4 departments**. Department counts are AI&DS: 7, CSE: 6, ECE: 6 and MECH: 6. These are realistic demonstration values, not real personal or examination data.

| Column | Description |
| --- | --- |
| `Student_ID` | Unique, nonempty identifier |
| `Name` | Student name, nonempty text |
| `Department` | Department, nonempty text |
| `Python` | Numeric marks out of 100 |
| `Mathematics` | Numeric marks out of 100 |
| `Statistics` | Numeric marks out of 100 |
| `Computer_Science` | Numeric marks out of 100 |
| `English` | Numeric marks out of 100 |
| `Attendance` | Numeric percentage from 0 to 100 |

Input is UTF-8 CSV. Identifiers are initially read as strings, preserving leading zeros. Marks and attendance are converted to numeric values after validation. Missing columns, blank identifying cells, missing/invalid numbers, values outside 0-100, duplicate IDs, and empty datasets are rejected with a helpful message. Additional columns are ignored.

## 5. Implementation

### Processing sequence

1. Parse optional input path, output folder and top-student count.
2. Load the CSV with `pd.read_csv()` and check data quality.
3. Select subject columns and convert them to a NumPy array of shape `(25, 5)` for the sample.
4. Use `np.sum(marks, axis=1)` for totals and `np.mean(marks, axis=1)` for averages.
5. Use `np.all(marks >= 40, axis=1)` for each student's pass condition.
6. Apply grades with reusable conditions and loops. Record failed subject names.
7. Flag attendance and rank students by unrounded average.
8. Analyze subjects and department groups; identify passed top performers and class extremes.
9. Display the input data, results and summaries; save CSV reports and a text report.

### Calculation rules

All subjects have equal weight. Total is the sum of five marks, with a maximum of 500. Average is total divided by five. A student passes only if every subject is at least 40. Any subject below 40 produces Fail and grade F. Attendance below 75% is flagged independently; attendance does not change the marks-based result.

| Grade | Passed-student average |
| --- | --- |
| A+ | 90 or more |
| A | 80 to less than 90 |
| B+ | 70 to less than 80 |
| B | 60 to less than 70 |
| C | 50 to less than 60 |
| D | 40 to less than 50 |
| F | Any failed subject, regardless of average |

Ranks and grades use unrounded averages. Numerical reports display two decimal places. Equal averages have competition ranks: 1, 1, 3, 4, 4, 6. Top performers are selected from passed students only, and ties at the requested cutoff are included. The class highest/lowest averages consider all students, independent of pass status.

### Reusable functions

| Function | Responsibility |
| --- | --- |
| `load_data()` / `validate_data()` | Load and validate the input |
| `assign_grade()` | Apply the grading rule |
| `process_students()` | Calculate student-level results |
| `subject_analysis()` | Compute subject statistics |
| `department_analysis()` | Summarize department groups |
| `top_performers()` | Select top passed students with ties |
| `class_summary()` | Calculate class-level metrics |
| `build_report()` | Prepare clear report text |
| `save_outputs()` | Save seven CSVs and one text file |
| `main()` | Coordinate the processing sequence |

## 6. Key features

- 25 organized student records loaded into a DataFrame.
- NumPy numerical calculations and explicit Python functions/loops.
- Individual totals, averages, grades and pass/fail results.
- Clear failed-subject and attendance flags.
- Highest, lowest and average class performance.
- Subject-wise highest/lowest/average, pass count and pass percentage.
- Department-wise performance and attendance summaries.
- Top passed students, preserving equal-score ties.
- Readable terminal results and eight saved reports.
- Input validation and 24 automated tests with boundary subcases.

## 7. Output and verified sample results

| Metric | Result |
| --- | --- |
| Total students | 25 |
| Passed students | 20 |
| Failed students | 5 |
| Pass percentage | 80.00% |
| Overall class average | 71.44 / 100 |
| Highest average | Priya and Sneha, 95.20 |
| Lowest average | Vignesh, 34.80 |
| Best subject average | English, 75.16 |
| Weakest subject average | Python, 68.96 |
| Average attendance | 84.40% |
| Low-attendance students | 5 |

### Top performers

| Rank | Student ID | Name | Total / 500 | Average / 100 | Grade |
| --- | --- | --- | --- | --- | --- |
| 1 | S002 | Priya | 476 | 95.20 | A+ |
| 1 | S018 | Sneha | 476 | 95.20 | A+ |
| 3 | S010 | Divya | 474 | 94.80 | A+ |
| 4 | S001 | Arun Kumar | 450 | 90.00 | A+ |
| 4 | S014 | Aishwarya | 450 | 90.00 | A+ |

### Subject-wise analysis

| Subject | Highest | Lowest | Average | Passed | Failed | Pass % |
| --- | --- | --- | --- | --- | --- | --- |
| Python | 96 | 31 | 68.96 | 21 | 4 | 84.00 |
| Mathematics | 95 | 28 | 69.20 | 22 | 3 | 88.00 |
| Statistics | 96 | 35 | 70.72 | 24 | 1 | 96.00 |
| Computer Science | 98 | 38 | 73.16 | 24 | 1 | 96.00 |
| English | 97 | 40 | 75.16 | 25 | 0 | 100.00 |

### Worked examples

Arun Kumar's total is `92 + 88 + 90 + 94 + 86 = 450`; his average is `450 / 5 = 90.00`. He passes every subject and receives A+.

Manoj's average is 77.00, but Mathematics is 35; he receives Fail and F. Prakash scores exactly 40 in every subject and has exactly 75% attendance; he receives Pass, D and Sufficient. Sanjay passes his subjects but is flagged for 74% attendance.

### Saved files

`output/student_results.csv`, `subject_analysis.csv`, `department_analysis.csv`, `top_performers.csv`, `failed_students.csv`, `attendance_alerts.csv`, `class_summary.csv`, and `analysis_report.txt` contain the generated results. Successful runs replace those reports in the selected output folder. The PDF includes actual result tables; screenshots are optional in the assignment.

### Verification

All **24 automated tests** passed locally. They cover hand-calculated totals and means, grade and attendance boundaries, failure despite a high average, raw-average grading, tied ranks, subject/department statistics, all-pass/all-fail cases, missing/invalid input, identifier handling, and command-line exports.

Run verification with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 8. Final outcome

The delivered local project loads the dataset, validates it, computes all required student metrics, answers practical class questions, identifies subject performance and top students, and exports readable results. Its code, dataset, documentation, study guide and sample outputs are ready for local review and adaptation. GitHub publication and the trainer's form submission are still pending.

The results describe this dataset only. The system does not predict future marks or establish that attendance causes academic performance. Charts, multiple-exam tracking and a configurable grading interface are possible future extensions.

## 9. Challenges and learning

Implementation issues handled in this project:

| Issue | Resolution / learning |
| --- | --- |
| High average despite a failed subject | Check every subject before assigning Pass and grade |
| Missing or invalid marks | Reject incomplete/invalid rows instead of inventing marks |
| Same average for multiple students | Preserve competition ranks and cutoff ties |
| Rounding near a grade boundary | Use unrounded calculations for decisions |
| IDs containing leading zeros | Read identifying fields as strings |
| Reports run from another folder | Resolve default paths relative to `main.py` |

The project demonstrates DataFrames, array axes, functions, conditions, loops, dictionaries, filtering, grouping, validation and report export. Before submission, personalize this section with what you personally learned while running, reviewing and adapting the implementation.

## 10. GitHub repository and submission

**Final repository URL: pending - add the actual URL after repository creation.**

Follow `GITHUB_SUBMISSION.md`: create a repository, upload the extracted project contents, add the actual URL here and in `STUDENT_DETAILS.md`, verify repository access, and submit that link through the Google Form supplied by the trainer. The assignment PDF contains the deadline but no Google Form URL. Complete submission on or before **15 October 2026**.

## Appendix A: Setup

Extract the ZIP and open the project folder in VS Code. In the terminal inside that folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Use Python 3.11 or later. If Windows recognizes `py` instead of `python`, use `py -m venv .venv` for the first command. Package installation needs internet; the analysis then works offline.

For a different CSV or report directory:

```powershell
.\.venv\Scripts\python.exe main.py --input students.csv --output custom_reports --top 3
```

## Appendix B: Learning references

- https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- https://pandas.pydata.org/docs/user_guide/groupby.html
- https://numpy.org/doc/stable/reference/generated/numpy.sum.html
- https://numpy.org/doc/stable/reference/generated/numpy.mean.html
- https://docs.python.org/3/tutorial/controlflow.html

For simple code explanations, viva questions and practice tasks, read `EXPLAIN_AND_VIVA.md`.
