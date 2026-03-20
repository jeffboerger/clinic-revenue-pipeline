# Clinic Revenue Pipeline

A Full ETL data Engineering Pipeline built on 7 years of real reveneue data from a chiropractic clinic near Austin Texas. 
Includes data cleaning, transformation, SQLite database loading, and an interactive Streamlit dashboard.

## Live Demo
[View the dashboard here](https://clinic-revenue-pipeline-odefttrp9eekfx34aqrveb.streamlit.app/)


## Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- Matplotlib
- Jupyter Notebooks


## Project Structure

- `data\` - Raw Excel source files and generated CSV/database outputs
- `notebooks\` - Expolratory data analysis notebook
- `scripts/etl.py` - ETL pipeline script
- `app.py` - Streamlit dashboard
- `requirements.txt` - Project dependencies


## How to Run

1. Clone the Repository
``` bash
git clone https://github.com/jeffboerger/clinic-revenue-pipeline.git
cd clinic-revenue-pipeline
```

2. Create and activate a virtual environment
```bash
python3 - m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the ETL pipeline
```bash
python scripts/etl.py
```

5. Launch the dashboard
```bash
streamlit run app.py
```


## Key Findings

- **$1,004,531** in total revenue generated over 7 years (2017-2023)
- **2022** was the strongest year at $187,025 — nearly 6x growth from the 
  partial first year
- **COVID impact was minimal** — only a 6% revenue drop in 2020, suggesting 
  the subscription model created sticky recurring revenue
- **Weight Loss (Ideal Protein)** represented nearly 50% of revenue in 2017-2018 
  but was phased out by 2020 as BTX subscriptions became the core business
- **Billing cycles are visible in the data** — revenue spikes on the 5th, 
  15th, and 20th of each month confirm subscription payment patterns
- **Large check anomaly identified** — 16 checks over $1,000 concentrated 
  between 2020-2023 may represent investor or bulk payments, flagged for 
  follow up with clinic ownership


## Background

This project was built as a portfolio piece using real financial data from 
Body Traxx Chiropractic, a clinic co-founded in Austin, TX in 2017. 

The data covers 7 years of daily revenue broken out by payment type 
(credit card, cash, check) and revenue stream (chiropractic subscriptions, 
supplements, and weight loss programs).

The clinic's subscription-based chiropractic model (BTX) grew from 
representing ~65% of revenue in 2017 to over 97% by 2023, reflecting 
a deliberate strategic pivot away from weight loss and supplement sales.

Note: All data used with permission. Patient data is excluded entirely — 
only financial and operational metrics are analyzed.

 
 ## Future Improvements

- Migrate from SQLite to PostgreSQL for production readiness
- Add expense data to enable full P&L analysis
- Schedule pipeline to run automatically with Apache Airflow
- Containerize with Docker for easy deployment
- Investigate large check anomaly with clinic ownership
 
 