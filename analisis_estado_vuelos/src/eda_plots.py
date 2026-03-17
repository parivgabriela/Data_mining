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

ordered_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

color_g = "#fc7753"
paleta = ["#fc7753", "#66d7d1", "#C45BAA"]

labels_cancelado = ["No Cancelado", "Cancelado"]

def plot_frequencies(df: pd.DataFrame, freq_column: str, category: str = None, title: str = None, color: str = "green",
                     sort_by_index: bool = False, show_mean: bool = False, fixed_colors: dict = None) -> None:
    """
    Generates a bar chart with an optional mean frequency line.

    Parameters
    ----------
    df           : Input DataFrame.
    freq_column  : Column to count on the X axis.
    category     : Optional column for hue grouping.
    title        : Chart title. Auto-generated if None.
    color        : Bar color when no category is used.
    sort_by_index: If True, sorts X axis by value instead of frequency.
    show_mean    : If True, draws a horizontal mean line.
    fixed_colors : Dict of fixed colors per category value.
    """
    df_plot = df.copy()

    if category:
        df_plot["empresa"] = df_plot["empresa"].map(name_mapping).fillna(df_plot["empresa"])

    # 1. X-axis order
    order = (
        sorted(df_plot[freq_column].unique()) if sort_by_index else df_plot[freq_column].value_counts().index.astype(str)
    )

    # 2. Build chart
    plt.figure(figsize=(10, 6))

    if category:
        ax = sns.countplot(data=df_plot, x=freq_column, hue=category, order=order, palette=fixed_colors)
        plt.legend(title=category, bbox_to_anchor=(1.05, 1), loc="upper left")
    else:
        ax = sns.countplot(data=df_plot, x=freq_column, order=order, color=color)

    # 3. Mean line
    if show_mean:
        counts = df_plot[freq_column].value_counts()
        mean_val = counts.mean()
        plt.axhline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.1f}")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # 4. Style
    auto_title = f"Distribution of {freq_column}" + (f" by {category}" if category else "")
    plt.title(title or auto_title, fontsize=14)
    plt.xlabel(freq_column, fontsize=12)
    plt.ylabel("Record Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_evolution(
    df: pd.DataFrame, x: str, y: str, category: str = None, estimator: str = "mean", title: str = None,
    fixed_colors: dict = None) -> None:
    """
    Plots the evolution of a metric over time or an ordered axis.

    Parameters
    ----------
    df          : Input DataFrame.
    x           : Column for the X axis.
    y           : Column for the Y axis (metric).
    category    : Optional column for hue grouping.
    estimator   : Aggregation function ('mean', 'sum', 'median').
    title       : Chart title. Auto-generated if None.
    fixed_colors: Dict of fixed colors per category value.
    """
    df_plot = df.copy()

    if category:
        df_plot[category] = df_plot[category].map(name_mapping).fillna(df_plot[category])

    label_y = y.replace("_", " ").title()
    label_x = x.replace("_", " ").title()

    plt.figure(figsize=(12, 5))
    sns.set_theme(style="whitegrid")

    sns.lineplot(
        data=df_plot, x=x, y=y, hue=category, estimator=estimator, marker="o", linewidth=2.5,
        errorbar=None, palette=fixed_colors if category else None
    )

    plt.title(title or f"{label_y} by {label_x}", fontsize=15, pad=20)
    plt.xlabel(label_x, fontsize=12)
    plt.ylabel(f"{estimator.capitalize()} of {label_y}", fontsize=12)

    if category:
        plt.legend(title=category.replace("_", " ").title(), bbox_to_anchor=(1.05, 1), loc="upper left")

    if df_plot[x].dtype in ["int64", "int32"]:
        plt.xticks(sorted(df_plot[x].unique()))

    plt.tight_layout()
    plt.show()

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


def plot_temporal_impact(df: pd.DataFrame, category: str = None, unit: str = "days", show_labels: bool = False,
                         fixed_colors: dict = None) -> None:
    """
    Compares total delay impact per month and company.

    Parameters
    ----------
    df           : Input DataFrame. Must contain 'mes', 'empresa',
                   'minutos_netos_demora'.
    category     : Optional column used for hue grouping.
    unit         : One of 'minutes', 'hours', 'days'.
    show_labels  : If True, renders data labels on top of each bar.
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
    
    target_col = category if category else "empresa"
    
    if target_col:
        df_plot[target_col] = df_plot[target_col].map(name_mapping).fillna(df_plot[target_col])

    df_grouped = (df_plot.groupby(["mes", target_col])["minutos_netos_demora"].sum().reset_index())
    df_grouped["converted_value"] = df_grouped["minutos_netos_demora"] / divisor

    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")

    ax = sns.barplot(
        data=df_grouped, 
        x="mes", 
        y="converted_value", 
        hue=target_col,
        palette=fixed_colors if fixed_colors else None
    )

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

