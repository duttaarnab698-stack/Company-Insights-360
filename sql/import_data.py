import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pathlib import Path


# ==============================
# MySQL Configuration
# ==============================

username = "root"
password = "Arnab@2005"

host = "localhost"
port = 3306
database = "Company_Insights_360"


# ==============================
# Project Paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent

csv_path = BASE_DIR.parent / "data" / "company_data_cleaned.csv"

print("CSV path:")
print(csv_path)


# ==============================
# Create MySQL Connection
# ==============================

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(connection_url)

print("Connected to MySQL successfully!")


# ==============================
# Check CSV
# ==============================

if not csv_path.exists():
    print("ERROR: CSV file not found!")
    print("Expected location:", csv_path)
    exit()


# ==============================
# Load CSV
# ==============================

df = pd.read_csv(csv_path)

# Clean column names
df.columns = df.columns.str.strip()

# Rename CampaignSchema column if required
if "CampaignSchema_" in df.columns:
    df.rename(
        columns={"CampaignSchema_": "CampaignSchema"},
        inplace=True
    )

print("CSV loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())


# ==============================
# Check MySQL Table Before Import
# ==============================

with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM company_data")
    )

    existing_rows = result.scalar()

    print("\nExisting rows in MySQL:", existing_rows)


# ==============================
# Import Data
# ==============================

df.to_sql(
    name="company_data",
    con=engine,
    if_exists="append",
    index=False
)

print("\nData imported into MySQL successfully!")


# ==============================
# Verify Data
# ==============================

with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM company_data")
    )

    total_rows = result.scalar()

    print("Total rows in MySQL:", total_rows)


# ==============================
# Final Check
# ==============================

if total_rows == 2000:
    print("\nSUCCESS: All 2000 rows imported successfully!")
else:
    print("\nWARNING: Expected 2000 rows, but found", total_rows)