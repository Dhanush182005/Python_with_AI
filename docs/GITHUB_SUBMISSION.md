# GitHub and assignment submission

The project code, dataset, sample outputs, README, and documentation are included. Creating the online repository and submitting the trainer's form remain separate steps.

## Option 1: Upload in the GitHub website

1. Sign in to [GitHub](https://github.com/).
2. Click **New repository**. Suggested repository name: `student-performance-analytics`.
3. Set visibility according to the trainer's instruction. Use Public if the trainer expects a public repository.
4. Create the repository. Avoid adding a second README because this project already includes one.
5. Click **Add file > Upload files**. Upload the contents of the extracted project folder, including `docs/`, `tests/`, and `output/`. Keep `main.py` and `README.md` at the repository's top level. Upload the extracted files, not only the ZIP.
6. Do not upload `.venv/`, `__pycache__/`, or the assignment PDF. `.gitignore` is included for local Git use; browser uploads require selecting the right files yourself.
7. Commit the uploaded files with a message such as `Add student performance analytics project`.
8. Copy the repository's actual URL. Add it to `docs/STUDENT_DETAILS.md` and section 10 of `docs/Project_Documentation.md`, and refresh the PDF if required by your trainer.
9. Verify that code, dataset, README, documentation and sample results are visible in the repository.
10. Open the Google Form supplied by EWB Courses and submit the repository link. This assignment PDF does not contain the actual Google Form URL.
11. Follow the trainer's exact submission sequence, verify form confirmation, and finish by **15 October 2026**.

## Option 2: Push using Git

First create an empty repository on GitHub. Then open a terminal inside this project's extracted folder.

```powershell
git init
git add .
git commit -m "Add student performance analytics project"
git branch -M main
```

Copy your new repository's actual HTTPS URL from GitHub. Set a PowerShell variable to that URL, replacing the clearly marked text below:

```powershell
$repoUrl = "PASTE_YOUR_ACTUAL_REPOSITORY_HTTPS_URL_HERE"
git remote add origin $repoUrl
git push -u origin main
```

GitHub may ask you to sign in. Complete its normal sign-in prompt. If a Git identity is needed, configure your own name and GitHub email; do not enter a password into project files.

If this folder already belongs to a repository, inspect `git status` and `git remote -v` before adding a remote. If `origin` already points to the correct repository, skip `git remote add`.

When documentation is updated later:

```powershell
git add docs README.md
git commit -m "Update project documentation and repository link"
git push
```

## Final checklist

- [ ] Review student name and add register/course ID.
- [ ] Run the project locally and understand its calculations.
- [ ] Keep at least 15-20 student records; the supplied dataset has 25.
- [ ] Run the tests and inspect the output files.
- [ ] Upload Python files, dataset, requirements, README, documentation and sample results.
- [ ] Add the actual repository URL to the documentation.
- [ ] Verify repository access using the trainer's required visibility.
- [ ] Submit the repository link through the trainer's Google Form.
- [ ] Keep the form's confirmation and finish by 15 October 2026.
