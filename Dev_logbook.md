# Project Developer Logbook: Restaurant Sales Synthetic Dataset

This logbook records the design decisions, development timeline, validation checks, and folder structure changes implemented during the building of this synthetic sales dataset generator.

---

## 1. Project Directory Structure

Following the organizational restructuring, the project files are arranged as follows:

```
restaurant_sales_dashboard/
├── datasets/
│   └── sales_data.csv            # Transaction-level dataset (10,950 records)
├── reports/
│   ├── dashboard_summary.csv     # Executive KPIs, Top/Bottom Days, & Payments
│   ├── monthly_summary.csv       # MoM sales, footfall, and estimated net profit
│   ├── outlet_summary.csv        # Performance summary by retail outlet
│   └── product_summary.csv       # Product category and sales shares summary
├── generate_sales_data.py        # Self-contained Python data generation engine
├── get_descriptive_stats.py       # Python script for descriptive statistics
└── Dev_logbook.md                # Developer history and decisions (this file)
```

---

## 2. Development Timeline

### Phase 1: Implementation & Planning (August 4, 2026 - 12:07 PM)
- **Goal**: Establish the base schema and define fictional parameters (outlets, managers, prices, products, and calendars).
- **Design Decisions**:
  - Selected the standard Indian Financial Year cycle (FY 2025-26 and FY 2026-27) starting from April 1, with quarters matching tax reporting.
  - Defined unique manager assignments and customized baseline pricing configurations per store to represent variations across premium Bengaluru areas.
  - Placed base multipliers in the algorithm to incorporate weekend peaks, Friday evening rushes, weather drops (10-20% for rainy days), and outlet-specific footfall profiles.

### Phase 2: Generation & Debugging (August 4, 2026 - 12:38 PM)
- **Execution**: Ran the script `generate_sales_data.py`.
- **Encountered Issue**: 
  - `ValueError: too many values to unpack (expected 2)` on the dictionary sorting logic during monthly summary generation.
  - *Cause*: The loop attempted to unpack key-value pairs from `sorted(monthly_data.keys())` which only yields key tuples.
- **Resolution**:
  - Refactored the loop signature from `for (yr, m_num, m_name, fy), val in sorted(...)` to `for (yr, m_num, m_name, fy) in sorted(...)` and fetched values inside the block.
- **Validation**: Re-ran the generation. All 10,950 records passed the built-in validation module verifying 100% mathematical accuracy.

### Phase 3: Folder Restructuring (August 4, 2026 - 12:44 PM)
- **Refactoring Request**: Arrange output files into distinct folders (`datasets` and `reports`).
- **Implementation**:
  - Updated imports and added automatic folder initialization `os.makedirs(..., exist_ok=True)` in `generate_sales_data.py`.
  - Re-routed all CSV file paths (`sales_data.csv` to `datasets/` and summaries to `reports/`).
  - Cleared old duplicate CSV files from the root directory.
  - Verified directory layout and updated links inside [walkthrough.md](file:///C:/Users/rohib/.gemini/antigravity-ide/brain/59fb5416-deab-4b84-a3ad-25ca7224eee2/walkthrough.md).

### Phase 4: Descriptive Statistics Script (August 4, 2026 - 12:50 PM)
- **Goal**: Implement an analytical tool to calculate descriptive statistics for validation and audit.
- **Implementation**:
  - Created `get_descriptive_stats.py` supporting both standard Python (fallback mode) and Pandas (pro mode) formatting.
  - Provides total counts, min/max range, mean, standard deviation, and breakdowns by outlet performance, product shares, payment distributions, and weather impacts.

---

## 3. Key Design Choices & Business Logic

### Pricing System (₹ INR)
- Fictional menus have fixed unit prices per store to mimic actual franchise operations.
- Prices conform strictly to constraints:
  - Chicken Burger: ₹180 to ₹225 (Limit: ₹170 - ₹230)
  - Veg Burger: ₹130 to ₹165 (Limit: ₹120 - ₹170)
  - French Fries: ₹85 to ₹115 (Limit: ₹80 - ₹130)

### Volume Modifiers (Base Multipliers)
- **Monsoon season (Jun-Sep)**: Increased chance of rainy weather, reducing walk-ins and customer footfall.
- **Heavy Rainfall Event**: 18% sales drop (cumulative with rainy weather factor).
- **Store-specific Profiles**:
  - *Electronic City*: Weekday-heavy (1.25x), weekend-light (0.6x).
  - *MG Road*: Weekend-heavy (1.45x), weekday-light (0.8x).
  - *Koramangala & Whitefield*: Elevated peak hour percentages representing dinner and lunch spikes respectively.
  - *Indiranagar*: Best overall base units sold (100 base units).

### Mathematical Rules
All columns conform to strict equations:
- `Gross Sales = Units Sold * Unit Price`
- `Discount Amount = round(Gross Sales * Discount %, 2)`
- `Net Sales = Gross Sales - Discount Amount`
- `GST Amount = round(Net Sales * 5%, 2)`
- `Total Bill = Net Sales + GST Amount`
- `Customer Count = round(Units Sold / avg_units_per_cust)` *(avg_units_per_cust between 1.2 and 1.5)*
- `Average Bill Size = round(Total Bill / Customer Count, 2)`

---

## 4. How to Reproduce, Regenerate, or Analyze Data

### Regenerating the Datasets
To regenerate the datasets or reset them, execute the following command from the root of the workspace directory:

```bash
python generate_sales_data.py
```

*Note: The script will automatically recreate the `datasets/` and `reports/` folders and populate them with fresh, validated CSV files.*

### Analyzing the Datasets (Descriptive Statistics)
To view the descriptive statistics and summaries of the generated data, run:

```bash
python get_descriptive_stats.py
```
