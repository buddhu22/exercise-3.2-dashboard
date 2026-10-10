# Streamlit Workshop Feedback Explorer

## Project overview

A local Streamlit dashboard for exploring synthetic feedback from a secure application development workshop. It summarizes ratings, lets users filter records, highlights low ratings, charts average rating by topic, and downloads the filtered rows.

## Problem statement

Workshop organizers need a simple way to review feedback trends by topic and rating. This mini-project demonstrates that workflow with invented data while practicing input validation and safe text display.

## Features

- Four interactive summary metrics
- Multi-select topic filter and 1–5 rating-range filter
- Filtered feedback table and low-rated section (rating ≤ 2)
- Average rating by topic chart
- CSV download of the filtered synthetic records
- Friendly handling of missing, malformed, or invalid data

## Technology stack

Python, Streamlit, pandas, and CSV. No external API or database is used.

## Project structure

```text
exercise_3_2/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── workshop_feedback.csv
├── docs/
│   └── security_notes.md
└── tests/
    └── test_cases.md
```

## Dataset

`data/workshop_feedback.csv` contains 40 synthetic records with `session_id`, `rating` (1–5), `topic`, and `comment`. It contains no real student information. Ratings, topics, and required text fields are validated when the file loads.

## Setup and run

From this project folder, run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser. To stop the app, press `Ctrl+C` in the terminal.

## Using the dashboard

1. In **Topics**, leave all selected or choose one or more topics.
2. Adjust **Rating range** from 1 to 5.
3. Review the metrics and feedback table, which update to match the filters.
4. Check **Low-Rated Feedback** for matching ratings of 1 or 2.
5. Use **Download filtered feedback as CSV** to save the current filtered rows.

## Security practices

The app validates file structure and row values, uses a fixed path relative to the app, and handles errors with friendly messages. Comments are untrusted plain text displayed using Streamlit's normal dataframe rendering; the app does not execute HTML/JavaScript or use `unsafe_allow_html`, `eval()`, or `exec()`. Only synthetic data is included, and the prototype runs locally without secrets or external services. See [docs/security_notes.md](docs/security_notes.md).

## Testing

Manual test cases TC-01 through TC-11 are documented in [tests/test_cases.md](tests/test_cases.md). They cover valid and invalid data, filters, low-rated feedback, comment safety, and CSV download. The cases are documented for workshop verification and have not been marked as run automatically.

## Limitations

- The app reads a bundled CSV and does not provide data entry or persistence.
- It is a local educational prototype, not a production deployment.
- Invalid records are skipped rather than repaired.
- Manual browser interaction is needed to verify Streamlit UI behavior.

## Future improvements

- Add automated unit tests for the data validation function.
- Let an instructor upload a CSV after adding stricter upload limits and validation.
- Add date or session fields to support time-based summaries using synthetic data.
