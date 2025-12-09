import streamlit as st
import sqlite3
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Job Hunter Insights",
    page_icon="🤖",
    layout="wide"
)

# --- HEADER ---
st.title("🤖 Job Hunter Bot - Analytics Dashboard")
st.markdown("Real-time monitoring of the automated recruitment pipeline.")
st.divider()

# --- DATA LOADING ---
def load_data():
    """
    Connects to the SQLite database and loads data into a Pandas DataFrame.
    """
    try:
        conn = sqlite3.connect('jobs.db')
        # Load all jobs, sorted by most recent
        df = pd.read_sql_query("SELECT * FROM jobs ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

# Load the data
df = load_data()

# --- METRICS SECTION ---
if not df.empty:
    # Create 3 columns for metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Jobs Found", value=len(df))

    with col2:
        # Count how many jobs have been sent to Discord (if you use the 'sent' column)
        # For now, we assume all saved jobs were sent.
        unique_companies = df['company'].nunique()
        st.metric(label="Unique Companies", value=unique_companies)

    with col3:
        # Simple Logic to detect 'Junior' roles for the metric
        junior_jobs = df[df['title'].str.contains('Junior|Entry|Associate', case=False, regex=True)]
        st.metric(label="Entry-Level Opportunities", value=len(junior_jobs))

    # --- CHARTS SECTION ---
    st.subheader("📊 Market Demand (Tech Stack)")

    # 1. Define keywords to analyze
    target_skills = ["Python", "SQL", "Data", "React", "AWS", "Backend", "Full Stack", "Django", "FastAPI"]

    # 2. Count occurrences of each keyword in job titles
    skill_counts = {}
    for skill in target_skills:
        # Check if the skill exists in the title (case insensitive)
        count = df['title'].str.contains(skill, case=False).sum()
        if count > 0:
            skill_counts[skill] = count

    # 3. Create a DataFrame for the chart
    if skill_counts:
        df_skills = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Count'])
        df_skills = df_skills.sort_values(by='Count', ascending=False)

        # Display Bar Chart
        st.bar_chart(df_skills.set_index('Skill'), color="#3498db")
    else:
        st.info("Not enough data to generate the skills chart yet.")

    # --- DATA TABLE SECTION ---
    st.subheader("📋 Recent Job Logs")

    # Show an interactive table (filtering only necessary columns)
    st.dataframe(
        df[['id', 'title', 'company', 'url']],
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No data found in 'jobs.db'. Please run 'main.py' to fetch jobs first.")

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("Pipeline Status")
    st.success("System Active")
    st.markdown(f"**Database:** SQLite")
    st.markdown(f"**Last Update:** {time.strftime('%H:%M:%S')}")

    if st.button("Refresh Data"):
        st.rerun()