# StockFlow

StockFlow is a Streamlit-based web application designed to help you manage and monitor your warehouse stock levels. It provides features for displaying current stock levels, alerting you when stock is low, forecasting future stock requirements, logging stock movements, and visualizing stock trends.

## Features

- **Current Stock Overview**: Displays the current stock levels for all products.
- **Low Stock Alerts**: Alerts you when stock levels fall below the minimum threshold.
- **Forecast Future Stock Requirements**: Predicts future stock levels based on a user-defined forecast period.
- **Log Stock Movements**: Allows you to log various stock movements such as restocking, sales, and discrepancies.
- **Stock Movement History**: Displays a history of all logged stock movements with filtering options.
- **Stock Level Trends**: Visualizes stock level trends over time.
Project Structure
main.py: The main script containing the Streamlit app code.
requirements.txt: A file listing the required Python packages.


How It Works
Current Stock Overview
Displays the current stock levels for all products, including product name, stock level, minimum stock level, and location.

Low Stock Alerts
Alerts you when stock levels fall below the minimum threshold. Provides a warning message for each product that needs restocking.

Forecast Future Stock Requirements
Allows you to select a forecast period (in days) using a slider. Predicts future stock levels based on a simple linear model that assumes a constant rate of stock depletion.

Log Stock Movements
Enables you to log various stock movements such as restocking, sales, and discrepancies. Adjusts stock levels accordingly and records the movement in the stock history.

Stock Movement History
Displays a history of all logged stock movements. Includes filtering options to view specific types of movements.

Stock Level Trends
Visualizes stock level trends over time using a line chart. Helps you understand stock usage patterns and make better forecasting decisions.

Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Requirements:
Streamlit
Pandas
Matplotlib
NumPy