#!/usr/bin/env python3
"""
Test script to add recent timeline data for testing
"""
import sys
import os
from datetime import datetime, timedelta, timezone
import random

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from db.session import get_db
from db.models import TrainLog

def add_recent_timeline_data():
    db = next(get_db())
    
    try:
        # Clear existing logs
        db.query(TrainLog).delete()
        
        # Create recent timeline data (last 2 hours)
        now = datetime.now(timezone.utc)
        trains = ['T001', 'T002', 'T003', 'T004', 'T005']
        stations = ['ST001', 'ST002', 'ST003', 'ST004', 'ST005']
        
        logs = []
        
        for train_id in trains:
            # Create a journey for each train
            base_time = now - timedelta(hours=1, minutes=random.randint(0, 30))
            
            for i, station_id in enumerate(stations):
                # Arrival event
                planned_arrival = base_time + timedelta(minutes=i*30)
                actual_arrival = planned_arrival + timedelta(minutes=random.randint(0, 10))
                delay = int((actual_arrival - planned_arrival).total_seconds() / 60)
                
                arrival_log = TrainLog(
                    train_id=train_id,
                    station_id=station_id,
                    section_id=f"S{i+1}",
                    event_type="arrival",
                    planned_time=planned_arrival,
                    actual_time=actual_arrival,
                    delay_minutes=delay,
                    status="arrived",
                    platform=f"P{i+1}",
                    notes=f"Arrived at {station_id}",
                    timestamp=actual_arrival
                )
                logs.append(arrival_log)
                
                # Departure event (5 minutes after arrival)
                planned_departure = planned_arrival + timedelta(minutes=5)
                actual_departure = actual_arrival + timedelta(minutes=5 + random.randint(0, 5))
                delay_dep = int((actual_departure - planned_departure).total_seconds() / 60)
                
                departure_log = TrainLog(
                    train_id=train_id,
                    station_id=station_id,
                    section_id=f"S{i+1}",
                    event_type="departure",
                    planned_time=planned_departure,
                    actual_time=actual_departure,
                    delay_minutes=delay_dep,
                    status="departed",
                    platform=f"P{i+1}",
                    notes=f"Departed from {station_id}",
                    timestamp=actual_departure
                )
                logs.append(departure_log)
        
        # Add all logs to database
        for log in logs:
            db.add(log)
        
        db.commit()
        print(f"✅ Added {len(logs)} timeline events for testing")
        print(f"Time range: {(now - timedelta(hours=1)).strftime('%H:%M')} - {now.strftime('%H:%M')}")
        
        # Show sample data
        sample_logs = db.query(TrainLog).filter(TrainLog.train_id == 'T001').order_by(TrainLog.timestamp).limit(4).all()
        print("\nSample T001 events:")
        for log in sample_logs:
            print(f"  {log.event_type} at {log.station_id}: {log.planned_time.strftime('%H:%M')} -> {log.actual_time.strftime('%H:%M')} ({log.delay_minutes}min delay)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_recent_timeline_data()
