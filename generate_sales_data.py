import datetime
import random
import csv
import os
import math

os.makedirs("datasets", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Set random seed for reproducibility
random.seed(42)

# Configurations
outlets = [
    {"id": "OUT001", "name": "Indiranagar", "area": "East", "manager": "Aarav Sharma", "base_units": 100, "prices": {"PRD001": 220, "PRD002": 160, "PRD003": 110}},
    {"id": "OUT002", "name": "Koramangala", "area": "South", "manager": "Ananya Iyer", "base_units": 85, "prices": {"PRD001": 215, "PRD002": 155, "PRD003": 105}},
    {"id": "OUT003", "name": "Whitefield", "area": "East", "manager": "Rahul Nair", "base_units": 75, "prices": {"PRD001": 220, "PRD002": 160, "PRD003": 110}},
    {"id": "OUT004", "name": "Electronic City", "area": "South", "manager": "Priyanka Sen", "base_units": 70, "prices": {"PRD001": 200, "PRD002": 145, "PRD003": 95}},
    {"id": "OUT005", "name": "MG Road", "area": "Central", "manager": "Vikram Malhotra", "base_units": 80, "prices": {"PRD001": 225, "PRD002": 165, "PRD003": 115}},
    {"id": "OUT006", "name": "Jayanagar", "area": "South", "manager": "Siddharth Rao", "base_units": 72, "prices": {"PRD001": 210, "PRD002": 150, "PRD003": 100}},
    {"id": "OUT007", "name": "Malleshwaram", "area": "West", "manager": "Meera Krishnan", "base_units": 65, "prices": {"PRD001": 190, "PRD002": 140, "PRD003": 90}},
    {"id": "OUT008", "name": "HSR Layout", "area": "South", "manager": "Aditya Verma", "base_units": 72, "prices": {"PRD001": 205, "PRD002": 150, "PRD003": 100}},
    {"id": "OUT009", "name": "Rajajinagar", "area": "West", "manager": "Sneha Hegde", "base_units": 65, "prices": {"PRD001": 195, "PRD002": 140, "PRD003": 90}},
    {"id": "OUT010", "name": "Yelahanka", "area": "North", "manager": "Rohan Das", "base_units": 55, "prices": {"PRD001": 180, "PRD002": 130, "PRD003": 85}}
]

products = [
    {"id": "PRD001", "name": "Chicken Burger", "category": "Burgers", "multiplier": 1.10},
    {"id": "PRD002", "name": "Veg Burger", "category": "Burgers", "multiplier": 1.00},
    {"id": "PRD003", "name": "French Fries", "category": "Sides", "multiplier": 0.85}
]

payment_modes = ["UPI", "Credit Card", "Debit Card", "Cash", "Wallet"]
payment_weights = [0.45, 0.25, 0.10, 0.15, 0.05]

# Calendar functions
def get_date_details(date_obj):
    day_name = date_obj.strftime("%A")
    month_name = date_obj.strftime("%B")
    
    # Financial Year & Quarters (Indian Calendar)
    # FY starts on April 1.
    # Q1: Apr-Jun, Q2: Jul-Sep, Q3: Oct-Dec, Q4: Jan-Mar
    year = date_obj.year
    month = date_obj.month
    
    if month >= 4:
        fy = f"FY {year}-{str(year+1)[2:]}"
        if month in [4, 5, 6]:
            q = f"Q1 {fy}"
        elif month in [7, 8, 9]:
            q = f"Q2 {fy}"
        elif month in [10, 11, 12]:
            q = f"Q3 {fy}"
        else:
            q = f"Q4 {fy}"
    else:
        fy = f"FY {year-1}-{str(year)[2:]}"
        if month in [1, 2, 3]:
            q = f"Q4 {fy}"
        elif month in [4, 5, 6]:
            q = f"Q1 {fy}"
        elif month in [7, 8, 9]:
            q = f"Q2 {fy}"
        else:
            q = f"Q3 {fy}"
            
    return day_name, month_name, q, fy

# Date list generation: Aug 1, 2025 to Jul 31, 2026
start_date = datetime.date(2025, 8, 1)
end_date = datetime.date(2026, 7, 31)

date_list = []
curr_date = start_date
while curr_date <= end_date:
    date_list.append(curr_date)
    curr_date += datetime.timedelta(days=1)

print(f"Generated {len(date_list)} dates from {start_date} to {end_date}.")

records = []

for date in date_list:
    day_of_week, month, quarter, fin_year = get_date_details(date)
    is_weekend = day_of_week in ["Saturday", "Sunday"]
    is_friday = day_of_week == "Friday"
    
    # Holiday & Festival spikes
    is_holiday = "No"
    special_event = "None"
    holiday_spike = 1.0
    
    # Independence Day: 15 Aug 2025
    if date == datetime.date(2025, 8, 15):
        is_holiday = "Yes"
        special_event = "Independence Day"
        holiday_spike = 1.25
    # Diwali: 20 Oct 2025
    elif date == datetime.date(2025, 10, 20):
        is_holiday = "Yes"
        special_event = "Diwali"
        holiday_spike = 1.45
    # Christmas: 25 Dec 2025
    elif date == datetime.date(2025, 12, 25):
        is_holiday = "Yes"
        special_event = "Christmas"
        holiday_spike = 1.40
    # New Year's Eve: 31 Dec 2025
    elif date == datetime.date(2025, 12, 31):
        is_holiday = "Yes"
        special_event = "New Year's Eve"
        holiday_spike = 1.50
    # New Year's Day: 1 Jan 2026
    elif date == datetime.date(2026, 1, 1):
        is_holiday = "Yes"
        special_event = "New Year's Day"
        holiday_spike = 1.30
    # Republic Day: 26 Jan 2026
    elif date == datetime.date(2026, 1, 26):
        is_holiday = "Yes"
        special_event = "Republic Day"
        holiday_spike = 1.25

    # Base monthly seasonal factor
    month_val = date.month
    monthly_factor = 1.0
    if month_val == 8: monthly_factor = 0.95
    elif month_val == 9: monthly_factor = 0.90
    elif month_val == 10: monthly_factor = 1.05
    elif month_val == 11: monthly_factor = 1.00
    elif month_val == 12: monthly_factor = 1.15
    elif month_val == 1: monthly_factor = 1.05
    elif month_val == 2: monthly_factor = 0.95
    elif month_val == 3: monthly_factor = 0.95
    elif month_val == 4: monthly_factor = 1.00
    elif month_val == 5: monthly_factor = 1.10
    elif month_val == 6: monthly_factor = 0.95
    elif month_val == 7: monthly_factor = 0.95

    # Base Weather logic based on month
    if month_val in [8, 9, 6, 7]: # Monsoon
        weather = random.choices(["Rainy", "Overcast", "Sunny"], weights=[0.40, 0.40, 0.20])[0]
    elif month_val in [10, 11]: # Post-monsoon
        weather = random.choices(["Sunny", "Overcast", "Rainy"], weights=[0.50, 0.30, 0.20])[0]
    elif month_val in [12, 1, 2, 3]: # Winter/Dry
        weather = random.choices(["Sunny", "Overcast", "Rainy"], weights=[0.80, 0.15, 0.05])[0]
    else: # Summer
        weather = random.choices(["Sunny", "Overcast", "Rainy"], weights=[0.60, 0.25, 0.15])[0]

    weather_factor = 1.0
    if weather == "Rainy":
        weather_factor = 0.88 # 12% drop for standard rainy day

    # Generate records for each outlet
    for outlet in outlets:
        # Determine store-level event for the day (if not a major festival)
        discount_pct = 0.0
        remarks = "Normal Operations"
        stock_avail = "Available"
        event_spike = 1.0
        shortage_product_id = None
        current_special_event = special_event
        current_weather = weather
        current_weather_factor = weather_factor
        
        if current_special_event == "None":
            # Roll for random daily events
            roll = random.random()
            if roll < 0.05:
                # 5% discount day
                discount_pct = 0.05
                remarks = "5% Discount Day"
            elif roll < 0.10:
                # Combo offer day
                discount_pct = 0.10
                remarks = "Combo Offer Applied"
            elif roll < 0.13:
                # Stock shortage day
                stock_avail = "Shortage"
                shortage_product_id = random.choice(["PRD001", "PRD002", "PRD003"])
                remarks = "Stock Shortage - Lower Sales"
            elif roll < 0.145:
                # Power outage
                event_spike = 0.90
                remarks = "Brief Power Outage - Slow Operations"
            elif roll < 0.175 and current_weather == "Rainy":
                # Heavy rainfall
                event_spike = 0.82
                remarks = "Heavy Rainfall - Lower Footfall"
            elif roll < 0.195:
                # Local event
                current_special_event = "Local Event"
                event_spike = 1.20
                remarks = "Local Event - High Footfall"
            elif roll < 0.205:
                # Marathon
                current_special_event = "Marathon"
                event_spike = 1.10
                remarks = "Marathon Day - Early Morning Peak"
            elif roll < 0.225:
                # College festival
                current_special_event = "College Festival"
                discount_pct = 0.05
                event_spike = 1.15
                remarks = "College Festival - Student Discounts"
        else:
            remarks = "Festival Demand - High Footfall"

        # Peak Hour Sales % Calculation
        if outlet["name"] == "Koramangala":
            peak_sales_pct = round(random.uniform(62.0, 75.0), 2) # Dinner-heavy
        elif outlet["name"] == "Whitefield":
            peak_sales_pct = round(random.uniform(55.0, 68.0), 2) # Lunch-heavy
        elif outlet["name"] == "Electronic City":
            if is_weekend:
                peak_sales_pct = round(random.uniform(40.0, 50.0), 2)
            else:
                peak_sales_pct = round(random.uniform(52.0, 62.0), 2)
        elif outlet["name"] == "MG Road":
            if is_weekend:
                peak_sales_pct = round(random.uniform(58.0, 70.0), 2)
            else:
                peak_sales_pct = round(random.uniform(42.0, 52.0), 2)
        elif outlet["name"] == "Indiranagar":
            peak_sales_pct = round(random.uniform(50.0, 65.0), 2)
        else:
            peak_sales_pct = round(random.uniform(45.0, 55.0), 2)

        # Day-of-week multiplier by store type
        if outlet["name"] == "Electronic City":
            # Weekday heavy
            day_factor = 1.25 if not is_weekend else 0.60
        elif outlet["name"] == "MG Road":
            # Weekend heavy
            if is_weekend:
                day_factor = 1.45
            elif is_friday:
                day_factor = 1.20
            else:
                day_factor = 0.80
        elif outlet["name"] == "Indiranagar":
            # Consistently high, weekend peak
            if is_weekend:
                day_factor = 1.35
            elif is_friday:
                day_factor = 1.20
            else:
                day_factor = 0.95
        else:
            # Standard outlets
            if is_weekend:
                day_factor = 1.30
            elif is_friday:
                day_factor = 1.15
            else:
                day_factor = 0.90

        # Shift selection
        if current_special_event != "None" and current_special_event != "Marathon":
            shift = "Full Day"
        else:
            if is_weekend:
                shift = random.choices(["Full Day", "Evening", "Morning"], weights=[0.80, 0.10, 0.10])[0]
            elif is_friday:
                shift = random.choices(["Evening", "Full Day", "Morning"], weights=[0.70, 0.20, 0.10])[0]
            else:
                shift = random.choices(["Morning", "Evening", "Full Day"], weights=[0.50, 0.40, 0.10])[0]

        # Generate each of the 3 products
        for prod in products:
            prod_id = prod["id"]
            prod_name = prod["name"]
            category = prod["category"]
            unit_price = outlet["prices"][prod_id]

            # Product specific availability and remarks
            row_stock = "Available"
            row_remarks = remarks
            row_discount_pct = discount_pct
            
            # Stock Shortage applies only to the selected product
            product_shortage_factor = 1.0
            if stock_avail == "Shortage":
                if prod_id == shortage_product_id:
                    row_stock = "Shortage"
                    product_shortage_factor = 0.65 # 35% drop
                    row_remarks = f"Stock Shortage of {prod_name}"
                else:
                    row_remarks = f"Normal Operations (Shortage of {next(p['name'] for p in products if p['id'] == shortage_product_id)})"

            # Base unit sales calculation
            base_units = outlet["base_units"]
            prod_mult = prod["multiplier"]
            
            # Combine factors with noise
            noise = random.uniform(0.90, 1.10)
            
            units_sold_float = (base_units * prod_mult * day_factor * monthly_factor * 
                                current_weather_factor * holiday_spike * event_spike * 
                                product_shortage_factor * noise)
            
            units_sold = max(10, round(units_sold_float)) # Ensure minimum sales is 10 units
            
            # Calculate values
            gross_sales = units_sold * unit_price
            
            # Calculate discount
            discount_amount = round(gross_sales * row_discount_pct, 2)
            net_sales = gross_sales - discount_amount
            
            # GST % is 5%
            gst_pct = 5
            gst_amount = round(net_sales * 0.05, 2)
            total_bill = round(net_sales + gst_amount, 2)
            
            # Customer count logic (average of 1.2 to 1.5 units per customer)
            avg_units_per_cust = random.uniform(1.2, 1.5)
            customer_count = max(1, round(units_sold / avg_units_per_cust))
            # Safety checks
            if customer_count > units_sold:
                customer_count = units_sold
                
            average_bill_size = round(total_bill / customer_count, 2)
            
            payment_mode = random.choices(payment_modes, weights=payment_weights)[0]
            
            records.append({
                "Transaction Date": date.strftime("%Y-%m-%d"),
                "Day of Week": day_of_week,
                "Month": month,
                "Quarter": quarter,
                "Financial Year": fin_year,
                "Outlet ID": outlet["id"],
                "Outlet Name": outlet["name"],
                "Area": outlet["area"],
                "Product ID": prod_id,
                "Product Name": prod_name,
                "Category": category,
                "Units Sold": units_sold,
                "Unit Price": unit_price,
                "Gross Sales": gross_sales,
                "Discount %": row_discount_pct,
                "Discount Amount": discount_amount,
                "Net Sales": net_sales,
                "GST %": gst_pct,
                "GST Amount": gst_amount,
                "Total Bill": total_bill,
                "Payment Mode": payment_mode,
                "Customer Count": customer_count,
                "Average Bill Size": average_bill_size,
                "Peak Hour Sales %": peak_sales_pct,
                "Weather": current_weather,
                "Special Event": current_special_event,
                "Holiday": is_holiday,
                "Stock Availability": row_stock,
                "Employee Shift": shift,
                "Manager Name": outlet["manager"],
                "Remarks": row_remarks
            })

# Save the full transaction dataset
sales_data_path = "datasets/sales_data.csv"
fieldnames = [
    "Transaction Date", "Day of Week", "Month", "Quarter", "Financial Year",
    "Outlet ID", "Outlet Name", "Area", "Product ID", "Product Name", "Category",
    "Units Sold", "Unit Price", "Gross Sales", "Discount %", "Discount Amount",
    "Net Sales", "GST %", "GST Amount", "Total Bill", "Payment Mode", "Customer Count",
    "Average Bill Size", "Peak Hour Sales %", "Weather", "Special Event", "Holiday",
    "Stock Availability", "Employee Shift", "Manager Name", "Remarks"
]

with open(sales_data_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Exported sales_data.csv with {len(records)} records successfully.")

# Validate calculations in python before proceeding
print("Running validations...")
errors = 0
for i, r in enumerate(records):
    # Gross
    g = r["Units Sold"] * r["Unit Price"]
    if abs(g - r["Gross Sales"]) > 0.01:
        print(f"Row {i} Gross mismatch: {g} vs {r['Gross Sales']}")
        errors += 1
    # Discount
    da = round(r["Gross Sales"] * r["Discount %"], 2)
    if abs(da - r["Discount Amount"]) > 0.01:
        print(f"Row {i} Discount mismatch: {da} vs {r['Discount Amount']}")
        errors += 1
    # Net Sales
    ns = r["Gross Sales"] - r["Discount Amount"]
    if abs(ns - r["Net Sales"]) > 0.01:
        print(f"Row {i} Net mismatch: {ns} vs {r['Net Sales']}")
        errors += 1
    # GST Amount
    ga = round(r["Net Sales"] * 0.05, 2)
    if abs(ga - r["GST Amount"]) > 0.01:
        print(f"Row {i} GST mismatch: {ga} vs {r['GST Amount']}")
        errors += 1
    # Total Bill
    tb = round(r["Net Sales"] + r["GST Amount"], 2)
    if abs(tb - r["Total Bill"]) > 0.01:
        print(f"Row {i} Total Bill mismatch: {tb} vs {r['Total Bill']}")
        errors += 1
    # Customer count
    if r["Customer Count"] < 1:
        print(f"Row {i} Customer count < 1: {r['Customer Count']}")
        errors += 1
    if r["Customer Count"] > r["Units Sold"]:
        print(f"Row {i} Customer count {r['Customer Count']} > Units Sold {r['Units Sold']}")
        errors += 1
    # Avg Bill size
    abs_calc = round(r["Total Bill"] / r["Customer Count"], 2)
    if abs(abs_calc - r["Average Bill Size"]) > 0.01:
        print(f"Row {i} Average Bill Size mismatch: {abs_calc} vs {r['Average Bill Size']}")
        errors += 1

if errors == 0:
    print("All mathematical calculations verified and are 100% correct!")
else:
    print(f"Validation failed with {errors} errors.")


# Generate Summary 1: Monthly Sales Summary & Profit Estimate
monthly_data = {}
for r in records:
    d = datetime.datetime.strptime(r["Transaction Date"], "%Y-%m-%d")
    key = (d.year, d.month, r["Month"], r["Financial Year"])
    if key not in monthly_data:
        monthly_data[key] = {
            "Units Sold": 0, "Gross Sales": 0.0, "Discount Amount": 0.0,
            "Net Sales": 0.0, "GST Amount": 0.0, "Total Bill": 0.0,
            "Customer Count": 0
        }
    monthly_data[key]["Units Sold"] += r["Units Sold"]
    monthly_data[key]["Gross Sales"] += r["Gross Sales"]
    monthly_data[key]["Discount Amount"] += r["Discount Amount"]
    monthly_data[key]["Net Sales"] += r["Net Sales"]
    monthly_data[key]["GST Amount"] += r["GST Amount"]
    monthly_data[key]["Total Bill"] += r["Total Bill"]
    monthly_data[key]["Customer Count"] += r["Customer Count"]

monthly_records = []
for (yr, m_num, m_name, fy) in sorted(monthly_data.keys(), key=lambda x: (x[0], x[1])):
    m_info = monthly_data[(yr, m_num, m_name, fy)]
    net_s = m_info["Net Sales"]
    tot_b = m_info["Total Bill"]
    
    # Cost Model: COGS = 35%, Labor = 20%, Rent = 15% of Net Sales
    cogs = round(net_s * 0.35, 2)
    labor = round(net_s * 0.20, 2)
    rent = round(net_s * 0.15, 2)
    profit = round(net_s * 0.30, 2)
    
    avg_spend = round(tot_b / m_info["Customer Count"], 2)
    
    monthly_records.append({
        "Month": m_name,
        "Year": yr,
        "Financial Year": fy,
        "Total Units Sold": m_info["Units Sold"],
        "Gross Sales": round(m_info["Gross Sales"], 2),
        "Total Discount": round(m_info["Discount Amount"], 2),
        "Net Sales": round(net_s, 2),
        "Total GST": round(m_info["GST Amount"], 2),
        "Total Revenue": round(tot_b, 2),
        "Est COGS": cogs,
        "Est Labor Cost": labor,
        "Est Rent Utilities": rent,
        "Est Net Profit": profit,
        "Customer Footfall": m_info["Customer Count"],
        "Average Spend Per Customer": avg_spend
    })

monthly_summary_path = "reports/monthly_summary.csv"
with open(monthly_summary_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Month", "Year", "Financial Year", "Total Units Sold", "Gross Sales", 
        "Total Discount", "Net Sales", "Total GST", "Total Revenue", 
        "Est COGS", "Est Labor Cost", "Est Rent Utilities", "Est Net Profit",
        "Customer Footfall", "Average Spend Per Customer"
    ])
    writer.writeheader()
    writer.writerows(monthly_records)
print("Exported monthly_summary.csv")


# Generate Summary 2: Outlet Performance Summary
outlet_data = {}
outlet_prod_units = {}

for r in records:
    oid = r["Outlet ID"]
    oname = r["Outlet Name"]
    area = r["Area"]
    mname = r["Manager Name"]
    pname = r["Product Name"]
    units = r["Units Sold"]
    
    if oid not in outlet_data:
        outlet_data[oid] = {
            "name": oname, "area": area, "manager": mname,
            "Units Sold": 0, "Revenue": 0.0, "Customer Count": 0,
            "Peak Hour Sales Sum": 0.0, "Count": 0
        }
    outlet_data[oid]["Units Sold"] += units
    outlet_data[oid]["Revenue"] += r["Total Bill"]
    outlet_data[oid]["Customer Count"] += r["Customer Count"]
    outlet_data[oid]["Peak Hour Sales Sum"] += r["Peak Hour Sales %"]
    outlet_data[oid]["Count"] += 1
    
    prod_key = (oid, pname)
    outlet_prod_units[prod_key] = outlet_prod_units.get(prod_key, 0) + units

outlet_records = []
for oid, info in outlet_data.items():
    prod_units = [(pname, u) for (o, pname), u in outlet_prod_units.items() if o == oid]
    prod_units.sort(key=lambda x: x[1], reverse=True)
    best_prod = prod_units[0][0]
    worst_prod = prod_units[-1][0]
    
    avg_bill = round(info["Revenue"] / info["Customer Count"], 2)
    avg_peak = round(info["Peak Hour Sales Sum"] / info["Count"], 2)
    
    if info["name"] == "Koramangala":
        lunch_peak = "30-35%"
        evening_peak = "65-70%"
    elif info["name"] == "Whitefield":
        lunch_peak = "60-65%"
        evening_peak = "35-40%"
    elif info["name"] == "Electronic City":
        lunch_peak = "50-55%"
        evening_peak = "45-50%"
    elif info["name"] == "MG Road":
        lunch_peak = "35-40%"
        evening_peak = "60-65%"
    else:
        lunch_peak = "45-50%"
        evening_peak = "50-55%"
        
    outlet_records.append({
        "Outlet ID": oid,
        "Outlet Name": info["name"],
        "Area": info["area"],
        "Manager Name": info["manager"],
        "Total Units Sold": info["Units Sold"],
        "Total Revenue": round(info["Revenue"], 2),
        "Total Customer Count": info["Customer Count"],
        "Average Bill Size": avg_bill,
        "Avg Peak Hour Sales %": avg_peak,
        "Lunch Peak Share Est": lunch_peak,
        "Evening Peak Share Est": evening_peak,
        "Best Selling Product": best_prod,
        "Worst Selling Product": worst_prod
    })

outlet_records.sort(key=lambda x: x["Total Revenue"], reverse=True)

outlet_summary_path = "reports/outlet_summary.csv"
with open(outlet_summary_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Outlet ID", "Outlet Name", "Area", "Manager Name", "Total Units Sold",
        "Total Revenue", "Total Customer Count", "Average Bill Size",
        "Avg Peak Hour Sales %", "Lunch Peak Share Est", "Evening Peak Share Est",
        "Best Selling Product", "Worst Selling Product"
    ])
    writer.writeheader()
    writer.writerows(outlet_records)
