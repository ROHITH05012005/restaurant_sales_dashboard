# 🍔 BiteAnalytics: Restaurant Sales Synthetic Dataset & Interactive BI Dashboard

A self-contained synthetic sales data generator and an interactive web analytics dashboard for a fictional fast-food chain. It models premium outlets located in commercial areas across Bengaluru, India, over a full year (August 1, 2025, to July 31, 2026).

* **Live Interactive Dashboard**: [restaurantsalesdashboard.vercel.app](https://restaurantsalesdashboard.vercel.app)
* **GitHub Repository**: [github.com/ROHITH05012005/restaurant_sales_dashboard](https://github.com/ROHITH05012005/restaurant_sales_dashboard)

---

## 📂 Project Directory Structure

```
restaurant_sales_dashboard/
├── datasets/
│   └── sales_data.csv            # Main transaction-level dataset (10,950 records)
├── reports/
│   ├── dashboard_summary.csv     # Executive KPIs, Top/Bottom Days, & Payments
│   ├── monthly_summary.csv       # MoM sales, footfall, and estimated net profit
│   ├── outlet_summary.csv        # Performance summary by retail outlet
│   └── product_summary.csv       # Product category and sales shares summary
├── generate_sales_data.py        # Self-contained Python data generation engine
├── get_descriptive_stats.py       # Python script to analyze statistics and audit
├── index.html                    # Dashboard layout and structure (Static UI)
├── style.css                     # Premium dark glassmorphic dashboard theme
├── app.js                        # JavaScript parsing logic (PapaParse & Chart.js)
├── Dev_logbook.md                # Developer history, timelines, and logic choices
└── README.md                     # Main project guide (this file)
```

---

## ⚙️ Data Generation & Business Logic

The transaction dataset consists of exactly **10,950 records** (365 days × 10 outlets × 3 products). It is built with zero placeholders or missing fields, and enforces total mathematical consistency.

### Simulated Variables & Rules
1. **Dynamic Pricing System**: Each outlet charges fixed unit prices per product based on their demographic area profile (all within the requested constraints).
2. **Weekly & Seasonal Patterns**: Saturday and Sunday show elevated sales, Friday evening shows a strong rush, and December holidays (Christmas, New Year's Eve) see spikes of 30-50%.
3. **Monsoon/Weather Factors**: Heavy rain and monsoon months (June-September) reduce footfall and sales by 10-20%.
4. **Regional Profiles**:
   - *Electronic City*: 1.25x weekday multiplier (IT parks), 0.6x weekend drop.
   - *MG Road*: 1.45x weekend multiplier (party-goers), 0.8x weekday drop.
   - *Koramangala*: Dinner-heavy peak (65-70% share).
   - *Whitefield*: Lunch-heavy peak (60-65% share).
   - *Indiranagar*: Consistently high-performing store (100 base units).

---

## 💻 Running the Project Locally

### 1. Data Generation
To regenerate the datasets and rebuild all summary reports:
```bash
python generate_sales_data.py
```

### 2. Descriptive Statistics & Audit
To view descriptive statistics (min, max, mean, standard deviation, and categorical shares) directly in your terminal:
```bash
python get_descriptive_stats.py
```

### 3. Open the Web Dashboard
Since the web dashboard runs entirely in the browser using static HTML, CSS, and JS:
- Double-click `index.html` to open it in any web browser, OR
- Serve it using a local server (e.g., Live Server in VS Code, or run `python -m http.server 8000` and visit `http://localhost:8000`).

---

## 🚀 Publishing to GitHub

To put this project on version control and push it to GitHub:

1. **Initialize Git & Commit Locally**:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit of dataset, generation scripts, and interactive dashboard"
   ```

2. **Connect to GitHub**:
   - Create a new blank repository on [GitHub](https://github.com/new).
   - Run the following commands (replace with your repository url):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

---

## 🌐 Deploying to Vercel

The dashboard is designed as a static website, making it compatible with Vercel's free hosting:

### Method A: Import via GitHub (Recommended)
1. Sign in to [Vercel](https://vercel.com) using your GitHub account.
2. Click **Add New** > **Project**.
3. Import your repository (`YOUR_REPO_NAME`).
4. Keep the default settings (Vercel automatically detects the static HTML project).
5. Click **Deploy**. Vercel will build and host your project at a custom subdomain (e.g. `your-repo-name.vercel.app`).

### Method B: Deploy via Vercel CLI
If you have Vercel CLI installed on your machine:
```bash
# In the project root directory
vercel
```
Follow the interactive CLI prompts to deploy directly from your command line.
