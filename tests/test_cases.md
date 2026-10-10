# Manual Test Cases

Run the app with `streamlit run app.py` and use temporary copies of the CSV when testing invalid file cases. Record actual outcomes and mark Pass/Fail during the workshop.

| Test ID | Feature | Input/Precondition | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Valid CSV loads | Use the supplied CSV | Dashboard loads 40 synthetic records | Not run | Not run | Default dataset |
| TC-02 | Missing file | Temporarily move the CSV away | Friendly warning/error; no traceback | Not run | Not run | Restore file afterward |
| TC-03 | Missing column | CSV lacks `topic` | Clear missing-column message; dashboard stops safely | Not run | Not run | |
| TC-04 | Non-numeric rating | Set one rating to `abc` | Invalid row is skipped and user sees a warning | Not run | Not run | |
| TC-05 | Out-of-range rating | Set one rating to `6` or `0` | Invalid row is skipped and user sees a warning | Not run | Not run | |
| TC-06 | Empty dataset | Use a header-only CSV | Friendly empty-data message; no traceback | Not run | Not run | |
| TC-07 | Topic filter | Select only `Python Security` | Table and metrics show only that topic | Not run | Not run | |
| TC-08 | Rating filter | Set range to 4–5 | Table and metrics show only ratings 4 and 5 | Not run | Not run | |
| TC-09 | Low-rated summary | Use default filters | Dedicated section shows only ratings ≤ 2 | Not run | Not run | |
| TC-10 | Comment safety | Add `<script>alert("XSS")</script>` as comment | Comment appears as text; no JavaScript executes | Not run | Not run | Streamlit dataframe uses normal safe rendering |
| TC-11 | CSV download | Apply topic/rating filters and download | Download contains only visible filtered synthetic rows and required columns | Not run | Not run | |
