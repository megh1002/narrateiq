import streamlit as st
import pandas as pd
from profiler import profile_dataframe
from narrator import generate_report, answer_question
from html_report_generator import generate_html_report
import base64

# --- Page Config ---
st.set_page_config(
    page_title="NarrateIQ",
    page_icon="📊",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5, #7C3AED);
            color: white;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            width: 100%;
        }
        .stButton > button:hover { opacity: 0.9; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("## 📊 NarrateIQ")
st.markdown("#### AI-Powered Analyst Report Generator")
st.markdown("Upload any CSV dataset and get a professional analyst report — with data quality checks, AI-written insights, and a Q&A assistant — in seconds.")
st.divider()

# --- Session State ---
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "report_text" not in st.session_state:
    st.session_state.report_text = ""
if "data_summary" not in st.session_state:
    st.session_state.data_summary = ""
if "html_report" not in st.session_state:
    st.session_state.html_report = ""
if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- File Upload ---
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
    help="Supports any CSV file up to 200MB"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    dataset_name = (
        uploaded_file.name
        .replace(".csv", "")
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )

    # Dataset stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", df.shape[1])
    col3.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")

    with st.expander("👀 Preview Dataset", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

    st.divider()

    if st.button("✨ Generate AI Report"):
        # Reset chat history for new report
        st.session_state.chat_history = []

        progress = st.progress(0, text="Starting analysis...")

        with st.spinner(""):
            progress.progress(20, text="📊 Profiling your dataset...")
            data_summary = profile_dataframe(df)

            progress.progress(50, text="🤖 Generating AI insights...")
            report_text = generate_report(data_summary, dataset_name)

            progress.progress(80, text="🎨 Building your report...")
            html_report = generate_html_report(report_text, df, dataset_name)

            progress.progress(100, text="✅ Done!")

        # Save to session state
        st.session_state.report_generated = True
        st.session_state.report_text = report_text
        st.session_state.data_summary = data_summary
        st.session_state.html_report = html_report
        st.session_state.dataset_name = dataset_name

    # --- Show Report if Generated ---
    if st.session_state.report_generated:
        st.success("Report generated successfully!")
        st.markdown("### 📝 Your Analyst Report")
        st.components.v1.html(st.session_state.html_report, height=950, scrolling=True)
        st.divider()

        # Download button
        b64 = base64.b64encode(st.session_state.html_report.encode()).decode()
        href = f'''
        <a href="data:text/html;base64,{b64}"
           download="{st.session_state.dataset_name}_NarrateIQ_Report.html"
           style="display:inline-block;padding:12px 28px;
                  background:linear-gradient(135deg,#4F46E5,#7C3AED);
                  color:white;border-radius:8px;text-decoration:none;
                  font-weight:600;font-size:0.95rem;">
            ⬇️ Download Full Report
        </a>
        <span style="margin-left:12px;color:#6B7280;font-size:0.85rem;">
            Open in browser → Cmd+P to save as PDF
        </span>
        '''
        st.markdown(href, unsafe_allow_html=True)

        # --- Q&A Section ---
        st.divider()
        st.markdown("### 💬 Ask Questions About This Report")
        st.caption("Ask the AI to clarify, expand on, or prioritize insights from the report above.")

        # Suggested questions
        st.markdown("**Suggested questions:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("What should I prioritize first?"):
                st.session_state.chat_history.append({"role": "user", "content": "What should I prioritize first?"})
            if st.button("Explain the anomalies in simple terms"):
                st.session_state.chat_history.append({"role": "user", "content": "Explain the anomalies in simple terms"})
        with col2:
            if st.button("What are the biggest risks?"):
                st.session_state.chat_history.append({"role": "user", "content": "What are the biggest risks?"})
            if st.button("Summarize this for a non-technical stakeholder"):
                st.session_state.chat_history.append({"role": "user", "content": "Summarize this for a non-technical stakeholder"})

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Answer any pending questions from buttons
        if (st.session_state.chat_history and
                st.session_state.chat_history[-1]["role"] == "user" and
                len(st.session_state.chat_history) % 2 != 0):
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = answer_question(
                        st.session_state.chat_history[-1]["content"],
                        st.session_state.report_text,
                        st.session_state.dataset_name
                    )
                st.markdown(answer)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

        # Chat input
        if question := st.chat_input("Ask anything about this report..."):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = answer_question(
                        question,
                        st.session_state.report_text,
                        st.session_state.dataset_name
                    )
                st.markdown(answer)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

else:
    st.markdown("#### What kind of datasets work?")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🛍️ E-commerce & Retail")
        st.info("📣 Marketing Campaigns")
        st.info("📋 Survey Responses")
    with col2:
        st.info("💰 Financial Records")
        st.info("📦 Supply Chain Data")
        st.info("👥 HR & People Data")