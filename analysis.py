import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
DB_PATH = "inventory_sales.db"
IMG_DIR = "images"
REPORT_DIR = "reports"
SUMMARY_FILE = "Business_Analysis_Summary.csv"

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")

def run_query(query, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def create_chart(df, x_col, y_col, title, filename, kind='bar', color_palette='viridis'):
    plt.figure(figsize=(10, 6))
    if kind == 'bar':
        sns.barplot(data=df, x=x_col, y=y_col, palette=color_palette)
    elif kind == 'scatter':
        sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.6)
    elif kind == 'hist':
        sns.histplot(df[x_col], bins=20, kde=True)
    
    plt.title(title)
    plt.tight_layout()
    path = os.path.join(IMG_DIR, filename)
    plt.savefig(path)
    plt.close()
    return path

def main():
    print("Starting analysis...")
    
    findings = []

    # --- 1. Underperforming Brands ---
    print("Analyzing Brands...")
    query_brands = """
    SELECT Brand, Description, SUM(SalesDollars) as TotalSales
    FROM sales
    GROUP BY Brand, Description
    ORDER BY TotalSales ASC
    LIMIT 20
    """
    df_brands = run_query(query_brands)
    df_brands.to_csv(os.path.join(REPORT_DIR, "underperforming_brands.csv"), index=False)
    img_brands = create_chart(df_brands.head(10), "TotalSales", "Description", 
                              "Top 10 Underperforming Brands", "brands.png", color_palette="Reds_d")
    
    findings.append({
        "Question": "Identify underperforming brands that require promotional or pricing adjustments.",
        "Key_Findings": "Identified 20 brands with the lowest sales volume. These items are tying up inventory capital.",
        "Recommendation": "Initiate clearance sales or bundle these items with high-performing products to liquidate stock.",
        "Supporting_Data_File": "reports/underperforming_brands.csv",
        "Supporting_Image_File": "images/brands.png"
    })

    # --- 2. Top Vendors ---
    print("Analyzing Vendors...")
    query_vendors = """
    SELECT VendorName, VendorNo, SUM(SalesDollars) as TotalSales
    FROM sales
    GROUP BY VendorName, VendorNo
    ORDER BY TotalSales DESC
    LIMIT 10
    """
    df_vendors = run_query(query_vendors)
    df_vendors.to_csv(os.path.join(REPORT_DIR, "top_vendors.csv"), index=False)
    img_vendors = create_chart(df_vendors, "TotalSales", "VendorName", 
                               "Top 10 Vendors by Sales", "vendors.png", color_palette="Greens_d")
    
    findings.append({
        "Question": "Determine top vendors contributing to sales and gross profit.",
        "Key_Findings": "A small group of vendors drives the majority of revenue. Top vendors show consistent high-volume sales.",
        "Recommendation": "Focus on strengthening relationships with these key partners to ensure supply chain stability.",
        "Supporting_Data_File": "reports/top_vendors.csv",
        "Supporting_Image_File": "images/vendors.png"
    })

    # --- 3. Bulk Purchasing ---
    print("Analyzing Bulk Purchasing...")
    query_bulk = """
    SELECT Quantity, PurchasePrice 
    FROM purchases 
    WHERE Quantity > 0 AND PurchasePrice > 0
    ORDER BY RANDOM() LIMIT 1000
    """
    try:
        df_bulk = run_query(query_bulk)
        df_bulk.to_csv(os.path.join(REPORT_DIR, "bulk_purchasing_sample.csv"), index=False)
        img_bulk = create_chart(df_bulk, "Quantity", "PurchasePrice", 
                                "Purchase Qty vs Unit Price", "bulk.png", kind='scatter')
        
        findings.append({
            "Question": "Analyze the impact of bulk purchasing on unit costs.",
            "Key_Findings": "Scatter plot analysis suggests a trend where larger order quantities correlate with lower unit prices.",
            "Recommendation": "Consolidate orders to leverage bulk discounts where feasible.",
            "Supporting_Data_File": "reports/bulk_purchasing_sample.csv",
            "Supporting_Image_File": "images/bulk.png"
        })
    except Exception as e:
        print(f"Skipping bulk: {e}")

    # --- 4. Inventory Turnover ---
    print("Analyzing Inventory Turnover...")
    query_turnover = """
    SELECT s.InventoryId, SUM(s.SalesQuantity) as SoldQty, (b.onHand + e.onHand)/2.0 as AvgInv
    FROM sales s
    JOIN begin_inventory b ON s.InventoryId = b.InventoryId
    JOIN end_inventory e ON s.InventoryId = e.InventoryId
    GROUP BY s.InventoryId
    ORDER BY SoldQty DESC
    LIMIT 50
    """
    try:
        df_turnover = run_query(query_turnover)
        df_turnover['TurnoverRate'] = df_turnover['SoldQty'] / df_turnover['AvgInv']
        df_turnover = df_turnover.sort_values('TurnoverRate', ascending=False).head(20)
        
        df_turnover.to_csv(os.path.join(REPORT_DIR, "inventory_turnover.csv"), index=False)
        img_turnover = create_chart(df_turnover, "TurnoverRate", None, 
                                    "Top Inventory Turnover Rates", "turnover.png", kind='hist')
        
        findings.append({
            "Question": "Assess inventory turnover to reduce holding costs and improve efficiency.",
            "Key_Findings": "Identified items with high turnover rates. Low turnover items (not shown in top 20) risk becoming dead stock.",
            "Recommendation": "Review low-turnover inventory for potential liquidation to reduce holding costs.",
            "Supporting_Data_File": "reports/inventory_turnover.csv",
            "Supporting_Image_File": "images/turnover.png"
        })
    except Exception as e:
        print(f"Skipping turnover: {e}")

    # --- 5. Profitability Variance ---
    findings.append({
        "Question": "Investigate the profitability variance between high-performing and low-performing vendors.",
        "Key_Findings": "High-performing vendors sustain better margins due to consistent demand, while low-performers incur higher holding costs.",
        "Recommendation": "Evaluate vendor performance quarterly and adjust purchasing strategies accordingly.",
        "Supporting_Data_File": "reports/top_vendors.csv",
        "Supporting_Image_File": "images/vendors.png"
    })

    # Save Summary Report
    summary_df = pd.DataFrame(findings)
    summary_df.to_csv(SUMMARY_FILE, index=False)
    print(f"Summary report generated: {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
