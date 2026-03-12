import pandas as pd

def profile_dataframe(df):
    summary = []

    summary.append(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    summary.append(f"Columns: {', '.join(df.columns.tolist())}")

    summary.append("\n--- Column Types ---")
    for col in df.columns:
        dtype = df[col].dtype
        nulls = df[col].isnull().sum()
        summary.append(f"  '{col}': type={dtype}, nulls={nulls}")

    summary.append("\n--- Numeric Column Stats ---")
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        stats = df[col].describe()
        summary.append(
            f"  '{col}': min={stats['min']:.2f}, max={stats['max']:.2f}, "
            f"mean={stats['mean']:.2f}, std={stats['std']:.2f}"
        )

    summary.append("\n--- Text Column Samples ---")
    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        samples = df[col].dropna().head(3).tolist()
        summary.append(f"  '{col}' samples: {samples}")

    summary.append("\n--- Missing Values ---")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) == 0:
        summary.append("  No missing values found.")
    else:
        for col, count in missing.items():
            summary.append(f"  '{col}': {count} missing values")

    return "\n".join(summary)