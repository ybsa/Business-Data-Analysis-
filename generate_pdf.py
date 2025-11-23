from fpdf import FPDF
import os
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Strategic Business Analysis: A Data-Driven Story', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_image(self, image_path, title):
        if os.path.exists(image_path):
            self.image(image_path, x=15, w=180)
            self.ln(2)
            self.set_font('Arial', 'I', 9)
            self.cell(0, 5, title, 0, 1, 'C')
            self.ln(5)
        else:
            self.chapter_body(f"[Image not found: {image_path}]")

def generate_pdf():
    pdf = PDFReport()
    pdf.add_page()
    
    # Executive Summary / The Story
    pdf.chapter_title("The Story of Our Inventory: Challenges & Opportunities")
    pdf.chapter_body(
        "Every data point tells a story, and for our retail operations, the story is one of hidden potential waiting to be unlocked. "
        "We embarked on a journey through our sales and inventory data to answer a critical question: 'Are we working as efficiently as we could be?'\n\n"
        "The narrative that emerged was clear. We have a strong engine driven by a few key vendor relationships, but we are weighed down by "
        "inventory that isn't moving. Our analysis revealed a tale of two extremes: high-flying products that fly off the shelves, and "
        "dormant brands that tie up our capital. This report outlines the chapters of this story and proposes a happy ending: optimized operations and higher profitability."
    )
    
    # Chapter 1: The Weight of the Past (Underperforming Brands)
    pdf.chapter_title("Chapter 1: The Weight of the Past (Underperforming Brands)")
    pdf.chapter_body(
        "Our first discovery was the 'dead weight' in our warehouse. We found 20 brands that have been sitting silently, contributing almost nothing to our bottom line. "
        "These aren't just products; they are frozen capital that could be used elsewhere. The chart below visualizes these silent anchors."
    )
    pdf.add_image("images/brands.png", "The Silent Anchors: Top Underperforming Brands")
    pdf.chapter_body(
        "**The Plot Twist:** By liberating ourselves from these underperforming brands through clearance or strategic bundling, we can free up resources for the winners."
    )

    # Chapter 2: The Heroes (Top Vendors)
    pdf.chapter_title("Chapter 2: The Heroes (Top Vendors)")
    pdf.chapter_body(
        "In every story, there are heroes. For us, a small group of vendors are carrying the torch, driving the vast majority of our revenue. "
        "These partners are the backbone of our success. The data shows a clear Pareto principle at play: a few key players deliver the most value."
    )
    pdf.add_image("images/vendors.png", "Our Revenue Heroes: Top Vendors")
    pdf.chapter_body(
        "**Strategic Move:** We shouldn't just transact with these vendors; we should partner with them. Deepening these relationships is our path to stability."
    )

    # Chapter 3: The Power of Scale (Bulk Purchasing)
    pdf.chapter_title("Chapter 3: The Power of Scale (Bulk Purchasing)")
    pdf.chapter_body(
        "As we looked deeper, we found a hidden lever for profitability: the power of scale. Our analysis of purchasing patterns revealed a secret weapon. "
        "When we buy in bulk, our unit costs drop significantly. We haven't always used this weapon effectively, leaving money on the table."
    )
    pdf.add_image("images/bulk.png", "Unlocking Value: Quantity vs. Price")
    pdf.chapter_body(
        "**The Opportunity:** By consolidating our orders, we can drive down costs immediately. It's a simple change with a dramatic impact on our margins."
    )

    # Chapter 4: The Pulse of the Business (Turnover)
    pdf.chapter_title("Chapter 4: The Pulse of the Business (Turnover)")
    pdf.chapter_body(
        "Finally, we checked the heartbeat of our operations: inventory turnover. A healthy business has a strong, steady pulse. "
        "We found that while some items are racing through our system, others are flatlining. The distribution below shows where we need to apply CPR."
    )
    pdf.add_image("images/turnover.png", "The Heartbeat: Inventory Turnover Rates")
    pdf.chapter_body(
        "**Action Plan:** We need to resuscitate or remove the low-turnover items to ensure our inventory remains fresh and profitable."
    )

    # Conclusion
    pdf.add_page()
    pdf.chapter_title("Epilogue: Writing the Next Chapter")
    pdf.chapter_body(
        "The story of our data points to a bright future, but only if we act. We have the map:\n"
        "1. Cut the dead weight (Underperforming Brands).\n"
        "2. Double down on our heroes (Top Vendors).\n"
        "3. Buy smarter, not harder (Bulk Purchasing).\n\n"
        "By taking these steps, the next chapter of our business story will be one of efficiency, growth, and maximized profit."
    )

    output_path = "Business_Analysis_Report.pdf"
    pdf.output(output_path, 'F')
    print(f"PDF Report generated: {output_path}")

if __name__ == "__main__":
    generate_pdf()
