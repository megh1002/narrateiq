# NarrateIQ — AI-Powered Analyst Report Generator

NarrateIQ is an AI-powered data analysis tool that transforms any CSV dataset into a 
professional analyst report — with automated data quality checks, AI-written insights, 
and an interactive Q&A assistant — in seconds.

## What It Does

1. **Upload any CSV** — sales data, survey responses, financial records, anything
2. **Automated Data Quality Audit** — health score, missing values, duplicate detection
3. **AI-Generated Report** — executive summary, key findings, anomalies, recommendations
4. **Interactive Q&A** — ask follow-up questions about the report in plain English
5. **Download Report** — export as a styled HTML report, printable to PDF

## Why I Built This

As a data analyst, writing narrative reports from data is one of the most time-consuming 
parts of the workflow. NarrateIQ automates that last mile — turning raw data into 
stakeholder-ready insights in one click.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Engine | OpenAI GPT-4o-mini API |
| Data Profiling | Python, Pandas |
| Frontend | Streamlit |
| Report Generation | HTML, CSS |
| Prompt Engineering | Role prompting, context summarization |

## Architecture
```
CSV Upload → Data Profiler → OpenAI API → HTML Report Generator → Streamlit App
```

- **profiler.py** — Condenses any size dataset into a smart statistical summary before 
sending to the LLM, solving the context window limitation
- **narrator.py** — Sends the summary to OpenAI with carefully engineered prompts, 
returns structured analyst report
- **html_report_generator.py** — Formats AI output into a clean, styled HTML report 
with data quality metrics
- **app.py** — Streamlit interface with progress tracking, report display, and Q&A chat

## Run Locally

1. Clone the repo:
```bash
git clone https://github.com/megh1002/narrateiq.git
cd narrateiq
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add your OpenAI API key:
```bash
# Create a .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

5. Run the app:
```bash
streamlit run app.py
```

## 📁 Project Structure
```
narrateiq/
├── app.py                    # Streamlit application
├── profiler.py               # Data profiling module
├── narrator.py               # OpenAI API integration
├── html_report_generator.py  # Report formatting
├── requirements.txt          # Dependencies
├── .env                      # API key (not committed)
└── .gitignore
```

## Key Technical Decisions

- **Data summarization before LLM prompting** — handles datasets of any size by 
profiling first, solving the context window problem
- **Separation of concerns** — each module does one job, making the codebase 
maintainable and extensible
- **Report-scoped Q&A** — questions are answered based on the generated report, 
keeping responses accurate and relevant