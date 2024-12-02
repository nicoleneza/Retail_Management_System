import csv
import random  # Import for generating random values
from faker import Faker
from datetime import datetime, timedelta
from tabulate import tabulate

# Initialize Faker instance
fake = Faker()

# Specify the number of records to generate
num_customers = 5000

# Generate dataset
customers = [
    {
        "Customer ID": f"CUST-{i + 1:04d}",
        "Customer Name": fake.name(),
        "Customer Address": fake.country(),
        "Email": fake.email(),
        "Phone": fake.phone_number()
    }
    for i in range(num_customers)
]

# Save customers to CSV
customers_file = "customers.csv"
with open(customers_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Customer ID", "Customer Name", "Customer Address", "Email", "Phone"]
    )
    writer.writeheader()
    writer.writerows(customers)

# print(tabulate(data, headers="keys", tablefmt="grid"))
print(f"Dataset with {num_customers} records saved to {customers_file}.")
