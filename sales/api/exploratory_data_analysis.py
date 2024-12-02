import requests
import pandas as pd

try:
    # Fetch sales data from the API with timeout
    sales_api = requests.get('http://127.0.0.1:8000/api/summary/', timeout=60)
    # sales_api2 = requests.get('http://127.0.0.1:8000/api/summary/?limit=0', timeout=60)
    sales_api.raise_for_status()
    sales_api_data = sales_api.json()
    # sales_api2_data = sales_api2.json()
    
    print("Sales API Response:", sales_api_data.keys())
    sdf = pd.DataFrame(sales_api_data if isinstance(sales_api_data, list) else sales_api_data.get('sales', []))
    sdf = sdf.rename(columns={'customer': 'Customer Name'})
    sdf2 = pd.read_csv("sales_save.csv").drop(columns=["bad_id"])
    print("sales api data shaper", sdf.shape, sdf.head())
    
    # Fetch customers data
    customers_api = requests.get('http://127.0.0.1:8000/api/customers/')
    # customers_api2 = requests.get('http://127.0.0.1:8000/api/customers/?limit=30')
    customers_api.raise_for_status()
    customers_api_data = customers_api.json()
    # customers_api2_data = customers_api2.json()
    cdf = pd.DataFrame(customers_api_data if isinstance(customers_api_data, list) else customers_api_data.get('results', []))
    cdf2 = pd.read_csv("customer_save.csv").drop(columns=["bad_id"])
    print("customer api data shaper", cdf.shape)
    
    print("Sales DataFrame Columns:", sdf.columns.tolist())
    print("Customers DataFrame Columns:", cdf.columns.tolist())

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
    exit()

try:
    # Standardize customer names
    sdf['Customer Name'] = sdf['Customer Name'].str.strip().str.lower()
    cdf['Customer Name'] = cdf['Customer Name'].str.strip().str.lower()

    # Deduplicate the customer data
    cdf = cdf.drop_duplicates(subset=['Customer Name'])
    # Standardize customer names
    sdf2['Customer Name'] = sdf2['Customer Name'].str.strip().str.lower()
    cdf2['Customer Name'] = cdf2['Customer Name'].str.strip().str.lower()

    # Deduplicate the customer data
    cdf2 = cdf2.drop_duplicates(subset=['Customer Name'])
    # Deduplicate the customer data
    cdf = cdf.drop_duplicates(subset=['Customer Name'])
    print("customer bug shape, small shape", cdf.shape, cdf2.shape)
    # Merge sales and customer data
    merged_df_big = pd.merge(
        sdf,
        cdf,
        how='inner',
        on='Customer Name',
        suffixes=('_sales', '_customers')
    )
    merged_df_small = pd.merge(
        sdf2,
        cdf2,
        how='inner',
        on='Customer Name',
        suffixes=('_sales', '_customers')
    )
    merged_df = pd.concat([merged_df_big, merged_df_big])

    # Prepare the limited dataframes for concatenation
    # mdf1 = pd.DataFrame(sales_api2_data if isinstance(sales_api2_data, list) else sales_api2_data.get('results', []))
    # mdf2 = pd.DataFrame(customers_api2_data if isinstance(customers_api2_data, list) else customers_api2_data.get('results', []))

    # # Concatenate full and limited data
    # merged_df2 = pd.concat(mdf1, mdf2)

    # output_file2 = "merged_sales_customers_concat.csv"
    # merged_df2.to_csv(output_file2, index=False)
    # print(f"\nMerged dataset saved to {output_file2}")

    # Reset index to remove duplicate issues
    merged_df = merged_df.reset_index(drop=True)
    
    # Handle missing values
    print("Missing values before handling:")
    print(merged_df.isnull().sum())
    fill_values = {
        'Customer Name': pd.NA,
        'Customer Address': pd.NA,
        'Total Amount': 0,
        'Date': pd.Timestamp.now().date(),
        'Payment Method': pd.NA,
        'sales': 0,
        'revenue': 0
    }
    merged_df.fillna(fill_values, inplace=True)

    # Save the merged DataFrame
    output_file = "merged_sales_customers.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\nMerged dataset saved to {output_file}")

    # Add descriptive statistics
    print("\nDataset Shape:")
    print(merged_df.shape)

    print("\nDataset Description:")
    print(merged_df.describe())

except Exception as e:
    print(f"Error processing data: {e}")
    exit()

try:
    # Remove duplicates for feature engineering
    merged_df = merged_df.loc[~merged_df.duplicated()]

    # Create new features
    merged_df['Total Sales'] = merged_df.groupby('Customer Name')['Total Amount'].transform('sum')
    merged_df['Transaction Count'] = merged_df.groupby('Customer Name')['Total Amount'].transform('count')
    merged_df['Average Transaction Value'] = merged_df['Total Sales'] / merged_df['Transaction Count']
    merged_df['Customer Tenure'] = (pd.to_datetime('today') - pd.to_datetime(merged_df['Date'])).dt.days

    # Payment Method Frequency
    try:
        payment_frequency = (
            merged_df.groupby(['Customer Name', 'Payment Method'])
            .size()
            .reset_index(name='Frequency')
        )
        # Merge the frequency data back to the main DataFrame
        merged_df = pd.merge(
            merged_df,
            payment_frequency,
            on=['Customer Name', 'Payment Method'],
            how='left'
        )
        print("Payment Method Frequency added successfully.")

    except Exception as e:
        print(f"Error adding Payment Method Frequency: {e}")

    # Customer Segmentation
    def segment_customer(row):
        if row['Total Sales'] > 1000:
            return 'High Value'
        elif row['Total Sales'] > 500:
            return 'Medium Value'
        else:
            return 'Low Value'

    merged_df['Customer Segment'] = merged_df.apply(segment_customer, axis=1)
    print("Feature creation successful!")

    # Save the updated DataFrame
    updated_file = "updated_sales_customers.csv"
    merged_df.to_csv(updated_file, index=False)
    print(f"\nUpdated dataset saved to {updated_file}")

except Exception as e:
    print(f"Error processing new features: {e}")
    exit()
