// Configure Chart.js global defaults for sleek dark mode aesthetics
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.backgroundColor = '#141621e6';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.plugins.tooltip.titleFont = { family: "'Outfit', sans-serif", weight: 700, size: 13 };
Chart.defaults.plugins.tooltip.bodyFont = { family: "'Plus Jakarta Sans', sans-serif" };

// Utility to parse floating numbers cleanly
const parseVal = (str) => {
    return parseFloat(str.replace(/[^0-9.-]/g, ''));
};

// Main execution function
document.addEventListener("DOMContentLoaded", () => {
    loadDashboardKPIs();
    loadMonthlySummary();
    loadOutletSummary();
    loadProductSummary();
});

// 1. Load and Parse dashboard_summary.csv for KPIs and Payment mode
function loadDashboardKPIs() {
    Papa.parse("reports/dashboard_summary.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            const rows = results.data;
            const kpis = {};
            const paymentModes = [];
            
            rows.forEach(r => {
                const group = r["Metric Group"];
                const name = r["Metric Name"];
                const val = r["Metric Value"];
                
                if (group === "Executive KPI") {
                    kpis[name] = val;
                } else if (group === "Payment Mode Distribution") {
                    // Expecting value: "45.48% Share (INR 62499749.82)"
                    const share = parseFloat(val.split("%")[0]);
                    paymentModes.push({ name: name, share: share });
                }
            });

            // Update DOM KPIs
            if (kpis["Total Revenue (INR)"]) {
                const rev = parseVal(kpis["Total Revenue (INR)"]);
                document.querySelector("#kpi-revenue .kpi-value").innerText = "₹" + (rev / 10000000).toFixed(2) + " Cr";
            }
            if (kpis["Total Customer Footfall"]) {
                const foot = parseVal(kpis["Total Customer Footfall"]);
                document.querySelector("#kpi-footfall .kpi-value").innerText = foot.toLocaleString("en-IN");
            }
            if (kpis["Average Order Value (INR)"]) {
                document.querySelector("#kpi-aov .kpi-value").innerText = "₹" + parseFloat(kpis["Average Order Value (INR)"]).toFixed(2);
            }
            if (kpis["Best Selling Product"]) {
                document.querySelector("#kpi-best-prod .kpi-value").innerText = kpis["Best Selling Product"];
            }
            if (kpis["Best Outlet Name"]) {
                document.querySelector("#kpi-best-outlet .kpi-value").innerText = kpis["Best Outlet Name"];
            }

            // Create Payment mode chart
            if (paymentModes.length > 0) {
                createPaymentChart(paymentModes);
            }
        }
    });
}

// 2. Load and Parse monthly_summary.csv for Monthly Sales & Profit Trend
function loadMonthlySummary() {
    Papa.parse("reports/monthly_summary.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            const data = results.data;
            const labels = data.map(r => r["Month"] + " " + r["Year"].slice(2));
            const revenues = data.map(r => parseVal(r["Total Revenue"]));
            const profits = data.map(r => parseVal(r["Est Net Profit"]));
            
            createMonthlyChart(labels, revenues, profits);
        }
    });
}

// 3. Load and Parse outlet_summary.csv for Outlet Performance Summary Table & Charts
function loadOutletSummary() {
    Papa.parse("reports/outlet_summary.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            const outlets = results.data;
            
            // Populate Table
            const tbody = document.querySelector("#outletTable tbody");
            tbody.innerHTML = ""; // Clear loader
            
            outlets.forEach((o, index) => {
                const tr = document.createElement("tr");
                
                // Highlight Top & Bottom performers
                let nameClass = "";
                if (index === 0) nameClass = "high-perf-text"; // Top performer
                else if (index === outlets.length - 1) nameClass = "low-perf-text"; // Bottom performer
                else nameClass = "med-perf-text";
                
                // Peak Sales description
                const peakStr = `${o["Lunch Peak Share Est"]} / ${o["Evening Peak Share Est"]}`;
                
                tr.innerHTML = `
                    <td><code>${o["Outlet ID"]}</code></td>
                    <td class="${nameClass}"><strong>${o["Outlet Name"]}</strong></td>
                    <td>${o["Area"]}</td>
                    <td>${o["Manager Name"]}</td>
                    <td>${parseInt(o["Total Units Sold"]).toLocaleString("en-IN")}</td>
                    <td><strong>₹${parseFloat(o["Total Revenue"]).toLocaleString("en-IN", {maximumFractionDigits: 0})}</strong></td>
                    <td>${parseInt(o["Total Customer Count"]).toLocaleString("en-IN")}</td>
                    <td>₹${parseFloat(o["Average Bill Size"]).toFixed(2)}</td>
                    <td>${peakStr}</td>
                    <td>${o["Best Selling Product"]}</td>
                `;
                tbody.appendChild(tr);
            });

            // Update Best Outlet revenue sub-badge in KPI card
            if (outlets.length > 0) {
                const bestOutName = outlets[0]["Outlet Name"];
                const bestOutRev = parseVal(outlets[0]["Total Revenue"]);
                document.getElementById("best-outlet-rev").innerText = "₹" + (bestOutRev / 100000).toFixed(2) + " Lakhs Rev";
            }

            // Create Outlet performance comparison chart
            createOutletChart(outlets);
        }
    });
}

