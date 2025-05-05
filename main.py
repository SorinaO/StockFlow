import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

# Sample stock data for testing purposes
stock_data = {
    'Product': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat'],
    'Stock Level': [50, 200, 30, 100, 75],
    'Min Stock Level': [40, 100, 20, 50, 60],
    'Location': ['A1', 'B2', 'C3', 'D4', 'E5']
}

# Initialize session state for stock and stock history
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(stock_data)

if 'stock_history' not in st.session_state:
    st.session_state.stock_history = []  # Store stock movement logs

if 'quantity_reset_counter' not in st.session_state:  # Initialize reset counter
    st.session_state.quantity_reset_counter = 0


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


# Function to Stock Requirement Forecast
def stock_requirement_forecast():
    st.subheader("Stock Requirement Forecast")
    forecast_period = st.slider("Select forecast period (days)", min_value=1, max_value=30, value=7)

    forecasted_df = st.session_state.df.copy()
    forecasted_df['Forecasted Stock Level'] = (
            forecasted_df['Stock Level'] - (forecasted_df['Stock Level'] * 0.1 * forecast_period)
    ).clip(lower=0)  # Ensure stock level never goes negative

    st.dataframe(forecasted_df[['Product', 'Stock Level', 'Forecasted Stock Level']])


# Function to log stock movements (Inbound, Outbound, Adjustments), including discrepancies
def log_stock_movement():
    st.subheader("Log Stock Movement")

    # Ensure session state has stock history initialized
    if 'stock_history' not in st.session_state:
        st.session_state.stock_history = []

        # Select product and movement type
    movement_product = st.selectbox("Select Product", st.session_state.df['Product'])
    movement_type = st.selectbox("Select Movement Type",
                                 ['Restocking', 'Returned Goods', 'Stock Adjustment', 'Sales',
                                  'Damaged', 'Discrepancy', 'Transfer'])

    #  Display current stock level
    current_stock = st.session_state.df.loc[st.session_state.df['Product'] == movement_product, 'Stock Level'].values[0]
    st.info(f"Current Stock Level: {current_stock}")

    quantity_key = f"quantity_input_{st.session_state.quantity_reset_counter}"  # Unique key for quantity field
    movement_quantity = st.number_input(f"Enter Quantity for {movement_type}", min_value=1, value=1, key=quantity_key)

    reason = None

    # Handle discrepancy-specific input
    if movement_type == 'Discrepancy':
        reason = st.selectbox("Select Discrepancy Reason", ['Missing Items', 'Miscount', 'Slot Adjustment'])

    # Disable button if quantity is invalid
    button_label = f"Log {movement_type}"
    log_button = st.button(button_label, disabled=(
        movement_quantity > current_stock if movement_type in ['Sales', 'Damaged', 'Transfer'] else False))

    if log_button:
        # Adjust stock levels based on movement type
        if movement_type in ['Restocking', 'Returned Goods', 'Stock Adjustment']:
            st.session_state.df.loc[
                st.session_state.df['Product'] == movement_product, 'Stock Level'] += movement_quantity
            reason = "New Stock Arrival" if movement_type == "Restocking" else movement_type

        elif movement_type in ['Sales', 'Damaged', 'Transfer']:
            if movement_quantity > current_stock:
                st.error(f"Cannot process {movement_type}: Not enough stock available!")
                return
            st.session_state.df.loc[
                st.session_state.df['Product'] == movement_product, 'Stock Level'] -= movement_quantity
            reason = movement_type

        elif movement_type == 'Discrepancy':
            st.session_state.df.loc[
                st.session_state.df['Product'] == movement_product, 'Stock Level'] -= movement_quantity
            reason = reason  # Already selected in the dropdown

        # Append the stock movement to history
        st.session_state.stock_history.append(
            {"Product": movement_product,
             "Quantity Change": movement_quantity if movement_type in ['Restocking', 'Returned Goods',
                                                                       'Stock Adjustment'] else -movement_quantity,
             "Reason": reason, "Movement Type": movement_type}
        )

        st.success(f"Logged {movement_type} for {movement_product}: {movement_quantity} units")
        st.session_state.quantity_reset_counter += 1  # Increment counter to reset quantity field
        time.sleep(2)
        st.rerun()


# Function to display stock movement history
def display_stock_movement_history():
    st.subheader("Stock Movement History")

    history_df = pd.DataFrame(st.session_state.stock_history,
                              columns=['Product', 'Quantity Change', 'Reason', 'Movement Type'])

    if not history_df.empty:
        # Add a filter dropdown for movement type
        movement_filter = st.selectbox("Filter by Movement Type", ["All"] + list(history_df["Movement Type"].unique()))

        # Apply filter
        if movement_filter != "All":
            history_df = history_df[history_df["Movement Type"] == movement_filter]

    st.dataframe(history_df)


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


# Main code
def main():
    st.title("Stock & System Dashboard")
    display_current_stock_overview()
    display_low_stock_alerts()
    log_stock_movement()
    display_stock_movement_history()
    stock_requirement_forecast()
    plot_stock_trends()


# Run the main function
if __name__ == "__main__":
    main()