# check_db_data.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select

# We need to import the settings and models from your application
from config import settings
from app.models import RunLog, DetectionEventLog, Base

# Use the exact same database URL as your main application
DATABASE_URL = settings.DATABASE.URL

# Set up the database connection
engine = create_async_engine(DATABASE_URL)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def check_data():
    """
    Connects to the database and prints the contents of the RunLog
    and DetectionEventLog tables.
    """
    print(f"--- Connecting to database: {DATABASE_URL} ---")
    
    async with AsyncSessionFactory() as session:
        # Check the RunLog table
        print("\n--- Checking 'run_logs' Table ---")
        run_log_query = select(RunLog).order_by(RunLog.start_timestamp.desc())
        run_log_result = await session.execute(run_log_query)
        all_runs = run_log_result.scalars().all()

        if not all_runs:
            print("RESULT: The 'run_logs' table is EMPTY.")
        else:
            print(f"RESULT: Found {len(all_runs)} records in 'run_logs' table:")
            for run in all_runs:
                print(
                    f"  - ID: {run.id}, "
                    f"Batch: {run.batch_code}, "
                    f"Status: {run.status.name}, "
                    f"Start: {run.start_timestamp.isoformat()}, "
                    f"End: {run.end_timestamp.isoformat() if run.end_timestamp else 'N/A'}"
                )

        # Check the DetectionEventLog table
        print("\n--- Checking 'detection_event_logs' Table ---")
        detection_log_query = select(DetectionEventLog).order_by(DetectionEventLog.timestamp.desc())
        detection_log_result = await session.execute(detection_log_query)
        all_detections = detection_log_result.scalars().all()

        if not all_detections:
            print("RESULT: The 'detection_event_logs' table is EMPTY.")
        else:
            print(f"RESULT: Found {len(all_detections)} records in 'detection_event_logs' table:")
            for detection in all_detections:
                print(
                    f"  - ID: {detection.id}, "
                    f"Run ID: {detection.run_log_id}, "
                    f"Timestamp: {detection.timestamp.isoformat()}, "
                    f"Image: {detection.image_path}"
                )

    await engine.dispose()
    print("\n--- Check complete ---")

if __name__ == "__main__":
    asyncio.run(check_data())