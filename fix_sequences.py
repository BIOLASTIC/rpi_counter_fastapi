# fix_sequences.py (Corrected and Final Version)
import sys
from sqlalchemy import create_engine, text

# --- Configuration ---
POSTGRES_DB_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/rpi_counter_db"

TABLES_TO_SYNC = [
    "operators", "products", "camera_profiles", "object_profiles",
    "configurations", "run_logs", "detection_event_logs", "event_logs"
]

def sync_sequences():
    print("--- Starting PostgreSQL Sequence Synchronization ---")

    try:
        engine = create_engine(POSTGRES_DB_URL)
        with engine.connect() as connection:
            transaction = connection.begin()
            for table_name in TABLES_TO_SYNC:
                sequence_name = f"{table_name}_id_seq"
                print(f"Syncing sequence for table: '{table_name}'...")

                # Corrected query to find the max ID and set the sequence.
                # COALESCE handles cases where a table might be empty.
                sql_query = text(f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX(id) FROM {table_name}), 1), false);")

                try:
                    connection.execute(sql_query)
                    # To verify, get the current value
                    result = connection.execute(text(f"SELECT last_value FROM {sequence_name};"))
                    last_val = result.scalar_one()
                    print(f"  -> Success. Sequence '{sequence_name}' is now set to {last_val}. The next inserted ID will be {last_val + 1}.")
                except Exception as e:
                    print(f"  -> WARNING: Could not sync sequence '{sequence_name}'. Does it exist? Error: {e}")

            transaction.commit() # Save all changes

    except Exception as e:
        print(f"\nCRITICAL ERROR: Failed to connect or execute. Is PostgreSQL running? Error: {e}", file=sys.stderr)
        return

    print("\n--- Sequence Synchronization Complete! ---")


if __name__ == "__main__":
    sync_sequences()