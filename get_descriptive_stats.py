import os
import csv
import sys

# Define target paths
sales_data_path = os.path.join("datasets", "sales_data.csv")

def run_pure_python_stats(filepath):
    print("=" * 60)
    print("   DESCRIPTIVE STATISTICS (PURE PYTHON FALLBACK MODE)")
    print("=" * 60)
    
    if not os.path.exists(filepath):
        print(f"Error: Dataset not found at '{filepath}'. Please run 'generate_sales_data.py' first.")
        return

    # Columns to compute numeric stats for
    numeric_cols = [
        "Units Sold", "Unit Price", "Gross Sales", "Discount Amount",
        "Net Sales", "GST Amount", "Total Bill", "Customer Count",
        "Average Bill Size", "Peak Hour Sales %"
    ]
    
    # Storage for statistics
    data = {col: [] for col in numeric_cols}
    outlets = {}
    products = {}
    payment_modes = {}
    weather_modes = {}
    row_count = 0
    unique_dates = set()

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            row_count += 1
            unique_dates.add(r["Transaction Date"])
            
            # Numeric values parsing
            for col in numeric_cols:
                try:
                    data[col].append(float(r[col]))
                except ValueError:
                    pass
            
            # Categorical counters
            out_name = r["Outlet Name"]
            prod_name = r["Product Name"]
            pay_mode = r["Payment Mode"]
            weather = r["Weather"]
            total_bill = float(r["Total Bill"])
            units_sold = int(r["Units Sold"])
            
            # Outlet breakdown
            if out_name not in outlets:
                outlets[out_name] = {"Units Sold": 0, "Revenue": 0.0, "Count": 0}
            outlets[out_name]["Units Sold"] += units_sold
            outlets[out_name]["Revenue"] += total_bill
            outlets[out_name]["Count"] += 1

            # Product breakdown
            if prod_name not in products:
                products[prod_name] = {"Units Sold": 0, "Revenue": 0.0, "Count": 0}
            products[prod_name]["Units Sold"] += units_sold
            products[prod_name]["Revenue"] += total_bill
            products[prod_name]["Count"] += 1

            # Payment breakdown
            if pay_mode not in payment_modes:
                payment_modes[pay_mode] = {"Revenue": 0.0, "Count": 0}
            payment_modes[pay_mode]["Revenue"] += total_bill
            payment_modes[pay_mode]["Count"] += 1

            # Weather breakdown
            if weather not in weather_modes:
                weather_modes[weather] = {"Units Sold": 0, "Count": 0}
            weather_modes[weather]["Units Sold"] += units_sold
            weather_modes[weather]["Count"] += 1

    sorted_dates = sorted(list(unique_dates))
    print(f"Dataset File: {filepath}")
    print(f"Total Record Count: {row_count}")
    print(f"Unique Dates: {len(sorted_dates)} ({sorted_dates[0]} to {sorted_dates[-1]})")
    print("-" * 60)

    # 1. Numeric Summaries
    print(f"{'Numeric Column':<22} | {'Mean':<12} | {'Min':<10} | {'Max':<10} | {'Std Dev':<10}")
    print("-" * 60)
    for col in numeric_cols:
        vals = data[col]
        if not vals:
            continue
        n = len(vals)
        mean_val = sum(vals) / n
        min_val = min(vals)
        max_val = max(vals)
        
        # Variance and Standard Deviation
        variance = sum((x - mean_val) ** 2 for x in vals) / max(1, n - 1)
        std_val = variance ** 0.5
        
        print(f"{col:<22} | {mean_val:<12.2f} | {min_val:<10.2f} | {max_val:<10.2f} | {std_val:<10.2f}")
    print("-" * 60)

    # 2. Outlet breakdown
    print("\nOUTLET PERFORMANCE BREAKDOWN:")
    print(f"{'Outlet Name':<18} | {'Total Units':<12} | {'Total Revenue (INR)':<20} | {'Avg Order Size (INR)':<20}")
    print("-" * 75)
    for name, stats in sorted(outlets.items(), key=lambda x: x[1]["Revenue"], reverse=True):
        avg_order = stats["Revenue"] / max(1, stats["Count"])
        print(f"{name:<18} | {stats['Units Sold']:<12} | {stats['Revenue']:<20.2f} | {avg_order:<20.2f}")

    # 3. Product breakdown
    print("\nPRODUCT PERFORMANCE BREAKDOWN:")
    print(f"{'Product Name':<18} | {'Total Units':<12} | {'Total Revenue (INR)':<20} | {'Sales Share %':<12}")
    print("-" * 70)
    total_revenue = sum(stats["Revenue"] for stats in products.values())
    for name, stats in sorted(products.items(), key=lambda x: x[1]["Revenue"], reverse=True):
        share_pct = (stats["Revenue"] / total_revenue) * 100 if total_revenue > 0 else 0
        print(f"{name:<18} | {stats['Units Sold']:<12} | {stats['Revenue']:<20.2f} | {share_pct:<12.2f}")

    # 4. Payment Modes breakdown
    print("\nPAYMENT MODE DISTRIBUTION:")
    print(f"{'Payment Mode':<15} | {'Transaction Count':<18} | {'Total Volume (INR)':<20} | {'Revenue Share %':<15}")
    print("-" * 75)
    for mode, stats in sorted(payment_modes.items(), key=lambda x: x[1]["Revenue"], reverse=True):
        share_pct = (stats["Revenue"] / total_revenue) * 100 if total_revenue > 0 else 0
        print(f"{mode:<15} | {stats['Count']:<18} | {stats['Revenue']:<20.2f} | {share_pct:<15.2f}")

    # 5. Weather breakdown
    print("\nWEATHER IMPACT BREAKDOWN:")
    print(f"{'Weather':<12} | {'Transaction Count':<18} | {'Avg Units Sold/Row':<20}")
    print("-" * 55)
    for weather, stats in sorted(weather_modes.items(), key=lambda x: x[1]["Count"], reverse=True):
        avg_units = stats["Units Sold"] / max(1, stats["Count"])
        print(f"{weather:<12} | {stats['Count']:<18} | {avg_units:<20.2f}")
    print("=" * 60)


