import os
from fpdf import FPDF

# Create directory
os.makedirs("report", exist_ok=True)

# Data Structure for the Book
book_content = [
    {
        "chapter": "Phase 1: The Detective's First Look (EDA)",
        "text": "BUSINESS STRATEGY:\nOur story begins by gathering our raw evidence: Customers, Orders, and Products. Before we clean, we must understand the landscape. We load the data and check for missing values, invalid datatypes, and anomalies like impossible ages (150) or negative discounts. Knowing the health of your data prevents fatal errors in Machine Learning later.",
        "code": '''import pandas as pd
customers_data = pd.read_csv("../data/customers.csv")
orders_data = pd.read_csv("../data/orders.csv")
products_data = pd.read_csv("../data/products.csv")

# Checking the health of the data
print(customers_data.info())
print(orders_data.isnull().sum())
print(orders_data.describe())'''
    },
    {
        "chapter": "Phase 2 (Step 1): Sweeping the Echoes (Duplicates)",
        "text": "BUSINESS STRATEGY:\nWe immediately noticed duplicated rows. In Machine Learning, duplicates create a false sense of pattern frequency (bias) and inflate revenue. We eliminated 60 duplicates across datasets to maintain a pure signal, creating clean copies to preserve the original data.",
        "code": '''# Create working copies for Phase 2
customers_clean = customers_data.copy()
orders_clean = orders_data.copy()
products_clean = products_data.copy()

# Remove exact duplicates
customers_clean.drop_duplicates(inplace=True)
orders_clean.drop_duplicates(inplace=True)
products_clean.drop_duplicates(inplace=True)'''
    },
    {
        "chapter": "Phase 2 (Step 2): Demographic & Text Validation",
        "text": "BUSINESS STRATEGY:\nCustomer records contained impossible ages (like -5 or 150) and invalid phone numbers/emails. We enforced business rules: Ages must be 18-100, and phones exactly 11 digits. Invalid demographics were set to NaN. We imputed missing ages with the robust median (42), but correctly left unique identifiers (phones, emails) as NaN to avoid corrupting records.",
        "code": '''# Age Validation and Imputation
invalid_ages = (customers_clean['age'] < 18) | (customers_clean['age'] > 100)
customers_clean.loc[invalid_ages, 'age'] = pd.NA
age_median = customers_clean['age'].median()
customers_clean['age'] = customers_clean['age'].fillna(age_median)

# Phone Number Validation (Regex)
invalid_phones = ~customers_clean['phone'].str.match(r'^\\d{11}$', na=False)
customers_clean.loc[invalid_phones, 'phone'] = pd.NA'''
    },
    {
        "chapter": "Phase 2 (Step 3): Handling Financial Anomalies",
        "text": "BUSINESS STRATEGY:\nWe found impossible financial metrics: negative shipping costs and discounts exceeding 100%. We replaced these with the 'median', a statistical measure robust against extreme outliers. Crucially, we investigated missing prices and costs, proving they were unrecoverable, and scientifically decided to keep them as NaN.",
        "code": '''# Fixing Impossible Discounts (Valid range: 0-100)
invalid_discounts = (orders_clean["discount"] < 0) | (orders_clean["discount"] > 100)
orders_clean.loc[invalid_discounts, "discount"] = pd.NA

discount_median = orders_clean["discount"].median()
orders_clean["discount"] = orders_clean["discount"].fillna(discount_median)

# Fixing Negative Shipping Costs
invalid_shipping = orders_clean["shipping_cost"] < 0
orders_clean.loc[invalid_shipping, "shipping_cost"] = pd.NA
orders_clean["shipping_cost"] = orders_clean["shipping_cost"].fillna(orders_clean["shipping_cost"].median())'''
    },
    {
        "chapter": "Phase 3: Painting the Picture (Visualizations)",
        "text": "BUSINESS STRATEGY:\nWith our data clean, we needed to understand the business visually. We plotted customer distributions across cities and identified top revenue-generating products. Why? Because an ML model finds mathematical patterns, but humans need visual context to know if those patterns actually make business sense.",
        "code": '''import matplotlib.pyplot as plt
import seaborn as sns

# Visualizing Top Revenue Generating Products
plt.figure(figsize=(10,5))
sns.barplot(
    x=top_revenue_products.values,
    y=top_revenue_products.index,
    hue=top_revenue_products.index,
    palette="viridis",
    legend=False
)
plt.title("Top 10 Revenue Generating Products")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.show()'''
    },
    {
        "chapter": "Phase 4: Advanced Feature Engineering (ABC Analysis)",
        "text": "BUSINESS STRATEGY:\nFinally, we implemented ABC Analysis, classifying our inventory into Class A, Class B, and Class C based on cumulative revenue. We also segmented products by Movement Speed. These are brilliant features for Machine Learning: they allow predictive models to prioritize high-value and fast-moving items.",
        "code": '''# ABC Analysis Logic
products_features = products_features.sort_values(by="total_revenue", ascending=False)
total_company_rev = products_features["total_revenue"].sum()

products_features["cumulative_revenue_percent"] = (
    products_features["total_revenue"].cumsum() / total_company_rev
) * 100

def abc_class(percent):
    if percent <= 80: return "A"
    elif percent <= 95: return "B"
    else: return "C"

products_features["ABC_Class"] = products_features["cumulative_revenue_percent"].apply(abc_class)'''
    }
]

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'Data Science to Machine Learning: The Interactive Logbook', 0, 1, 'C')
        self.set_draw_color(150, 150, 150)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(220, 235, 255)
        self.set_text_color(0, 50, 100)
        self.cell(0, 10, f' {title}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_text(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 6, text)
        self.ln(4)
        
    def chapter_code(self, code):
        self.set_font('courier', '', 9.5)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(20, 100, 20) # Dark green for code to make it pop
        # Replace tabs with spaces
        code = code.replace('\\t', '    ')
        self.multi_cell(0, 5, code, fill=True)
        self.ln(8)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Intro
pdf.set_font('helvetica', 'I', 11)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 6, "Welcome to your Interactive Logbook. This document maps your exact Jupyter Notebook cells into a cohesive narrative. It pairs the Python Code you wrote directly with the Business Strategy (the 'Why') behind it. By reading the strategy and viewing the corresponding code side-by-side, you will be fully prepared to explain your data pipeline to any Machine Learning engineer or Business Stakeholder.")
pdf.ln(8)

for section in book_content:
    pdf.chapter_title(section["chapter"])
    pdf.chapter_text(section["text"])
    pdf.chapter_code(section["code"])
    
pdf.output('report/Data_Science_Interactive_Storybook.pdf')
print("Interactive PDF created successfully!")