// 4. Load and Parse product_summary.csv for Product Sales shares
function loadProductSummary() {
    Papa.parse("reports/product_summary.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            const data = results.data;
            const names = data.map(r => r["Product Name"]);
            const shares = data.map(r => parseFloat(r["Sales Share %"]));
            const revenues = data.map(r => parseVal(r["Total Revenue"]));
            
            createProductChart(names, shares, revenues);
        }
    });
}

// --- Chart Generation Helpers ---

function createMonthlyChart(labels, revenues, profits) {
    const ctx = document.getElementById("monthlyTrendChart").getContext("2d");
    
    // Create soft gradients
    const revenueGrad = ctx.createLinearGradient(0, 0, 0, 300);
    revenueGrad.addColorStop(0, "rgba(99, 102, 241, 0.4)");
    revenueGrad.addColorStop(1, "rgba(99, 102, 241, 0.0)");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Monthly Total Revenue (INR)",
                    data: revenues,
                    borderColor: "#6366f1",
                    backgroundColor: revenueGrad,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 3,
                    pointBackgroundColor: "#6366f1",
                    pointHoverRadius: 7,
                    yAxisID: "y-rev"
                },
                {
                    label: "Estimated Net Profit (INR)",
                    data: profits,
                    borderColor: "#10b981",
                    borderWidth: 3,
                    borderDash: [5, 5],
                    pointBackgroundColor: "#10b981",
                    fill: false,
                    tension: 0.1,
                    pointHoverRadius: 6,
                    yAxisID: "y-rev" // Same scale or can use dual-axis, keeping same scale is cleaner here
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "top",
                    labels: { boxWidth: 15, padding: 20, color: '#f1f3f9' }
                }
            },
            scales: {
                "y-rev": {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: {
                        callback: function(val) {
                            return "₹" + (val / 100000).toFixed(0) + "L";
                        }
                    }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

function createProductChart(names, shares, revenues) {
    const ctx = document.getElementById("productShareChart").getContext("2d");
    
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: names,
            datasets: [{
                data: shares,
                backgroundColor: [
                    "#6366f1", // Indigo for Chicken Burger
                    "#06b6d4", // Teal for Veg Burger
                    "#f59e0b"  // Amber for French Fries
                ],
                borderWidth: 2,
                borderColor: "#141621",
                hoverOffset: 12
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "70%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { boxWidth: 12, padding: 15, color: '#f1f3f9' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const val = revenues[context.dataIndex];
                            return `${context.label}: ${context.raw}% (₹${(val / 100000).toFixed(1)}L)`;
                        }
                    }
                }
            }
        }
    });
}

function createOutletChart(outlets) {
    const ctx = document.getElementById("outletBarChart").getContext("2d");
    
    const names = outlets.map(o => o["Outlet Name"]);
    const revenues = outlets.map(o => parseVal(o["Total Revenue"]));
    const aovs = outlets.map(o => parseFloat(o["Average Bill Size"]));
    
    // Create gradient
    const barGrad = ctx.createLinearGradient(0, 0, 500, 0);
    barGrad.addColorStop(0, "rgba(6, 182, 212, 0.85)");
    barGrad.addColorStop(1, "rgba(99, 102, 241, 0.85)");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: names,
            datasets: [
                {
                    label: "Total Sales Revenue (INR)",
                    data: revenues,
                    backgroundColor: barGrad,
                    borderRadius: 6,
                    borderWidth: 0,
                    yAxisID: "y-rev"
                }
            ]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const val = context.raw;
                            const aov = aovs[context.dataIndex];
                            return `Revenue: ₹${(val/100000).toFixed(2)}L (AOV: ₹${aov.toFixed(0)})`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: {
                        callback: function(val) {
                            return "₹" + (val / 100000).toFixed(0) + "L";
                        }
                    }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

function createPaymentChart(paymentModes) {
    const ctx = document.getElementById("paymentModeChart").getContext("2d");
    const labels = paymentModes.map(p => p.name);
    const shares = paymentModes.map(p => p.share);
    
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: shares,
                backgroundColor: [
                    "#06b6d4", // UPI: Teal
                    "#6366f1", // Credit Card: Indigo
                    "#f43f5e", // Cash: Rose
                    "#a855f7", // Debit Card: Purple
                    "#f59e0b"  // Wallet: Amber
                ],
                borderWidth: 2,
                borderColor: "#141621"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { boxWidth: 10, padding: 12, color: '#f1f3f9' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}
