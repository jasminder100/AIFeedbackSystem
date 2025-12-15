import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

from llm_utils import (
    generate_user_response,
    generate_summary,
    generate_recommended_action
)

# --------------------------------------------------
# CONFIG & SETUP
# --------------------------------------------------

st.set_page_config(page_title="AI Feedback System", layout="wide")

load_dotenv()

DATA_FILE = "Feedback5.csv"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["User Dashboard", "Admin Dashboard"])

# --------------------------------------------------
# USER DASHBOARD (PUBLIC-FACING)
# --------------------------------------------------

if page == "User Dashboard":
    st.title("📝 Customer Feedback")

    with st.form("feedback_form"):
        rating = st.selectbox("Select your rating", [1, 2, 3, 4, 5])
        review = st.text_area("Write your review")
        submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if review.strip() == "":
            st.warning("Please enter a review before submitting.")
        else:
            with st.spinner("Generating AI response..."):
                ai_response = generate_user_response(rating, review)
                ai_summary = generate_summary(review)
                ai_action = generate_recommended_action(review)

                new_row = {
                    "timestamp": datetime.now(),
                    "user_rating": rating,
                    "user_review": review,
                    "ai_response": ai_response,
                    "ai_summary": ai_summary,
                    "ai_recommended_action": ai_action
                }

                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

            st.success("Feedback submitted successfully!")
            st.subheader("AI Response")
            st.write(ai_response)

# --------------------------------------------------
# ADMIN DASHBOARD (INTERNAL-FACING)
# --------------------------------------------------

elif page == "Admin Dashboard":
    st.title("🔐 Admin Dashboard")

    # ---------- Authentication ----------
    if not st.session_state.admin_authenticated:
        st.subheader("Admin Login")

        password_input = st.text_input("Enter admin password", type="password")

        if st.button("Login"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Access granted")
                st.rerun()
            else:
                st.error("Incorrect password")

        st.stop()

    # ---------- Admin Content ----------
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        st.info("No feedback submissions yet.")
        st.stop()

    # Convert timestamp to datetime (for filtering & sorting)
    df["timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # --------------------------------------------------
    # FILTERS (ADMIN ONLY)
    # --------------------------------------------------

    st.sidebar.subheader("Admin Filters")

    rating_filter = st.sidebar.multiselect(
        "Filter by Rating",
        options=sorted(df["user_rating"].dropna().unique()),
        default=sorted(df["user_rating"].dropna().unique())
    )

    min_date = df["timestamp_dt"].min().date()
    max_date = df["timestamp_dt"].max().date()

    date_range = st.sidebar.date_input(
        "Filter by Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply filters
    filtered_df = df[
        (df["user_rating"].isin(rating_filter)) &
        (df["timestamp_dt"].dt.date >= date_range[0]) &
        (df["timestamp_dt"].dt.date <= date_range[1])
    ]

    # Sort by latest feedback
    filtered_df = filtered_df.sort_values("timestamp_dt", ascending=False)

    # Format timestamp for display
    filtered_df["timestamp"] = filtered_df["timestamp_dt"].dt.strftime(
        "%d/%m/%Y %I:%M %p"
    )

    # Drop helper column before display
    filtered_df = filtered_df.drop(columns=["timestamp_dt"])

    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    st.subheader("📋 All Feedback")
    st.dataframe(filtered_df, use_container_width=True)

    # Download button
    st.download_button(
        label="⬇️ Download Feedback CSV",
        data=filtered_df.to_csv(index=False),
        file_name="feedback_export.csv",
        mime="text/csv"
    )

    # --------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------

    st.subheader("📈 Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Reviews", len(filtered_df))
    col2.metric(
        "Average Rating",
        round(filtered_df["user_rating"].mean(), 2)
        if not filtered_df.empty else 0
    )
    col3.metric(
        "Low Ratings (≤ 2)",
        len(filtered_df[filtered_df["user_rating"] <= 2])
    )

    st.subheader("🚨 Reviews Needing Attention")
    low_rating_df = filtered_df[filtered_df["user_rating"] <= 2]

    if low_rating_df.empty:
        st.success("No critical reviews 🎉")
    else:
        st.dataframe(low_rating_df, use_container_width=True)
