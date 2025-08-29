# migrate_db.py (Corrected)
import pandas as pd
from sqlalchemy import create_engine, text
import json

# --- Configuration ---
SQLITE_DB_PATH = "data/box_counter.db"
SQLITE_DB_URL = f"sqlite:///{SQLITE_DB_PATH}"

POSTGRES_DB_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/rpi_counter_db"

TABLES_TO_MIGRATE = [
    "operators", "products", "camera_profiles", "object_profiles",
    "configurations", "run_logs", "detection_event_logs", "event_logs"
]

def safe_json_dumps(d):
    """
    Safely converts a Python dict to a JSON string.
    Handles None or non-dict values gracefully.
    """
    if isinstance(d, dict):
        return json.dumps(d)
    # If it's already a valid JSON string (or None), return as is.
    # Otherwise, return None to avoid insertion errors.
    if isinstance(d, str) or d is None:
        return d
    return None

def migrate_data():
    print("--- Starting Database Migration ---")

    sqlite_engine = create_engine(SQLITE_DB_URL)
    postgres_engine = create_engine(POSTGRES_DB_URL)

    try:
        with postgres_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("  -> PostgreSQL connection successful.")
    except Exception as e:
        print(f"  -> CRITICAL ERROR: Could not connect to PostgreSQL. Is the Docker container running? Error: {e}")
        return

    for table_name in TABLES_TO_MIGRATE:
        print(f"Migrating table: '{table_name}'...")
        try:
            df = pd.read_sql_table(table_name, sqlite_engine)
            print(f"  -> Found {len(df)} rows to migrate.")

            # --- THIS IS THE FIX ---
            # Check if this table has a known JSON column that needs conversion.
            json_column = None
            if table_name == 'run_logs':
                json_column = 'object_profile_snapshot'
            elif table_name in ['detection_event_logs', 'event_logs']:
                json_column = 'details'

            if json_column and json_column in df.columns:
                print(f"  -> Converting '{json_column}' column from Python dicts to JSON strings...")
                df[json_column] = df[json_column].apply(safe_json_dumps)
            # --- END OF FIX ---

            if not df.empty:
                df.to_sql(
                    name=table_name,
                    con=postgres_engine,
                    if_exists='append',
                    index=False
                )
                print(f"  -> Successfully migrated {len(df)} rows to PostgreSQL.")
            else:
                print("  -> Table is empty, nothing to migrate.")

        except Exception as e:
            print(f"  -> ERROR migrating table '{table_name}': {e}")
            print("  -> Halting migration. Please resolve the issue and try again.")
            return

    print("--- Database Migration Complete! ---")


if __name__ == "__main__":
    print(f"This script will migrate data from '{SQLITE_DB_PATH}' to the PostgreSQL server.")
    confirm = input("Are you sure you want to proceed? (yes/no): ")
    if confirm.lower() == 'yes':
        migrate_data()
    else:
        print("Migration cancelled by user.")