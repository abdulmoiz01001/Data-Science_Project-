import os
from fpdf import FPDF

# Create directory
os.makedirs("report", exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Data Science Journey: The ShopSphere Project', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, num, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, f'Chapter {num}: {title}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(6)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# --- Content ---

intro = "Welcome to the story of ShopSphere's data! We began with three raw datasets: Customers, Orders, and Products. Our goal was to transition into Advanced Analytics and Machine Learning. But as any data scientist knows, algorithms are only as good as the data they learn from. This document details how we built a robust pipeline to create a Gold Standard dataset."
pdf.set_font('helvetica', 'I', 12)
pdf.multi_cell(0, 7, intro)
pdf.ln(10)

ch1_body = "Our journey began with a deep investigation into the data's health. We loaded our datasets and profiled them to identify structural issues, missing values, and anomalies. We found inconsistent text formatting, invalid datatypes, impossible demographic values (like ages of 150), and missing critical fields across all three tables."
pdf.chapter_title(1, 'Phase 1: Data Understanding & Profiling')
pdf.chapter_body(ch1_body)

ch2_body = "Data cleaning is the foundation of Machine Learning. We took decisive actions:\n\nStep 1: Removing Duplicates. We dropped 60 exact duplicate rows across all datasets to prevent biased metrics and incorrect revenue calculations.\n\nStep 2: Demographic Validation. We strictly enforced business rules. Ages outside 18-100 were replaced with the median age (42). Invalid phone numbers and emails were converted to missing values, as guessing unique identifiers risks corrupting customer records.\n\nStep 3: Handling Missing & Anomalous Financials. We discovered impossible negative shipping costs and discounts exceeding 100%. These were removed and imputed using median values, ensuring statistical robustness without distorting the data with extreme outliers.\n\nStep 4: Acknowledging Unrecoverable Data. We proved that some missing prices, costs, and dates could not be recovered from any source. We made the professional choice to leave them as missing (NaN) rather than introducing false data."
pdf.chapter_title(2, 'Phase 2: Data Cleaning & Business Rules')
pdf.chapter_body(ch2_body)

ch3_body = "With clean data, we needed to understand the business visually. We used Matplotlib and Seaborn to plot customer distributions across cities and identify the top and bottom revenue-generating products.\n\nBusiness Strategy: Visualizations bridge the gap between complex data and human intuition. They allow stakeholders to see the exact patterns that our future Machine Learning models will learn."
pdf.chapter_title(3, 'Phase 3: Visualizing the Business')
pdf.chapter_body(ch3_body)

ch4_body = "In the final phase, we mathematically engineered new metrics to give our models deeper context.\n\nWe implemented ABC Analysis, categorizing products into A, B, and C classes based on their cumulative revenue contribution to identify our most valuable inventory.\n\nWe also segmented products into Fast, Medium, and Slow moving categories based on quantity percentiles, and ranked products by overall performance.\n\nBusiness Strategy: By engineering these features, we transform simple transaction logs into powerful predictive profiles perfectly suited for forecasting and inventory optimization."
pdf.chapter_title(4, 'Phase 4: Advanced Feature Engineering')
pdf.chapter_body(ch4_body)

conclusion = "And so, our pipeline is complete. We went from raw, messy data to a clean, feature-rich powerhouse. We successfully removed critical errors, applied robust imputation strategies, and built high-value business features. The ShopSphere dataset is now fully prepared for advanced predictive modeling!"
pdf.set_font('helvetica', 'B', 12)
pdf.multi_cell(0, 7, conclusion)

pdf.output('report/Data_Science_Journey.pdf')
print("PDF created successfully!")
