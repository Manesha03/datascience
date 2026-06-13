# Retail Sales Analytics 

This repository presents a complete retail sales analytics project. It combines sales trend analysis, distribution analysis, outlier detection, and correlation analysis in one reproducible workflow.

The project covers:

1. Sales trend and category analysis
2. Distribution and outlier analysis
3. Correlation and relationship analysis

The project uses a reproducible synthetic retail sales dataset, generates all required PNG charts, and exports concise written summaries for submission.

## Project Structure

```text
.
|-- data/
|   `-- retail_sales.csv
|-- index.html
|-- outputs/
|   |-- charts/
|   |   |-- sales_trend_category_analysis/
|   |   |-- distribution_outlier_analysis/
|   |   `-- correlation_relationship_analysis/
|   `-- summaries/
|-- src/
|   `-- retail_sales_analytics.py
|-- data_science_task_brief.pdf
|-- requirements.txt
`-- README.md
```

## How To Run

Install the required packages if needed:

```bash
pip install -r requirements.txt
```

Run the full analysis:

```bash
python src/retail_sales_analytics.py
```

The script creates:

- `data/retail_sales.csv`
- PNG charts in `outputs/charts/`
- Short written summaries in `outputs/summaries/`
- Data quality, numeric summary, and category-region performance tables in `outputs/summaries/`

## View The Dashboard

Open `index.html` in a browser to view the generated charts and report links as a static dashboard.

The dashboard includes:

- Sticky navigation for major report sections
- In-page report previews instead of plain text file opening
- Methodology and data preparation notes
- Variable structure, data quality, descriptive summary, limitation, and next-step previews

## Deliverables

### Sales Trend and Category Analysis

- Daily sales line chart
- Monthly sales line chart
- Quarterly sales bar chart
- Category revenue comparison bar chart
- Category revenue share pie chart
- Summary discussing chart choices, labels, legends, and axes

### Distribution and Outlier Analysis

- Revenue histogram with KDE
- Revenue box plot by region
- Revenue KDE by region
- Outlier table
- One-paragraph interpretation covering spread, skewness, group comparison, and outliers

### Correlation and Relationship Analysis

- Pearson correlation matrix
- Masked annotated correlation heatmap
- Pairplot for key variables
- Summary of strongest positive and negative relationships

## Dataset Notes

The dataset is generated with a fixed random seed so results are reproducible. It includes order dates, categories, regions, units sold, unit price, discounts, shipping days, customer satisfaction, marketing spend, revenue, profit, and profit margin.
