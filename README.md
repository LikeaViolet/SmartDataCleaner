# Smart Data Cleaner

A reusable Python application that cleans CSV and Excel files, exports the cleaned dataset, and produces a clear report showing what changed.

## Current features

- Reads CSV, XLSX, and XLS files
- Removes completely blank rows
- Trims extra spaces from text values
- Removes exact duplicate rows
- Optionally converts selected columns to title case
- Reports missing values by column
- Exports cleaned data to CSV or Excel
- Generates text and JSON cleaning reports
- Includes automated tests

## Why title casing is optional

Automatically capitalizing every text column can corrupt emails, URLs, IDs, and product codes. You must explicitly name the columns that should be changed.

## Setup

```bash
cd smart-data-cleaner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
```

## Run the sample

```bash
python main.py input/sample_customers.csv \
  --output output/cleaned_customers.xlsx \
  --title-case Name City
```

The application creates:

```text
output/cleaned_customers.xlsx
output/cleaning_report.txt
output/cleaning_report.json
```

## Run tests

```bash
pytest
```

## Portfolio roadmap

Version 1.1:
- Email validation
- Phone-number normalization
- Date detection and standardization

Version 1.2:
- Before-and-after issue report
- Configurable cleaning rules

Version 2:
- Streamlit upload interface
- Download buttons
- Data-quality score
