import pandas as pd
import plotly.io as pio
import re

def clean_text_html(text):
    text = text.replace('\u2014', '-')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    return text


def generate_data_quality_section(df):
    total_rows = df.shape[0]
    total_cols = df.shape[1]
    
    # Missing values
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    
    # Duplicates
    duplicate_count = df.duplicated().sum()
    
    # Data types breakdown
    numeric_count = len(df.select_dtypes(include='number').columns)
    categorical_count = len(df.select_dtypes(include='object').columns)
    
    # Health score calculation
    missing_penalty = (len(missing_cols) / total_cols) * 40
    duplicate_penalty = min((duplicate_count / total_rows) * 40, 40)
    health_score = max(0, 100 - missing_penalty - duplicate_penalty)
    
    if health_score >= 80:
        score_color = "#10B981"
        score_label = "Good"
        score_emoji = "✅"
    elif health_score >= 60:
        score_color = "#F59E0B"
        score_label = "Fair"
        score_emoji = "⚠️"
    else:
        score_color = "#EF4444"
        score_label = "Poor"
        score_emoji = "❌"

    # Missing values detail
    if len(missing_cols) == 0:
        missing_html = '<p class="quality-good">✅ No missing values found across all columns.</p>'
    else:
        rows = ""
        for col, count in missing_cols.items():
            pct = (count / total_rows) * 100
            rows += f'<tr><td>{col}</td><td>{count}</td><td>{pct:.1f}%</td></tr>'
        missing_html = f'''
        <table class="quality-table">
            <thead><tr><th>Column</th><th>Missing Count</th><th>% Missing</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>'''

    duplicate_html = (
        '<p class="quality-good">✅ No duplicate rows found.</p>'
        if duplicate_count == 0
        else f'<p class="quality-warn">⚠️ {duplicate_count} duplicate rows detected ({(duplicate_count/total_rows)*100:.1f}% of data).</p>'
    )

    return f'''
    <div class="section quality-section">
        <h2>🔍 Data Quality Report</h2>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_rows:,}</div>
                <div class="stat-label">Total Rows</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_cols}</div>
                <div class="stat-label">Total Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{numeric_count}</div>
                <div class="stat-label">Numeric Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{categorical_count}</div>
                <div class="stat-label">Categorical Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: {score_color}">{health_score:.0f}/100</div>
                <div class="stat-label">Health Score {score_emoji}</div>
            </div>
        </div>

        <div class="quality-subsection">
            <h3>Missing Values</h3>
            {missing_html}
        </div>

        <div class="quality-subsection">
            <h3>Duplicate Rows</h3>
            {duplicate_html}
        </div>
    </div>
    '''


def format_report_html(report_text):
    report_text = clean_text_html(report_text)
    lines = report_text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue

        if line.startswith('## ') or line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            heading = line.lstrip('#').strip()
            html_lines.append(f'<h2>{heading}</h2>')

        elif re.match(r'^\d+\.', line) or line.startswith('-') or line.startswith('•'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            line = line.lstrip('-•0123456789.').strip()
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f'<li>{line}</li>')

        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f'<p>{line}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def generate_html_report(report_text: str, df: pd.DataFrame, dataset_name: str = "Dataset") -> str:
    quality_section = generate_data_quality_section(df)
    report_html = format_report_html(report_text)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NarrateIQ Report - {dataset_name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #F3F4F6;
            color: #111827;
            line-height: 1.75;
        }}

        .header {{
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            padding: 52px 48px;
        }}

        .header-inner {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .header h1 {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}

        .header .subtitle {{
            opacity: 0.8;
            font-size: 0.95rem;
            margin-bottom: 16px;
        }}

        .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 36px 24px 60px;
        }}

        .section {{
            background: white;
            border-radius: 16px;
            padding: 36px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
        }}

        h2 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #4F46E5;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #EEF2FF;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        h3 {{
            font-size: 0.9rem;
            font-weight: 600;
            color: #374151;
            margin: 20px 0 10px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}

        p {{
            margin-bottom: 14px;
            color: #374151;
            font-size: 0.95rem;
        }}

        ul {{
            margin: 8px 0 16px 0;
            padding-left: 0;
            list-style: none;
        }}

        li {{
            color: #374151;
            font-size: 0.95rem;
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
        }}

        li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #4F46E5;
            font-weight: 600;
        }}

        strong {{ color: #111827; font-weight: 600; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 28px;
        }}

        .stat-card {{
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
        }}

        .stat-number {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #4F46E5;
            margin-bottom: 4px;
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: #6B7280;
            font-weight: 500;
        }}

        .quality-subsection {{
            margin-top: 20px;
        }}

        .quality-good {{
            color: #059669;
            font-weight: 500;
            background: #ECFDF5;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        .quality-warn {{
            color: #D97706;
            font-weight: 500;
            background: #FFFBEB;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        .quality-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            margin-top: 8px;
        }}

        .quality-table th {{
            background: #F9FAFB;
            padding: 10px 14px;
            text-align: left;
            font-weight: 600;
            color: #374151;
            border-bottom: 1px solid #E5E7EB;
        }}

        .quality-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid #F3F4F6;
            color: #374151;
        }}

        .footer {{
            text-align: center;
            padding: 24px;
            color: #9CA3AF;
            font-size: 0.8rem;
        }}

        @media print {{
            body {{ background: white; }}
            .header {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-inner">
            <h1>📊 NarrateIQ</h1>
            <div class="subtitle">AI-Generated Analyst Report</div>
            <div class="badge">📁 {dataset_name}</div>
        </div>
    </div>

    <div class="container">
        {quality_section}
        <div class="section">
            {report_html}
        </div>
    </div>

    <div class="footer">
        Generated by NarrateIQ &nbsp;·&nbsp; AI-Powered Analyst Report Generator
    </div>
</body>
</html>'''

    return html