print("Exported outlet_summary.csv")


# Generate Summary 3: Product-wise Sales Summary
product_data = {}
total_chain_revenue = sum(r["Total Bill"] for r in records)

for r in records:
    pid = r["Product ID"]
    pname = r["Product Name"]
    cat = r["Category"]
    
    if pid not in product_data:
        product_data[pid] = {
            "name": pname, "category": cat, "Units Sold": 0, "Gross Sales": 0.0,
            "Discount Amount": 0.0, "Net Sales": 0.0, "GST Amount": 0.0, "Revenue": 0.0,
            "Price Sum": 0.0, "Price Count": 0
        }
    p_info = product_data[pid]
    p_info["Units Sold"] += r["Units Sold"]
    p_info["Gross Sales"] += r["Gross Sales"]
    p_info["Discount Amount"] += r["Discount Amount"]
    p_info["Net Sales"] += r["Net Sales"]
    p_info["GST Amount"] += r["GST Amount"]
    p_info["Revenue"] += r["Total Bill"]
    p_info["Price Sum"] += r["Unit Price"]
    p_info["Price Count"] += 1

product_records = []
for pid, info in product_data.items():
    share_pct = round((info["Revenue"] / total_chain_revenue) * 100, 2)
    avg_price = round(info["Price Sum"] / info["Price Count"], 2)
    
    product_records.append({
        "Product ID": pid,
        "Product Name": info["name"],
        "Category": info["category"],
        "Avg Unit Price": avg_price,
        "Total Units Sold": info["Units Sold"],
        "Gross Sales": round(info["Gross Sales"], 2),
        "Total Discount Amount": round(info["Discount Amount"], 2),
        "Total Net Sales": round(info["Net Sales"], 2),
        "Total GST Amount": round(info["GST Amount"], 2),
        "Total Revenue": round(info["Revenue"], 2),
        "Sales Share %": share_pct
    })

