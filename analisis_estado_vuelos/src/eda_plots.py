import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


name_mapping = {
    'FO': 'Flybondi',
    'WJ': 'Jetsmart'
}

# colors that represent the company
fixed_colors = {
    'Jetsmart': '#1b365d', # Azul
    'Flybondi': '#fdbe15'  # Amarillo
}

def show_custom_pie(df: pd.DataFrame, column_name: str, labels: list = None, title: str = None, colors: list = None ) -> None:
    """
    Renders a pie chart for a categorical column.

    Parameters
    ----------
    df          : Input DataFrame.
    column_name : Column to count and plot.
    labels      : Optional list of display labels. Uses index values if None.
    title       : Chart title. Auto-generated if None.
    colors      : List of colors. Uses Pastel1 colormap if None.
    """
    data = df[column_name].value_counts()
    n_categories = len(data)

    # Label handling
    if labels is None:
        labels = [f"{idx} ({val})" for idx, val in zip(data.index, data.values)]
    else:
        labels = [f"{label} ({val})" for label, val in zip(labels, data.values)]

    # Color and explode
    if colors is None:
        colors = plt.cm.Pastel1.colors
    explode = [0.1 if i == 1 else 0 for i in range(n_categories)]

    plt.figure(figsize=(8, 6))
    plt.pie(data, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors[:n_categories],
            explode=explode if n_categories > 1 else None, shadow=True)
    plt.title(title if title else f"Distribution of {column_name}", fontsize=14)
    plt.axis("equal")
    plt.show()


# ---------------------------------------------------------------------------
# Temporal delay impact
# ---------------------------------------------------------------------------

def plot_temporal_impact(df: pd.DataFrame, category: str = None, unit: str = "days", show_labels: bool = False, 
                         name_mapping: dict = None, fixed_colors: dict = None) -> None:
    """
    Compares total delay impact per month and company.

    Parameters
    ----------
    df           : Input DataFrame. Must contain 'mes', 'empresa',
                   'minutos_netos_demora'.
    category     : Optional column used for hue grouping.
    unit         : One of 'minutes', 'hours', 'days'.
    show_labels  : If True, renders data labels on top of each bar.
    name_mapping : Dict to remap company/category display names.
    fixed_colors : Dict of fixed colors per category value.
    """
    unit_config = {
        "minutes": {"divisor": 1,    "label": "Total Minutes",     "fmt": "%.0f"},
        "hours":   {"divisor": 60,   "label": "Total Hours",       "fmt": "%.1f"},
        "days":    {"divisor": 1440, "label": "Days of Delay",     "fmt": "%.2f"},
    }

    if unit not in unit_config:
        raise ValueError(f"unit must be one of: {list(unit_config.keys())}")

    divisor  = unit_config[unit]["divisor"]
    label_y  = unit_config[unit]["label"]
    fmt      = unit_config[unit]["fmt"]

    df_plot = df.copy()
    if category and name_mapping:
        df_plot[category] = df_plot[category].map(name_mapping).fillna(df_plot[category])

    df_grouped = (df_plot.groupby(["mes", "empresa"])["minutos_netos_demora"].sum().reset_index())
    df_grouped["converted_value"] = df_grouped["minutos_netos_demora"] / divisor

    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")

    ax = sns.barplot(data=df_grouped, x="mes", y="converted_value", hue="empresa", 
                     palette=fixed_colors if category else None)

    if show_labels:
        for container in ax.containers:
            ax.bar_label(container, fmt=fmt, padding=3, fontsize=9)

    plt.title(f"Monthly Comparison: {label_y}", fontsize=15, pad=20)
    plt.ylabel(label_y, fontsize=12)
    plt.xlabel("Month", fontsize=12)
    plt.legend(title="Company", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.margins(y=0.15)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Cancellations by month (line — single month)
# ---------------------------------------------------------------------------

def plot_cancellations_month(df: pd.DataFrame, month: int) -> None:
    """
    Line chart of daily cancellations for a single month.

    Parameters
    ----------
    df    : DataFrame with 'fecha' (datetime) and 'is_cancelled' columns.
    month : Integer month number (1–12).
    """
    df_month = df[df["fecha"].dt.month == month].copy()

    if df_month.empty:
        print(f"No data available for month {month}.")
        return

    data_plot = df_month.groupby("fecha")["is_cancelled"].sum().reset_index()

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=data_plot, x="fecha", y="is_cancelled", marker="o", color="darkred")
    plt.title(f"Cancellations — Month {month}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Cancellations overview (annual or filtered by month)
# ---------------------------------------------------------------------------

def plot_cancellations(df: pd.DataFrame, color: str = "steelblue", by_company: bool = False, month: int = None,
    fixed_colors: dict = None) -> None:

    df_plot = df.copy()
    df_plot["fecha"] = pd.to_datetime(df_plot["fecha"])

    if by_company:
        df_plot["empresa"] = df_plot["empresa"].map(name_mapping).fillna(df_plot["empresa"])

    # Optional month filter
    if month:
        df_plot = df_plot[df_plot["fecha"].dt.month == month]
        month_name = df_plot["fecha"].dt.month_name().iloc[0] if not df_plot.empty else ""
        title_extra = f" — Month: {month_name}"
    else:
        title_extra = " — Annual"

    group_cols = ["fecha", "empresa"] if by_company else ["fecha"]
    data_grouped = df_plot.groupby(group_cols)["is_cancelled"].sum().reset_index()

    plt.figure(figsize=(14, 6))
    sns.set_style("whitegrid")

    if by_company:
        sns.lineplot(
            data=data_grouped, x="fecha", y="is_cancelled",
            hue="empresa", palette=fixed_colors, marker="o"
        )
        plt.title(f"Cancellations by Company{title_extra}")
    else:
        sns.lineplot(
            data=data_grouped, x="fecha", y="is_cancelled",
            color=color, marker="o"
        )
        plt.title(f"Total Cancellations Evolution{title_extra}")

    plt.ylabel("Number of Cancellations")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_cancellations_heatmap(df: pd.DataFrame, ordered_months: list = None, ordered_days: list = None) -> None:
    """
    Heatmap of cancellation rate by month and day of week.

    Parameters
    ----------
    df             : DataFrame with 'fecha' and 'is_cancelled'.
    ordered_months : List of month names defining row order.
    ordered_days   : List of day names defining column order.
    """
    df_heat = df.copy()
    df_heat["Month"]      = df_heat["fecha"].dt.month_name()
    df_heat["Day_of_Week"] = df_heat["fecha"].dt.day_name()

    pivot = df_heat.pivot_table(values="is_cancelled", index="Month", columns="Day_of_Week", aggfunc="mean")

    if ordered_months:
        pivot = pivot.reindex(index=ordered_months)
    if ordered_days:
        pivot = pivot.reindex(columns=ordered_days)

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, cmap="YlOrRd", fmt=".2f", linewidths=0.5)
    plt.title("Heatmap: Cancellation Rate by Month and Day", fontsize=15)
    plt.xlabel("Day of the Week")
    plt.ylabel("Month")
    plt.show()