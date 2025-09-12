#!/usr/bin/env python3
"""
Migration script to add new columns to existing database tables
"""
import sys
import os
from sqlalchemy import create_engine, text

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def migrate_database():
    # Create engine
    engine = create_engine("sqlite:///app/rail.db")
    
    with engine.connect() as conn:
        try:
            # Add new columns to train_schedules table
            print("Adding new columns to train_schedules table...")
            
            # Check if columns exist before adding them
            result = conn.execute(text("PRAGMA table_info(train_schedules)"))
            existing_columns = [row[1] for row in result.fetchall()]
            
            new_columns = [
                ("actual_arrival", "DATETIME"),
                ("actual_departure", "DATETIME"),
                ("actual_platform", "TEXT"),
                ("status", "TEXT"),
                ("delay_minutes", "INTEGER")
            ]
            
            for column_name, column_type in new_columns:
                if column_name not in existing_columns:
                    print(f"Adding column: {column_name}")
                    conn.execute(text(f"ALTER TABLE train_schedules ADD COLUMN {column_name} {column_type}"))
                else:
                    print(f"Column {column_name} already exists")
            
            # Create train_logs table if it doesn't exist
            print("Creating train_logs table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS train_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    train_id TEXT NOT NULL,
                    station_id TEXT NOT NULL,
                    section_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    planned_time DATETIME,
                    actual_time DATETIME,
                    delay_minutes INTEGER DEFAULT 0,
                    status TEXT,
                    platform TEXT,
                    notes TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (train_id) REFERENCES trains (id),
                    FOREIGN KEY (station_id) REFERENCES stations (id)
                )
            """))
            
            # Create indexes
            print("Creating indexes...")
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_train_logs_train_id ON train_logs (train_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_train_logs_station_id ON train_logs (station_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_train_logs_section_id ON train_logs (section_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_train_logs_event_type ON train_logs (event_type)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_train_logs_timestamp ON train_logs (timestamp)"))
            
            conn.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"Migration failed: {e}")
            raise

if __name__ == "__main__":
    migrate_database()