product_records.sort(key=lambda x: x["Total Revenue"], reverse=True)

product_summary_path = "reports/product_summary.csv"
with open(product_summary_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Product ID", "Product Name", "Category", "Avg Unit Price", "Total Units Sold",
        "Gross Sales", "Total Discount Amount", "Total Net Sales", "Total GST Amount",
        "Total Revenue", "Sales Share %"
    ])
    writer.writeheader()
    writer.writerows(product_records)
print("Exported product_summary.csv")


# Generate Summary 4: dashboard_summary.csv
dashboard_rows = []

total_revenue = sum(r["Total Bill"] for r in records)
total_customers = sum(r["Customer Count"] for r in records)
total_days = len(date_list)
avg_daily_sales = round(total_revenue / total_days, 2)
avg_order_value = round(total_revenue / total_customers, 2)

prod_totals = {p["name"]: 0 for p in products}
for r in records:
    prod_totals[r["Product Name"]] += r["Units Sold"]
best_selling_product = max(prod_totals, key=prod_totals.get)

outlet_revenues = {}
for r in records:
    oid = r["Outlet ID"]
    oname = r["Outlet Name"]
    outlet_revenues[oname] = outlet_revenues.get(oname, 0.0) + r["Total Bill"]
best_outlet = max(outlet_revenues, key=outlet_revenues.get)
worst_outlet = min(outlet_revenues, key=outlet_revenues.get)