def run_pandas_stats(filepath):
    import pandas as pd
    
    print("=" * 70)
    print("   DESCRIPTIVE STATISTICS (PANDAS PRO MODE)")
    print("=" * 70)
    
    if not os.path.exists(filepath):
        print(f"Error: Dataset not found at '{filepath}'. Please run 'generate_sales_data.py' first.")
        return

    # Load data
    df = pd.read_csv(filepath)
    
    # Dataset General info
    print(f"Dataset File: {filepath}")
    print(f"Total Rows (Transactions): {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Date Range: {df['Transaction Date'].min()} to {df['Transaction Date'].max()}")
    print("-" * 70)
    
    # Numeric column description
    numeric_cols = [
        "Units Sold", "Unit Price", "Gross Sales", "Discount Amount",
        "Net Sales", "GST Amount", "Total Bill", "Customer Count",
        "Average Bill Size", "Peak Hour Sales %"
    ]
    
    print("\nNUMERIC COLUMNS SUMMARY STATS:")
    numeric_desc = df[numeric_cols].describe().T
    # Format description table nicely
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    print(numeric_desc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])
    print("-" * 70)
    
    # Categorical breakdown: Outlet Performance
    print("\nREVENUE & FOOTFALL BY OUTLET (SORTED BY TOTAL REVENUE):")
    outlet_summary = df.groupby("Outlet Name").agg(
        Total_Units_Sold=("Units Sold", "sum"),
        Total_Revenue_INR=("Total Bill", "sum"),
        Total_Customers=("Customer Count", "sum"),
        Average_Bill_Size=("Total Bill", lambda x: x.sum() / df.loc[x.index, "Customer Count"].sum()),
        Avg_Peak_Hour_Sales_Pct=("Peak Hour Sales %", "mean")
    ).sort_values(by="Total_Revenue_INR", ascending=False)
    print(outlet_summary)
    print("-" * 70)

    # Categorical breakdown: Product performance
    print("\nSALES SUMMARY BY PRODUCT:")
    total_rev = df["Total Bill"].sum()
    product_summary = df.groupby("Product Name").agg(
        Total_Units_Sold=("Units Sold", "sum"),
        Total_Revenue_INR=("Total Bill", "sum"),
        Average_Unit_Price=("Unit Price", "mean"),
        Revenue_Share_Pct=("Total Bill", lambda x: (x.sum() / total_rev) * 100)
    ).sort_values(by="Total_Revenue_INR", ascending=False)
    print(product_summary)
    print("-" * 70)

    # Categorical breakdown: Payment Modes
    print("\nPAYMENT MODE DISTRIBUTION:")
    payment_summary = df.groupby("Payment Mode").agg(
        Transaction_Count=("Total Bill", "count"),
        Total_Revenue_INR=("Total Bill", "sum"),
        Revenue_Share_Pct=("Total Bill", lambda x: (x.sum() / total_rev) * 100)
    ).sort_values(by="Total_Revenue_INR", ascending=False)
    print(payment_summary)
    print("-" * 70)

    # Categorical breakdown: Weather Impact
    print("\nWEATHER IMPACT ON FOOTFALL AND SALES:")
    weather_summary = df.groupby("Weather").agg(
        Transaction_Count=("Total Bill", "count"),
        Average_Units_Sold=("Units Sold", "mean"),
        Average_Customer_Count=("Customer Count", "mean")
    ).sort_values(by="Average_Units_Sold", ascending=False)
    print(weather_summary)
    print("=" * 70)

if __name__ == "__main__":
    # Check if pandas is available
    try:
        import pandas
        run_pandas_stats(sales_data_path)
    except ImportError:
        print("Pandas library not found. Running statistics using Python standard libraries...")
        run_pure_python_stats(sales_data_path)
