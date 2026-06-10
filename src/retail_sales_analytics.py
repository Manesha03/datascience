from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CHART_DIR = ROOT / "outputs" / "charts"
SUMMARY_DIR = ROOT / "outputs" / "summaries"

SALES_TREND_DIR = CHART_DIR / "sales_trend_category_analysis"
DISTRIBUTION_DIR = CHART_DIR / "distribution_outlier_analysis"
CORRELATION_DIR = CHART_DIR / "correlation_relationship_analysis"


def prepare_directories() -> None:
    for path in [DATA_DIR, SUMMARY_DIR, SALES_TREND_DIR, DISTRIBUTION_DIR, CORRELATION_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def configure_plots() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 180,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.titlesize": 13,
            "legend.frameon": True,
        }
    )


def currency_axis(ax: plt.Axes) -> None:
    ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")


def save_current_figure(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def generate_sales_data(path: Path) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    categories = ["Electronics", "Fashion", "Home", "Beauty", "Sports"]
    regions = ["North", "South", "East", "West"]

    rows = []
    category_base_price = {
        "Electronics": 420,
        "Fashion": 95,
        "Home": 185,
        "Beauty": 55,
        "Sports": 130,
    }
    region_multiplier = {"North": 1.12, "South": 0.94, "East": 1.03, "West": 1.0}

    for day in dates:
        month = day.month
        seasonal_boost = 1 + 0.20 * np.sin((month - 1) / 12 * 2 * np.pi)
        weekend_boost = 1.18 if day.dayofweek >= 5 else 1.0
        orders_today = int(rng.integers(10, 22))

        for _ in range(orders_today):
            category = rng.choice(categories, p=[0.24, 0.25, 0.18, 0.17, 0.16])
            region = rng.choice(regions, p=[0.28, 0.24, 0.25, 0.23])
            units_sold = int(max(1, rng.poisson(3.2) + 1))
            unit_price = category_base_price[category] * rng.normal(1, 0.12)
            discount_rate = float(np.clip(rng.normal(0.10, 0.04), 0, 0.25))
            marketing_spend = float(rng.gamma(4.0, 18.0))
            shipping_days = int(np.clip(round(rng.normal(3.2, 1.1)), 1, 7))

            revenue = (
                units_sold
                * unit_price
                * (1 - discount_rate)
                * region_multiplier[region]
                * seasonal_boost
                * weekend_boost
            )
            cost_ratio = rng.normal(0.62, 0.06)
            profit = revenue * (1 - cost_ratio) - marketing_spend * 0.35
            satisfaction = np.clip(
                rng.normal(4.2, 0.35)
                + (0.15 if shipping_days <= 2 else -0.08 if shipping_days >= 5 else 0),
                2.5,
                5.0,
            )

            rows.append(
                {
                    "order_date": day,
                    "category": category,
                    "region": region,
                    "units_sold": units_sold,
                    "unit_price": round(unit_price, 2),
                    "discount_rate": round(discount_rate, 3),
                    "marketing_spend": round(marketing_spend, 2),
                    "shipping_days": shipping_days,
                    "customer_satisfaction": round(satisfaction, 2),
                    "revenue": round(revenue, 2),
                    "profit": round(profit, 2),
                }
            )

    df = pd.DataFrame(rows)
    df["profit_margin"] = (df["profit"] / df["revenue"]).round(3)
    df.to_csv(path, index=False)
    return df


def analyze_sales_trends_and_categories(df: pd.DataFrame) -> None:
    daily_sales = df.groupby("order_date", as_index=False)["revenue"].sum()
    monthly_sales = df.set_index("order_date").resample("ME")["revenue"].sum()
    quarterly_sales = df.set_index("order_date").resample("QE")["revenue"].sum()
    category_sales = df.groupby("category", as_index=False)["revenue"].sum().sort_values(
        "revenue", ascending=False
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=daily_sales, x="order_date", y="revenue", ax=ax, color="#1f77b4")
    ax.set_title("Daily Sales Revenue Across 2025")
    ax.set_xlabel("Order Date")
    ax.set_ylabel("Revenue")
    currency_axis(ax)
    save_current_figure(SALES_TREND_DIR / "daily_sales_line.png")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly_sales.index.strftime("%b"), monthly_sales.values, marker="o", linewidth=2.4)
    ax.set_title("Monthly Sales Aggregation")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    currency_axis(ax)
    save_current_figure(SALES_TREND_DIR / "monthly_sales_line.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(quarterly_sales.index.to_period("Q").astype(str), quarterly_sales.values, color="#2ca02c")
    ax.set_title("Quarterly Sales Aggregation")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Revenue")
    currency_axis(ax)
    save_current_figure(SALES_TREND_DIR / "quarterly_sales_bar.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=category_sales, x="category", y="revenue", ax=ax, palette="Set2", hue="category", legend=False)
    ax.set_title("Revenue by Product Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue")
    currency_axis(ax)
    save_current_figure(SALES_TREND_DIR / "category_revenue_bar.png")

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        category_sales["revenue"],
        labels=category_sales["category"],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
    )
    ax.set_title("Category Share of Total Revenue")
    save_current_figure(SALES_TREND_DIR / "category_revenue_share_pie.png")

    top_category = category_sales.iloc[0]
    best_month = monthly_sales.idxmax().strftime("%B")
    summary = f"""Sales Trend and Category Analysis Summary

The line charts are used for daily and monthly sales because they clearly show changes over time, including seasonality, peaks, and dips. The daily view preserves detail, while the monthly aggregation smooths short-term noise and makes the yearly trend easier to read. A bar chart is used for quarterly sales and category comparison because bars make discrete groups easy to compare. A pie chart is included only for category share, where the goal is to communicate each category's contribution to the whole.

Key findings:
- Total records analyzed: {len(df):,}
- Total revenue: ${df["revenue"].sum():,.2f}
- Best revenue month: {best_month}
- Top category: {top_category["category"]} (${top_category["revenue"]:,.2f})

Formatting choices:
- Clear chart titles explain the question each chart answers.
- Axes use readable date/category labels and currency formatting for revenue.
- Legends are used only where they add meaning, avoiding unnecessary visual clutter.
- PNG exports are saved in outputs/charts/sales_trend_category_analysis.
"""
    (SUMMARY_DIR / "sales_trend_category_summary.txt").write_text(summary, encoding="utf-8")


def analyze_distributions_and_outliers(df: pd.DataFrame) -> None:
    revenue = df["revenue"]
    q1 = revenue.quantile(0.25)
    q3 = revenue.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(revenue < lower_bound) | (revenue > upper_bound)].copy()
    outliers.sort_values("revenue", ascending=False).head(25).to_csv(
        SUMMARY_DIR / "top_revenue_outliers.csv", index=False
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=df, x="revenue", kde=True, bins=35, ax=ax, color="#4c78a8")
    ax.set_title("Revenue Distribution with KDE")
    ax.set_xlabel("Order Revenue")
    ax.set_ylabel("Order Count")
    save_current_figure(DISTRIBUTION_DIR / "revenue_histogram_kde.png")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df, x="region", y="revenue", ax=ax, palette="Set3", hue="region", legend=False)
    ax.set_title("Revenue Spread and Outliers by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Order Revenue")
    currency_axis(ax)
    save_current_figure(DISTRIBUTION_DIR / "revenue_boxplot_by_region.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.kdeplot(data=df, x="revenue", hue="region", fill=True, common_norm=False, alpha=0.25, ax=ax)
    ax.set_title("Revenue Distribution Comparison by Region")
    ax.set_xlabel("Order Revenue")
    ax.set_ylabel("Density")
    save_current_figure(DISTRIBUTION_DIR / "revenue_kde_by_region.png")

    skewness = revenue.skew()
    region_medians = df.groupby("region")["revenue"].median().sort_values(ascending=False)
    outlier_rule_text = (
        f"above ${upper_bound:,.2f} or below ${lower_bound:,.2f}"
        if lower_bound > 0
        else f"above ${upper_bound:,.2f}; the lower IQR threshold is below zero, so there are no realistic lower-end revenue outliers"
    )
    interpretation = f"""Distribution and Outlier Analysis Interpretation

The histogram with KDE shows that order revenue is right-skewed, with many medium-value orders and a smaller number of high-value orders. The calculated skewness is {skewness:.2f}, confirming that the distribution has a longer upper tail. The box plots show that regional revenue spreads are broadly similar, but {region_medians.index[0]} has the highest median order revenue (${region_medians.iloc[0]:,.2f}) while {region_medians.index[-1]} has the lowest median (${region_medians.iloc[-1]:,.2f}). Using the IQR rule, {len(outliers):,} outliers were detected {outlier_rule_text}; these are mostly premium, multi-unit orders rather than data errors, so they should be retained for business analysis but monitored separately.
"""
    (SUMMARY_DIR / "distribution_outlier_interpretation.txt").write_text(interpretation, encoding="utf-8")


def analyze_correlations_and_relationships(df: pd.DataFrame) -> None:
    numeric_columns = [
        "units_sold",
        "unit_price",
        "discount_rate",
        "marketing_spend",
        "shipping_days",
        "customer_satisfaction",
        "revenue",
        "profit",
        "profit_margin",
    ]
    corr = df[numeric_columns].corr(method="pearson")
    corr.to_csv(SUMMARY_DIR / "sales_correlation_matrix.csv")

    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        linewidths=0.5,
        cbar_kws={"label": "Pearson correlation"},
        ax=ax,
    )
    ax.set_title("Pearson Correlation Heatmap")
    save_current_figure(CORRELATION_DIR / "correlation_heatmap_masked.png")

    pair_columns = ["units_sold", "unit_price", "marketing_spend", "revenue", "profit"]
    pair_grid = sns.pairplot(
        df[pair_columns + ["region"]],
        vars=pair_columns,
        hue="region",
        diag_kind="kde",
        plot_kws={"alpha": 0.35, "s": 18},
        corner=True,
    )
    pair_grid.fig.suptitle("Pairwise Relationships for Key Sales Variables", y=1.02)
    pair_grid.savefig(CORRELATION_DIR / "key_variable_pairplot.png", bbox_inches="tight", dpi=180)
    plt.close(pair_grid.fig)

    pair_mask = np.tril(np.ones_like(corr, dtype=bool), k=-1)
    corr_pairs = corr.where(pair_mask).stack().dropna().sort_values()
    strongest_negative = corr_pairs.iloc[0]
    strongest_negative_pair = corr_pairs.index[0]
    strongest_positive = corr_pairs.iloc[-1]
    strongest_positive_pair = corr_pairs.index[-1]

    summary = f"""Correlation and Relationship Analysis Summary

Pearson correlations were computed for numeric variables and visualized with an annotated heatmap. The upper triangle is masked to avoid repeating the same information twice. A pairplot was also created for units sold, unit price, marketing spend, revenue, and profit so that linear relationships, clusters, and possible non-linear patterns can be inspected visually.

Strongest positive relationship:
- {strongest_positive_pair[0]} and {strongest_positive_pair[1]}: {strongest_positive:.2f}

Strongest negative relationship:
- {strongest_negative_pair[0]} and {strongest_negative_pair[1]}: {strongest_negative:.2f}

Business interpretation:
Revenue and profit move together strongly because higher-value orders usually create higher gross profit. Unit price and revenue also tend to be positively related, especially for categories with expensive items. Discount rate and profit margin show a negative relationship, which is expected because deeper discounts reduce retained margin. Customer satisfaction has a mild relationship with shipping days, suggesting faster delivery supports better customer experience.
"""
    (SUMMARY_DIR / "correlation_relationship_summary.txt").write_text(summary, encoding="utf-8")