month_revenues = {}
for r in records:
    mkey = f"{r['Month']} {datetime.datetime.strptime(r['Transaction Date'], '%Y-%m-%d').year}"
    month_revenues[mkey] = month_revenues.get(mkey, 0.0) + r["Total Bill"]
highest_month = max(month_revenues, key=month_revenues.get)
lowest_month = min(month_revenues, key=month_revenues.get)

quarter_revenues = {}
for r in records:
    q = r["Quarter"]
    quarter_revenues[q] = quarter_revenues.get(q, 0.0) + r["Total Bill"]

def add_kpi(name, val):
    dashboard_rows.append({
        "Metric Group": "Executive KPI",
        "Metric Name": name,
        "Metric Value": str(val)
    })

add_kpi("Total Revenue (INR)", round(total_revenue, 2))
add_kpi("Total Customer Footfall", total_customers)
add_kpi("Average Daily Sales (INR)", avg_daily_sales)
add_kpi("Average Order Value (INR)", avg_order_value)
add_kpi("Best Selling Product", best_selling_product)
add_kpi("Best Outlet Name", best_outlet)
add_kpi("Worst Outlet Name", worst_outlet)
add_kpi("Highest Revenue Month", highest_month)
add_kpi("Lowest Revenue Month", lowest_month)
add_kpi("Year-over-Year Trend", "+12.4% (vs Fictional FY24-25 baseline)")

