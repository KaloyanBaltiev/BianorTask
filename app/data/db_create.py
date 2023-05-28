from sqlalchemy import create_engine
import pandas as pd

def ingest_csv_to_postgres(csv_file, table_name):
    df = pd.read_csv(csv_file)

    # hack!
    # for now just set the necessary columns for easier queries
    if table_name == 'customer':
        df['birthdate'] = pd.to_datetime(df['birthdate'], format='%Y-%m-%d')
    if table_name == 'sales_receipts':
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%Y-%m-%d')

    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


# Define the PostgreSQL database connection details
database_url = 'postgresql+psycopg2://postgres:1234@127.0.0.1:5432/maria_database'
engine = create_engine(database_url)

# Ingest data from CSV files into PostgreSQL tables
data_mappings = {
    'app/data/product.csv': 'product',
    'app/data/customer.csv': 'customer',
    'app/data/sales_receipts.csv': 'sales_receipts'
}

for csv_file, table_name in data_mappings.items():
    ingest_csv_to_postgres(csv_file, table_name)

# Close the database connection
engine.dispose()
