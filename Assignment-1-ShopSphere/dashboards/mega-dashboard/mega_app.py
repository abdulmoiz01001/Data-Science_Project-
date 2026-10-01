import streamlit as st
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="ShopSphere AI Super App", layout="wide")

# Cached Data Loaders
@st.cache_resource
def load_sales_model():
    model = xgb.XGBRegressor()
    model.load_model('xgboost_sales_model.json')
    return model

@st.cache_resource
def load_churn_model():
    model = xgb.XGBClassifier()
    model.load_model('xgboost_churn_model.json')
    return model

@st.cache_resource
def load_clv_model():
    model = xgb.XGBRegressor()
    model.load_model('xgboost_clv_model.json')
    return model

@st.cache_data
def load_data_for_recs():
    data_dir = r"D:\University\Artificial Intellignece Learning\Core Python Learning\weak 2 learning\Assignment-1-ShopSphere\output\cleaned_data"
    orders = pd.read_csv(f"{data_dir}\\orders_clean.csv")
    products = pd.read_csv(f"{data_dir}\\products_clean.csv")
    df = orders.merge(products[['product_id', 'product_name']], on='product_id', how='left')
    customer_item_matrix = df.pivot_table(index='customer_id', columns='product_name', values='quantity', aggfunc='sum', fill_value=0)
    customer_item_matrix = (customer_item_matrix > 0).astype(int)
    item_similarity = cosine_similarity(customer_item_matrix.T)
    item_sim_df = pd.DataFrame(item_similarity, index=customer_item_matrix.columns, columns=customer_item_matrix.columns)
    return item_sim_df

# Sidebar Navigation
st.sidebar.title("🧠 AI Super App")
st.sidebar.markdown("Navigate between models:")
page = st.sidebar.radio("Select Tool", ["Sales Forecasting", "Customer Churn", "CLV Prediction", "Product Recommendations"])

if page == "Sales Forecasting":
    st.title("📈 Sales Forecaster")
    st.write("Predict future sales based on business logic.")
    
    model = load_sales_model()
    
    col1, col2 = st.columns(2)
    with col1:
        lag_1 = st.number_input("Yesterday's Sales (PKR)", min_value=0, value=150000)
        lag_7 = st.number_input("Last Week's Sales (PKR)", min_value=0, value=140000)
        rolling_7 = st.number_input("7-Day Average Sales (PKR)", min_value=0, value=145000)
        day = st.slider("Day of the Month", 1, 31, 15)
    with col2:
        is_weekend = st.selectbox("Is Weekend?", [0, 1])
        is_payday = st.selectbox("Is Salary Day (1-5)?", [0, 1])
        is_festival = st.selectbox("Is Festival/Eid?", [0, 1])
        is_promo = st.selectbox("Is Marketing Promo Active?", [0, 1])
        month = st.slider("Month", 1, 12, 8)
    
    if st.button("Forecast Sales"):
        input_data = pd.DataFrame([[day, month, 2024, 3, is_weekend, lag_1, lag_7, rolling_7, is_payday, is_festival, is_promo]], 
                                  columns=['Day', 'Month', 'Year', 'DayOfWeek', 'Is_Weekend', 'Lag_1', 'Lag_7', 'Rolling_Mean_7', 'Is_Payday', 'Is_Festival', 'Is_Promo_Day'])
        prediction = model.predict(input_data)[0]
        st.success(f"🎯 Expected Daily Revenue: **PKR {prediction:,.2f}**")

elif page == "Customer Churn":
    st.title("🏃 Customer Churn Prediction")
    st.write("Will this customer leave the platform?")
    
    model = load_churn_model()
    
    col1, col2 = st.columns(2)
    with col1:
        total_orders = st.number_input("Total Lifetime Orders", min_value=1, value=5)
        total_spent = st.number_input("Total Lifetime Spent (PKR)", min_value=100, value=15000)
        age = st.number_input("Age", min_value=12, max_value=90, value=25)
    with col2:
        gender = st.selectbox("Gender Code (0=Female, 1=Male)", [0, 1])
        city = st.selectbox("City Code", [0, 1, 2, 3, 4], index=2)
        
    if st.button("Predict Churn Risk"):
        input_data = pd.DataFrame([[total_orders, total_spent, city, gender, age]], 
                                  columns=['Total_Orders', 'Total_Spent', 'city', 'gender', 'age'])
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            st.error("🚨 HIGH RISK: Customer is likely to churn!")
        else:
            st.success("✅ SAFE: Customer is active and loyal.")

elif page == "CLV Prediction":
    st.title("💎 Customer Lifetime Value (CLV)")
    st.write("Predict lifetime spend based on the FIRST order.")
    
    model = load_clv_model()
    
    col1, col2 = st.columns(2)
    with col1:
        first_order_val = st.number_input("First Order Value (PKR)", min_value=100, value=3000)
        age = st.number_input("Age", min_value=12, max_value=90, value=28)
    with col2:
        gender = st.selectbox("Gender Code (0=Female, 1=Male)", [0, 1])
        city = st.selectbox("City Code", [0, 1, 2, 3, 4])
        
    if st.button("Predict Lifetime Value"):
        input_data = pd.DataFrame([[city, gender, age, first_order_val]], 
                                  columns=['city', 'gender', 'age', 'First_Order_Value'])
        prediction = model.predict(input_data)[0]
        st.success(f"💰 Expected Lifetime Revenue from this customer: **PKR {prediction:,.2f}**")

elif page == "Product Recommendations":
    st.title("🛒 AI Recommendation Engine")
    st.write("Amazon-style 'Frequently Bought Together' system.")
    
    with st.spinner("Loading product matrix..."):
        item_sim_df = load_data_for_recs()
        
    product_list = item_sim_df.columns.tolist()
    selected_product = st.selectbox("Select a Product to view recommendations:", product_list)
    
    if st.button("Get Recommendations"):
        similar_items = item_sim_df[selected_product].sort_values(ascending=False).drop(selected_product).head(3)
        st.write(f"### People who bought '{selected_product}' also bought:")
        for i, (item, score) in enumerate(similar_items.items(), 1):
            match_pc = score * 100
            if match_pc > 0:
                st.info(f"**{i}. {item}** (Match: {match_pc:.1f}%)")
            else:
                st.warning(f"**{i}. {item}** (No strong match history)")