for q, rev in sorted(quarter_revenues.items()):
    add_kpi(f"Revenue {q} (INR)", round(rev, 2))

daily_revenues = {}
for r in records:
    d = r["Transaction Date"]
    daily_revenues[d] = daily_revenues.get(d, 0.0) + r["Total Bill"]

top_10_days = sorted(daily_revenues.items(), key=lambda x: x[1], reverse=True)[:10]
for idx, (day_val, rev) in enumerate(top_10_days, 1):
    dashboard_rows.append({
        "Metric Group": "Top 10 Revenue Days",
        "Metric Name": f"Rank {idx}: {day_val}",
        "Metric Value": round(rev, 2)
    })

bottom_10_days = sorted(daily_revenues.items(), key=lambda x: x[1])[:10]
for idx, (day_val, rev) in enumerate(bottom_10_days, 1):
    dashboard_rows.append({
        "Metric Group": "Bottom 10 Revenue Days",
        "Metric Name": f"Rank {idx}: {day_val}",
        "Metric Value": round(rev, 2)
    })

payment_mode_revs = {}
for r in records:
    pm = r["Payment Mode"]
    payment_mode_revs[pm] = payment_mode_revs.get(pm, 0.0) + r["Total Bill"]

for pm, rev in sorted(payment_mode_revs.items(), key=lambda x: x[1], reverse=True):
    pm_share = round((rev / total_revenue) * 100, 2)
    dashboard_rows.append({
        "Metric Group": "Payment Mode Distribution",
        "Metric Name": pm,
        "Metric Value": f"{pm_share}% Share (INR {round(rev, 2)})"
    })

dashboard_summary_path = "reports/dashboard_summary.csv"
with open(dashboard_summary_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Metric Group", "Metric Name", "Metric Value"])
    writer.writeheader()
    writer.writerows(dashboard_rows)
print("Exported dashboard_summary.csv")

print("All tasks completed successfully!")
