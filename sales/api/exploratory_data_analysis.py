import requests
import pandas as pd

try:
    # Fetch sales data from the API with timeout
    sales_api = requests.get('http://127.0.0.1:8000/api/summary/', timeout=60)
    sales_api.raise_for_status()
    sales_api_data = sales_api.json()
    
    print("Sales API Response:", sales_api_data.keys())
    sdf = pd.DataFrame(sales_api_data if isinstance(sales_api_data, list) else sales_api_data.get('sales', []))
    sdf = sdf.rename(columns={'customer': 'Customer Name'})

    # Fetch customers data
    customers_api = requests.get('http://127.0.0.1:8000/api/customers/')
    customers_api.raise_for_status()
    customers_api_data = customers_api.json()
    cdf = pd.DataFrame(customers_api_data if isinstance(customers_api_data, list) else customers_api_data.get('results', []))
    
    print("Sales DataFrame Columns:", sdf.columns.tolist())
    print("Customers DataFrame Columns:", cdf.columns.tolist())

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
    exit()

try:
    # Standardize customer names by stripping spaces and converting to lowercase
    sdf['Customer Name'] = sdf['Customer Name'].str.strip().str.lower()
    cdf['Customer Name'] = cdf['Customer Name'].str.strip().str.lower()

    # Print unique customer names for debugging
    print("\nUnique customers in sales data:", sdf['Customer Name'].unique())
    print("\nUnique customers in customer data:", cdf['Customer Name'].unique())

    # Deduplicate the customer data if needed
    cdf = cdf.drop_duplicates(subset=['Customer Name'])

    # Merge with a left join to keep all sales records
    merged_df = pd.merge(
        sdf, 
        cdf, 
        how='left',  # Keep all sales records
        on='Customer Name',  # Use standardized customer names
        validate='m:1'  # Many-to-one relationship validation
    )

    # Check for any rows that did not find a match
    unmatched_rows = merged_df[merged_df['Customer Name'].isnull()]
    print("\nUnmatched sales records:", unmatched_rows)

    # Print some diagnostic information
    print("\nUnique customers in sales data:", sdf['Customer Name'].nunique())
    print("Unique customers in customer data:", cdf['Customer Name'].nunique())
    print("Unique customers in merged data:", merged_df['Customer Name'].nunique())

    # Check for missing values
    print("Missing values before handling:")
    print(merged_df.isnull().sum())

    fill_values = {
    'Customer Name': 'Unknown Customer',
    'Customer Address': 'Unknown Address',
    'Total Amount': 0,
    'Date': pd.Timestamp.now().date(),
    'Payment Method': 'Unknown',
    'sales': 0,
    'revenue': 0,
    'Email': 'unknown@email.com',
    'Phone': 'N/A'
}

    merged_df.fillna(fill_values, inplace=True)

    # Example: Fill missing values for 'Customer Name' with 'Unknown' and 'Sales Amount' with 0
    

    # Rest of your data processing code...
    print("Shape of the Merged DataFrame:", merged_df.shape)
    print("\nDataset Description:\n", merged_df.describe())
    
    # Save the merged DataFrame to a CSV file
    output_file = "merged_sales_customers.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\nMerged dataset saved to {output_file}")


except Exception as e:
    print(f"Error processing data: {e}")
    exit()

try:
    # After merging the DataFrames
    # Create new features
    merged_df['Total Sales'] = merged_df.groupby('Customer Name')['Total Amount'].transform('sum')
    merged_df['Transaction Count'] = merged_df.groupby('Customer Name')['Total Amount'].transform('count')
    merged_df['Average Transaction Value'] = merged_df['Total Sales'] / merged_df['Transaction Count']
    merged_df['Customer Tenure'] = (pd.to_datetime('today') - pd.to_datetime(merged_df['Date'])).dt.days

    # Payment Method Frequency
    merged_df['Payment Method Frequency'] = merged_df.groupby('Customer Name')['Payment Method'].transform(lambda x: x.value_counts().get(x, 0))

    # Customer Segmentation
    def segment_customer(row):
        if row['Total Sales'] > 1000:
            return 'High Value'
        elif row['Total Sales'] > 500:
            return 'Medium Value'
        else:
            return 'Low Value'
    
    merged_df['Customer Segment'] = merged_df.apply(segment_customer, axis=1)


except Exception as e:
    print(f"Error processing data: {e}")
    exit()
