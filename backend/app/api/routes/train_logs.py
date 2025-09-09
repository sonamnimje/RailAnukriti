from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from .users import require_role
from app.db.session import get_db
from app.db.models import TrainLog, TrainSchedule, Train, Station

# Temporarily remove authentication for testing
# router = APIRouter(dependencies=[Depends(require_role("controller", "admin"))])
router = APIRouter()


@router.get("/logs")
def get_train_logs(
    train_id: Optional[str] = Query(None, description="Filter by train ID"),
    section_id: Optional[str] = Query(None, description="Filter by section ID"),
    station_id: Optional[str] = Query(None, description="Filter by station ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    hours: int = Query(24, ge=1, le=168, description="Hours to look back"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> dict:
    """Get train logs with filtering options"""
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=hours)
    
    query = db.query(TrainLog).filter(TrainLog.timestamp >= start_time)
    
    if train_id:
        query = query.filter(TrainLog.train_id.ilike(f"%{train_id}%"))
    if section_id:
        query = query.filter(TrainLog.section_id.ilike(f"%{section_id}%"))
    if station_id:
        query = query.filter(TrainLog.station_id.ilike(f"%{station_id}%"))
    if event_type:
        query = query.filter(TrainLog.event_type == event_type)
    
    logs = query.order_by(TrainLog.timestamp.desc()).limit(limit).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "train_id": log.train_id,
                "station_id": log.station_id,
                "section_id": log.section_id,
                "event_type": log.event_type,
                "planned_time": log.planned_time.isoformat() if log.planned_time else None,
                "actual_time": log.actual_time.isoformat() if log.actual_time else None,
                "delay_minutes": log.delay_minutes,
                "status": log.status,
                "platform": log.platform,
                "notes": log.notes,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ],
        "total": len(logs)
    }


@router.get("/schedules")
def get_train_schedules(
    train_id: Optional[str] = Query(None, description="Filter by train ID"),
    station_id: Optional[str] = Query(None, description="Filter by station ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    hours: int = Query(24, ge=1, le=168, description="Hours to look back"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> dict:
    """Get train schedules with actual vs planned times"""
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=hours)
    
    query = db.query(TrainSchedule).filter(
        or_(
            TrainSchedule.planned_arrival >= start_time,
            TrainSchedule.actual_arrival >= start_time
        )
    )
    
    if train_id:
        query = query.filter(TrainSchedule.train_id.ilike(f"%{train_id}%"))
    if station_id:
        query = query.filter(TrainSchedule.station_id.ilike(f"%{station_id}%"))
    if status:
        query = query.filter(TrainSchedule.status == status)
    
    schedules = query.order_by(TrainSchedule.planned_arrival.desc()).limit(limit).all()
    
    return {
        "schedules": [
            {
                "id": schedule.id,
                "train_id": schedule.train_id,
                "station_id": schedule.station_id,
                "planned_arrival": schedule.planned_arrival.isoformat() if schedule.planned_arrival else None,
                "actual_arrival": schedule.actual_arrival.isoformat() if schedule.actual_arrival else None,
                "planned_departure": schedule.planned_departure.isoformat() if schedule.planned_departure else None,
                "actual_departure": schedule.actual_departure.isoformat() if schedule.actual_departure else None,
                "planned_platform": schedule.planned_platform,
                "actual_platform": schedule.actual_platform,
                "status": schedule.status,
                "delay_minutes": schedule.delay_minutes
            }
            for schedule in schedules
        ],
        "total": len(schedules)
    }


@router.get("/timeline")
def get_timeline_data(
    train_id: Optional[str] = Query(None, description="Filter by train ID"),
    section_id: Optional[str] = Query(None, description="Filter by section ID"),
    hours: int = Query(12, ge=1, le=168, description="Hours to look back"),
    db: Session = Depends(get_db)
) -> dict:
    """Get timeline data for Gantt-style visualization"""
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=hours)
    
    # Get train movements with planned vs actual times
    query = db.query(
        TrainLog.train_id,
        TrainLog.station_id,
        TrainLog.section_id,
        TrainLog.event_type,
        TrainLog.planned_time,
        TrainLog.actual_time,
        TrainLog.delay_minutes,
        TrainLog.status,
        TrainLog.platform
    ).filter(
        TrainLog.timestamp >= start_time
    )
    
    if train_id:
        query = query.filter(TrainLog.train_id.ilike(f"%{train_id}%"))
    if section_id:
        query = query.filter(TrainLog.section_id.ilike(f"%{section_id}%"))
    
    movements = query.order_by(TrainLog.train_id, TrainLog.timestamp).all()
    
    # Group by train for timeline visualization
    timeline_data = {}
    for movement in movements:
        train_id = movement.train_id
        if train_id not in timeline_data:
            timeline_data[train_id] = []
        
        timeline_data[train_id].append({
            "station_id": movement.station_id,
            "section_id": movement.section_id,
            "event_type": movement.event_type,
            "planned_time": movement.planned_time.isoformat() if movement.planned_time else None,
            "actual_time": movement.actual_time.isoformat() if movement.actual_time else None,
            "delay_minutes": movement.delay_minutes,
            "status": movement.status,
            "platform": movement.platform
        })
    
    return {
        "timeline": timeline_data,
        "time_range": {
            "start": start_time.isoformat(),
            "end": now.isoformat()
        }
    }


@router.get("/stats")
def get_log_stats(
    hours: int = Query(24, ge=1, le=168, description="Hours to look back"),
    db: Session = Depends(get_db)
) -> dict:
    """Get statistics about train logs and schedules"""
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=hours)
    
    # Total logs in time period
    total_logs = db.query(func.count(TrainLog.id)).filter(
        TrainLog.timestamp >= start_time
    ).scalar()
    
    # Delayed trains
    delayed_trains = db.query(func.count(func.distinct(TrainLog.train_id))).filter(
        and_(
            TrainLog.timestamp >= start_time,
            TrainLog.delay_minutes > 0
        )
    ).scalar()
    
    # Average delay
    avg_delay = db.query(func.avg(TrainLog.delay_minutes)).filter(
        and_(
            TrainLog.timestamp >= start_time,
            TrainLog.delay_minutes > 0
        )
    ).scalar()
    
    # On-time percentage
    total_schedules = db.query(func.count(TrainSchedule.id)).filter(
        or_(
            TrainSchedule.planned_arrival >= start_time,
            TrainSchedule.actual_arrival >= start_time
        )
    ).scalar()
    
    on_time_schedules = db.query(func.count(TrainSchedule.id)).filter(
        and_(
            or_(
                TrainSchedule.planned_arrival >= start_time,
                TrainSchedule.actual_arrival >= start_time
            ),
            or_(
                TrainSchedule.delay_minutes == 0,
                TrainSchedule.delay_minutes.is_(None)
            )
        )
    ).scalar()
    
    on_time_percentage = (on_time_schedules / total_schedules * 100) if total_schedules > 0 else 0
    
    return {
        "total_logs": total_logs or 0,
        "delayed_trains": delayed_trains or 0,
        "average_delay_minutes": round(avg_delay or 0, 1),
        "on_time_percentage": round(on_time_percentage, 1),
        "total_schedules": total_schedules or 0
    }
