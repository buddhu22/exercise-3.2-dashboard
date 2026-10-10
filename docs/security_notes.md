# Security Notes (Viva-Friendly)

- **Validate CSV data:** A CSV may be edited or malformed. The app checks required columns, numeric ratings in the 1–5 range, and non-empty identifiers/topics/comments. Invalid rows are skipped and summarized to the user.
- **Treat comments as untrusted input:** Comments can contain arbitrary text, including strings that look like code. The dashboard shows them in a regular Streamlit dataframe and never interprets them.
- **Avoid raw HTML and JavaScript:** Executing markup from feedback could allow a malicious comment to run script in a browser. The app does not enable `unsafe_allow_html` for comments.
- **Avoid `eval()` and `exec()`:** These functions can run text as Python code. The project has no need to execute data as code.
- **Use synthetic data only:** The included examples are invented and contain no student identities or contact details, reducing privacy risk during a classroom demonstration.
- **Keep this a local prototype:** The dashboard reads a bundled local CSV and has no public API or external database. It is intended for workshop learning, not production deployment or collection of real feedback.
- **Show safe errors:** Users receive short validation messages instead of stack traces, local paths, or internal exceptions. This avoids exposing implementation details.
- **Use predictable paths:** The dataset path is built relative to `app.py` with `pathlib`, rather than accepting a user-supplied path.
- **Keep secrets out of source:** The app has no credentials or secrets. `.env` files are ignored by Git.

These controls demonstrate basic secure development practices; they do not make a classroom prototype suitable for production use.
