import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_report(data_summary: str, dataset_name: str = "Uploaded Dataset") -> str:
    prompt = f"""
You are a senior data analyst. You have been given a statistical summary of a dataset called "{dataset_name}".

Here is the data summary:
{data_summary}

Write a professional analyst report with the following sections:

1. **Executive Summary** — A 3-4 sentence overview of what this dataset contains and its key characteristics.

2. **Key Findings** — 4-6 bullet points highlighting the most important patterns, trends, or statistics found in the data.

3. **Anomalies & Watch Points** — Any missing values, outliers, or unusual patterns that an analyst should be aware of.

4. **Recommendations** — 3-4 actionable recommendations based on the data for a business stakeholder.

Write in a clear, professional tone as if presenting to a non-technical executive. Do not use jargon. Be specific and reference actual numbers from the summary.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional data analyst who writes clear, insightful business reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content

def answer_question(question: str, report_text: str, dataset_name: str) -> str:
    prompt = f"""
You are a data analyst assistant. You have just generated an analyst report for a dataset called "{dataset_name}".

Here is the full report:
{report_text}

The user is asking the following question about this report:
"{question}"

Answer clearly and concisely based on the report content.
If the question is outside the scope of the report, say so and suggest what analysis would help.
Keep your answer to 3-5 sentences. Be direct and specific, referencing the report where relevant.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful analyst assistant who answers questions about data reports clearly and concisely."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300
    )

    return response.choices[0].message.content