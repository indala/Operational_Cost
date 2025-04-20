from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL
DATABASE_URL = "postgresql://operational_cost_db_user:KdSlsqJHDE1QJNG1S4wXdzQTDA3bdEfG@dpg-cvn7mffgi27c73bi8ar0-a.oregon-postgres.render.com/operational_cost_db"

# Create engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Base class for models
Base = declarative_base()

# Function to get table description and data
def get_table_description():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)
    for table in tables:
        print(f"\nDescription of table '{table}':")
        columns = inspector.get_columns(table)
        for column in columns:
            print(column)

# Function to drop all tables in the database
def drop_all_tables():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("All tables have been dropped.")

# Call the function to drop all tables
drop_all_tables()
