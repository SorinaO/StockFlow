import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample stock data for testing purposes
stock_data = {
    'Product': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat'],
    'Stock Level': [50, 200, 30, 100, 75],
    'Min Stock Level': [40, 100, 20, 50, 60],
    'Location': ['A1', 'B2', 'C3', 'D4', 'E5']
}

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(stock_data)

# Function to display the current stock overview
def display_current_stock_overview():
    st.subheader("Current Stock Overview")
    st.dataframe(st.session_state.df[['Product', 'Stock Level', 'Min Stock Level', 'Location']])

# Function to display low stock alerts
def display_low_stock_alerts():
    low_stock_df = st.session_state.df[st.session_state.df['Stock Level'] < st.session_state.df['Min Stock Level']]
    st.subheader("Stock Replenishment Alerts")
    st.dataframe(low_stock_df)
    
    st.subheader("Low Stock Alerts")
    for index, row in low_stock_df.iterrows():
        st.warning(f"Product {row['Product']} is below the minimum stock level!")

# Function to plot stock trends
def plot_stock_trends():
    st.subheader("Stock Level Trends")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.df['Product'], st.session_state.df['Stock Level'], marker='o', label='Stock Level')
    ax.set_xlabel('Product')
    ax.set_ylabel('Stock Level')
    ax.set_title('Stock Level Trend')
    ax.legend()
    st.pyplot(fig)

# Function to forecast future stock requirements
def forecast_stock_requirements():
    st.subheader("Forecast Future Stock Requirements")
    forecast_period = st.slider("Select forecast period (days)", min_value=1, max_value=30, value=7)
    
    forecasted_df = st.session_state.df.copy()
    forecasted_df['Forecasted Stock Level'] = (forecasted_df['Stock Level'] - 
                                               (forecasted_df['Stock Level'] // 10 * forecast_period)).clip(lower=0)
    
    st.dataframe(forecasted_df[['Product', 'Stock Level', 'Forecasted Stock Level']])

# Function to log stock discrepancies
def log_stock_discrepancy():
    st.subheader("Log Stock Discrepancy")
    discrepancy_product = st.selectbox("Select Product with Discrepancy", st.session_state.df['Product'])
    discrepancy_quantity = st.number_input("Enter Discrepancy Quantity", min_value=0)
    if st.button('Log Discrepancy'):
        st.session_state.df.loc[st.session_state.df['Product'] == discrepancy_product, 'Stock Level'] -= discrepancy_quantity
        st.write(f"Logged discrepancy for {discrepancy_product}: {discrepancy_quantity} units")
        st.rerun()

# Main code
def main():
    st.title("Stock & System Dashboard")
    display_current_stock_overview()
    display_low_stock_alerts()
    plot_stock_trends()
    log_stock_discrepancy()
    forecast_stock_requirements()

# Run the main function
if __name__ == "__main__":
    main()
