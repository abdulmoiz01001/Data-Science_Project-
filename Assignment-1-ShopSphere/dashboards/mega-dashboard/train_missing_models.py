import pandas as pd
import xgboost as xgb
import os

print("Starting training process...")

# Paths
data_dir = r"D:\University\Artificial Intellignece Learning\Core Python Learning\weak 2 learning\Assignment-1-ShopSphere\output\cleaned_data"
orders = pd.read_csv(f"{data_dir}\\orders_clean.csv")
customers = pd.read_csv(f"{data_dir}\\customers_clean.csv")
products = pd.read_csv(f"{data_dir}\\products_clean.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders_merged = orders.merge(products[['product_id', 'price']], on="product_id", how="left")
orders_merged["price"] = orders_merged["price"].fillna(orders_merged["price"].median())
orders_merged["revenue"] = (orders_merged["price"] * orders_merged["quantity"]) * (1 - orders_merged["discount"]/100)

current_date = orders_merged['order_date'].max()

# CHURN MODEL
print("Training Churn Model...")
rfm = orders_merged.groupby('customer_id').agg(
    Last_Order_Date=('order_date', 'max'), Total_Orders=('order_id', 'nunique'), Total_Spent=('revenue', 'sum')
).reset_index()
rfm['Recency_Days'] = (current_date - rfm['Last_Order_Date']).dt.days
rfm['Is_Churned'] = rfm['Recency_Days'].apply(lambda x: 1 if x > 180 else 0)
cust_features = rfm.merge(customers[['customer_id', 'city', 'gender', 'age']], on='customer_id', how='left')
cust_features['gender'] = cust_features['gender'].astype('category').cat.codes
cust_features['city'] = cust_features['city'].astype('category').cat.codes
cust_features['age'] = cust_features['age'].fillna(cust_features['age'].median())

X_churn = cust_features[['Total_Orders', 'Total_Spent', 'city', 'gender', 'age']]
y_churn = cust_features['Is_Churned']

model_churn = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
model_churn.fit(X_churn, y_churn)
model_churn.save_model("xgboost_churn_model.json")
print("Churn Model Saved!")

# CLV MODEL
print("Training CLV Model...")
orders_sorted = orders_merged.sort_values(['customer_id', 'order_date'])
first_orders = orders_sorted.drop_duplicates(subset=['customer_id'], keep='first')[['customer_id', 'revenue']].rename(columns={'revenue': 'First_Order_Value'})
total_spent = orders_merged.groupby('customer_id')['revenue'].sum().reset_index().rename(columns={'revenue': 'Total_Lifetime_Value'})
clv_data = customers[['customer_id', 'city', 'gender', 'age']].merge(first_orders, on='customer_id', how='left').merge(total_spent, on='customer_id', how='left').dropna()
clv_data['gender'] = clv_data['gender'].astype('category').cat.codes
clv_data['city'] = clv_data['city'].astype('category').cat.codes

X_clv = clv_data[['city', 'gender', 'age', 'First_Order_Value']]
y_clv = clv_data['Total_Lifetime_Value']
model_clv = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
model_clv.fit(X_clv, y_clv)
model_clv.save_model("xgboost_clv_model.json")
print("CLV Model Saved!")
print("Done.")
