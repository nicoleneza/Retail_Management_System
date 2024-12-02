import pandas as pd
import psycopg2
from datetime import datetime

# Database connection setup
conn = psycopg2.connect(
    dbname="retail",
    user="postgres",
    password="nicolebbb",
    host="localhost",
    port="5434"
)
cursor = conn.cursor()

try:
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_analytics (
            id SERIAL PRIMARY KEY,
            invoice_number VARCHAR(20),
            customer_name VARCHAR(100),
            customer_address VARCHAR(100),
            total_amount DECIMAL(10,2),
            date DATE,
            payment_method VARCHAR(20),
            daily_sales DECIMAL(10,2),
            daily_revenue DECIMAL(10,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR(20) PRIMARY KEY,
            customer_name VARCHAR(100),
            customer_address VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(50)
        )
    """)
    conn.commit()

    # Read the CSV file
    df = pd.read_csv('dataset1.csv')
    customers_df = pd.read_csv('customers.csv')
    
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate daily metrics
    daily_metrics = df.groupby('Date').agg({
        'Invoice Number': 'count',  # Count of sales per day
        'Total Amount': 'sum'      # Sum of revenue per day
    }).reset_index()
    
    daily_metrics.columns = ['date', 'daily_sales', 'daily_revenue']
    
    for index, row in customers_df.iterrows():
        cursor.execute(
            """
            INSERT INTO customers (
                customer_id,
                customer_name,
                customer_address,
                email,
                phone
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
            """,
            (
                row['Customer ID'],
                row['Customer Name'],
                row['Customer Address'],
                row['Email'],
                row['Phone']
            )
        )
    # Insert data
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO sales_analytics (
                invoice_number,
                customer_name,
                customer_address,
                total_amount,
                date,
                payment_method
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                row['Invoice Number'],
                row['Customer Name'],
                row['Customer Address'],
                row['Total Amount'],
                row['Date'],
                row['Payment Method']
            )
        )

    conn.commit()
    print("Data successfully inserted into the database.")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    cursor.close()
    conn.close()