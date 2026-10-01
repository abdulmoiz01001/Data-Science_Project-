import streamlit as st                                                                                            
import xgboost as xgb                                                                                                     
import pandas as pd                                                                                               
                                                                                                                  
# Page Design Setup                                                                                               
st.set_page_config(page_title="ShopSphere AI Forecast", layout="centered")                                        
                                                                                                                  
st.title("📈 ShopSphere AI Sales Forecaster")                                                                     
st.write("Machine Learning (XGBoost) ka istemaal karte hue aaj ki sales predict karein.")                         
                                                                                                                  
# 1. Model Load karein                                                                                            
@st.cache_resource                                                                                                
def load_model():                                                                                                 
    model = xgb.XGBRegressor()
    model.load_model('xgboost_sales_model.json')
    return model                                                                 
                                                                                                                  
model = load_model()                                                                                              
                                                                                                                  
# 2. User se Input lenge (Website ke Side panel mein)                                                             
st.sidebar.header("📊 Input Sales Data")                                                                          
st.sidebar.write("Pichli history darj karein:")                                                                   
                                                                                                                  
lag_1 = st.sidebar.number_input("Kal ki Sales (PKR)", min_value=0, value=150000)                                  
lag_7 = st.sidebar.number_input("Pichle Hafte same din ki Sales (PKR)", min_value=0, value=140000)                
rolling_7 = st.sidebar.number_input("Pichle 7 Din ki Average Sales", min_value=0, value=145000)                   
                                                                                                                  
st.sidebar.markdown("---")                                                                                        
is_weekend = st.sidebar.selectbox("Kya aaj Weekend hai?", [0, 1])                                                 
is_payday = st.sidebar.selectbox("Kya aaj Salary Day (1-5 date) hai?", [0, 1])                                    
is_festival = st.sidebar.selectbox("Kya aaj koi Tehwaar (Eid/Sale) hai?", [0, 1])                                 
is_promo = st.sidebar.selectbox("Kya aaj Marketing Campaign chal rahi hai?", [0, 1])                              
                                                                                                                  
# Basic dates                                                                                                     
day = st.sidebar.slider("Aaj ki Tareekh (Day)", 1, 31, 15)                                                        
month = st.sidebar.slider("Mahina (Month)", 1, 12, 8)                                                             
year = 2024                                                                                                       
dayofweek = 3 # Dummy value                                                                                       
                                                                                                                  
# 3. Prediction Button                                                                                            
if st.button("🚀 Forecast Sales"):                                                                                
    # Data ko wese hi arrange karein jese XGBoost train hua tha                                                   
    input_data = pd.DataFrame([[day, month, year, dayofweek, is_weekend, lag_1, lag_7, rolling_7, is_payday, is_festival, is_promo]],                                                                                            
                              columns=['Day', 'Month', 'Year', 'DayOfWeek', 'Is_Weekend', 'Lag_1', 'Lag_7',  'Rolling_Mean_7', 'Is_Payday', 'Is_Festival', 'Is_Promo_Day'])                                                      
                                                                                                                  
    # Model se prediction lena                                                                                    
    prediction = model.predict(input_data)[0]                                                                     
                                                                                                                  
    st.success(f"🎯 Expected Daily Revenue: **PKR {prediction:,.2f}**")                                           
    st.balloons() # Thori si animation!