import csv
import random  # Import for generating random values
from faker import Faker
from datetime import datetime, timedelta
from tabulate import tabulate

# Initialize Faker instance
fake = Faker()

# Specify the number of records to generate
num_records = 500000

# Generate dataset
data = [
    {
        "Invoice Number": f"INV-{fake.date_this_year(before_today=True, after_today=False).year}-{i + 1:05d}",
        "Customer Name": fake.name(),
        "Customer Address": fake.country(),
        "Total Amount": fake.random_int(min=100, max=100000),
        "Date": (fake.date_between(start_date="-60d", end_date="today")).strftime("%Y-%m-%d"),
        "Payment Method": random.choice(['cash', 'card', 'mobile'])
    }
    for i in range(num_records)
]
output_file = "dataset1.csv"
# Save to CSV file
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Invoice Number", "Customer Name", "Customer Address", "Total Amount", "Date", "Payment Method"]
    )
    writer.writeheader()
    writer.writerows(data)



# print(tabulate(data, headers="keys", tablefmt="grid"))
# print(f"Dataset with {num_records} records saved to {output_file}.")
