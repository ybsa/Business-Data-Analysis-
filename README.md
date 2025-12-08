# Business Data Analysis

## Overview

This project performs data analysis on inventory and sales data to generate actionable business insights. It includes an ETL (Extract, Transform, Load) process to migrate raw CSV data into a SQLite database and an analytical engine to visualize trends in sales, inventory turnover, and vendor performance.

## Key Features

- **ETL Pipeline**: Automated loading of CSV datasets (Sales, Inventory, Purchases, etc.) into a structured SQLite database (`inventory_sales.db`).
- **Data Analysis**:
  - **Underperforming Brands**: Identifies brands with low sales volume to optimize inventory.
  - **Top Vendors**: Highlights key vendor partnerships driving revenue.
  - **Bulk Purchasing Analysis**: Examines the correlation between order quantity and unit price.
  - **Inventory Turnover**: Calculates turnover rates to identify efficient vs. slow-moving stock.
- **Reporting**: Generates data-backed reports (CSV) and visualizations (charts) to support decision-making.

## Project Structure

`Business-Data-Analysis-/`
├── `load_data.py`       # Script to load CSV data into SQLite database
├── `analysis.py`        # Generic analysis script for generating reports and plots
├── `README.md`          # Project documentation
├── `inventory_sales.db` # SQLite database (generated)
├── `images/`            # Generated charts and visualizations
└── `reports/`           # Generated CSV summary reports

## Prerequisites

- Python 3.x
- Required libraries:

  ```bash
  pip install pandas matplotlib seaborn
  ```

## Usage

### 1. Data Loading

The `load_data.py` script initializes the database and loads data from raw CSV files.
**Note**: Ensure the `DATA_DIR` path in `load_data.py` points to your local data directory containing the CSV files.

```bash
python load_data.py
```

*This will create `inventory_sales.db` and log progress to `data_loading.log`.*

### 2. Running Analysis

The `analysis.py` script interprets the data, calculates metrics, and generates visualizations.

```bash
python analysis.py
```

*Outputs:*

- **Charts** in the `images/` directory (e.g., `brands.png`, `vendors.png`).
- **Data Reports** in the `reports/` directory (e.g., `top_vendors.csv`).
- **Summary**: `Business_Analysis_Summary.csv` containing key findings and recommendations.

## Generated Insights

The analysis focuses on answering key business questions:

- *Which brands are underperforming?*
- *Who are the top vendors?*
- *Does bulk purchasing lower costs?*
- *Which items have the highest inventory turnover?*