def write_executive_summary(df: pd.DataFrame) -> None:
    summary = f"""Retail Sales Analytics Portfolio - Executive Summary

This submission presents a complete retail sales analytics project using one clean, reproducible analysis pipeline.

Dataset overview:
- Rows: {len(df):,}
- Date range: {df["order_date"].min().date()} to {df["order_date"].max().date()}
- Categories: {", ".join(sorted(df["category"].unique()))}
- Regions: {", ".join(sorted(df["region"].unique()))}
- Total revenue: ${df["revenue"].sum():,.2f}
- Total profit: ${df["profit"].sum():,.2f}

Files generated:
- Sales trend and category charts for time series, monthly/quarterly aggregation, category comparison, and share analysis.
- Distribution charts, KDEs, box plots, an outlier table, and a written distribution interpretation.
- Correlation matrix, masked annotated heatmap, pairplot, and relationship summary.

All charts are exported as PNG files under outputs/charts, and all written outputs are saved under outputs/summaries.
"""
    (SUMMARY_DIR / "executive_summary.txt").write_text(summary, encoding="utf-8")


def main() -> None:
    prepare_directories()
    configure_plots()

    data_path = DATA_DIR / "retail_sales.csv"
    df = generate_sales_data(data_path)
    df["order_date"] = pd.to_datetime(df["order_date"])

    analyze_sales_trends_and_categories(df)
    analyze_distributions_and_outliers(df)
    analyze_correlations_and_relationships(df)
    write_executive_summary(df)

    print("Retail sales analytics project complete.")
    print(f"Dataset: {data_path.relative_to(ROOT)}")
    print(f"Charts: {CHART_DIR.relative_to(ROOT)}")
    print(f"Summaries: {SUMMARY_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
