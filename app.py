"""Local dashboard for exploring synthetic workshop feedback."""

from pathlib import Path

import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = ["session_id", "rating", "topic", "comment"]
DATA_FILE = Path(__file__).parent / "data" / "workshop_feedback.csv"


def load_feedback(file_path: Path) -> tuple[pd.DataFrame | None, list[str]]:
    """Load and validate feedback, returning safe row-level issue summaries."""
    if not file_path.is_file():
        return None, ["The feedback CSV file is missing. Restore data/workshop_feedback.csv and restart the app."]

    try:
        feedback = pd.read_csv(file_path, dtype={"session_id": "string", "topic": "string", "comment": "string"})
    except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError):
        return None, ["The feedback CSV could not be read. Check that it is a valid, non-empty CSV file."]

    missing = [column for column in REQUIRED_COLUMNS if column not in feedback.columns]
    if missing:
        return None, ["The feedback CSV is missing required columns: " + ", ".join(missing) + "."]
    if feedback.empty:
        return None, ["The feedback CSV contains no feedback records."]

    feedback = feedback[REQUIRED_COLUMNS].copy()
    feedback["rating"] = pd.to_numeric(feedback["rating"], errors="coerce")
    valid_rating = feedback["rating"].notna() & feedback["rating"].between(1, 5)
    valid_topic = feedback["topic"].fillna("").str.strip().ne("")
    valid_session = feedback["session_id"].fillna("").str.strip().ne("")
    valid_comment = feedback["comment"].notna()
    invalid_count = int((~(valid_rating & valid_topic & valid_session & valid_comment)).sum())
    feedback = feedback.loc[valid_rating & valid_topic & valid_session & valid_comment].copy()
    feedback["rating"] = feedback["rating"].astype(int)

    issues = []
    if invalid_count:
        issues.append(f"Skipped {invalid_count} invalid row(s). Ratings must be numeric values from 1 to 5; session IDs, topics, and comments must be present, and topics cannot be blank.")
    if feedback.empty:
        return None, issues + ["No valid feedback records remain after validation."]
    return feedback, issues


def main() -> None:
    st.set_page_config(page_title="Workshop Feedback Explorer", page_icon="📊", layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(180deg, #f3f7fb 0%, #f8fafc 240px, #f8fafc 100%); }
        .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3rem; }
        [data-testid="stMetric"] { background: white; border: 1px solid #e4ebf3; border-radius: 14px; padding: 18px 20px; box-shadow: 0 4px 14px rgba(25, 50, 80, .045); }
        [data-testid="stMetricLabel"] { color: #60738a; }
        [data-testid="stMetricValue"] { color: #15304b; }
        [data-testid="stDataFrame"] { border: 1px solid #e4ebf3; border-radius: 12px; overflow: hidden; }
        .hero { background: linear-gradient(120deg, #123c69, #176b87); color: white; padding: 28px 32px; border-radius: 18px; margin-bottom: 24px; box-shadow: 0 12px 28px rgba(18, 60, 105, .16); }
        .hero h1 { color: white; font-size: 2.15rem; margin: 0 0 7px 0; }
        .hero p { color: #e4f1f7; font-size: 1.02rem; margin: 0; }
        .section-note { color: #6b7c90; margin-top: -10px; margin-bottom: 14px; }
        </style>
        <div class="hero">
          <h1>Workshop Feedback Explorer</h1>
          <p>Simple insights from synthetic feedback · Secure Application Development Workshop</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Local learning dashboard • Synthetic data only • No real personal information")

    feedback, issues = load_feedback(DATA_FILE)
    for issue in issues:
        st.warning(issue)
    if feedback is None:
        st.error("Feedback data is unavailable. Please check the dataset and try again.")
        return

    st.subheader("Filter feedback", divider="blue")
    st.markdown('<p class="section-note">Choose topics and ratings to update the dashboard.</p>', unsafe_allow_html=True)
    topic_options = sorted(feedback["topic"].unique().tolist())
    filter_columns = st.columns([1.4, 1])
    with filter_columns[0]:
        topic_selection = st.multiselect("Workshop topics", topic_options, default=topic_options, help="Choose one or more topics.")
    with filter_columns[1]:
        rating_range = st.slider("Rating range", min_value=1, max_value=5, value=(1, 5), step=1)

    # Filtering creates a separate dataframe and leaves the validated source intact.
    filtered = feedback.loc[
        feedback["topic"].isin(topic_selection)
        & feedback["rating"].between(rating_range[0], rating_range[1])
    ].copy()
    low_rated = filtered.loc[filtered["rating"] <= 2].copy()

    st.subheader("At a glance", divider="blue")
    metric_columns = st.columns(4)
    metric_columns[0].metric("Total Responses", len(filtered))
    metric_columns[1].metric("Average Rating", f"{filtered['rating'].mean():.2f}" if not filtered.empty else "—")
    metric_columns[2].metric("Topics", filtered["topic"].nunique())
    metric_columns[3].metric("Low Rated (≤ 2)", len(low_rated))

    st.subheader("Feedback records", divider="blue")
    st.markdown('<p class="section-note">Comments are shown as plain text.</p>', unsafe_allow_html=True)
    st.dataframe(filtered[REQUIRED_COLUMNS], use_container_width=True, hide_index=True)

    st.subheader("Needs attention · Low-rated feedback", divider="orange")
    if low_rated.empty:
        st.info("No low-rated feedback found for the current filters.")
    else:
        st.dataframe(low_rated[REQUIRED_COLUMNS], use_container_width=True, hide_index=True)

    st.subheader("Average rating by topic", divider="blue")
    if filtered.empty:
        st.info("No records match the current filters, so there is no chart to display.")
    else:
        averages = filtered.groupby("topic")["rating"].mean().sort_index()
        st.bar_chart(averages, y_label="Average rating (1–5)")

    st.subheader("Export", divider="blue")
    st.write("Save the records currently shown in the dashboard.")
    st.download_button(
        "⬇  Download filtered feedback as CSV",
        data=filtered[REQUIRED_COLUMNS].to_csv(index=False).encode("utf-8"),
        file_name="filtered_workshop_feedback.csv",
        mime="text/csv",
        disabled=filtered.empty,
        type="primary",
    )

    st.divider()
    st.caption("Workshop Feedback Explorer · Built with Streamlit · Comments are treated as plain text.")


if __name__ == "__main__":
    main()
