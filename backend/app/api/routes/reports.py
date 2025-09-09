from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from .users import require_role
from app.db.session import get_db
from app.db.models import TrainPosition, TrainSchedule, Train

router = APIRouter(dependencies=[Depends(require_role("controller", "admin"))])


@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)) -> dict:
	# Minimal placeholder KPIs derived from counts
	positions_count = db.query(TrainPosition).count()
	schedules_count = db.query(TrainSchedule).count()
	return {
		"throughput_per_hour": positions_count % 50,
		"avg_delay_minutes": 3.5,
		"congestion_index": 0.42,
		"on_time_percentage": 92.1,
		"positions_count": positions_count,
		"schedules_count": schedules_count,
	}


@router.get("/delay_trends")
def delay_trends(hours: int = Query(24, ge=1, le=168), db: Session = Depends(get_db)) -> dict:
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    # We don't have explicit delay; approximate trend using average speed drop proxy per hour
    # Compute avg speed per hour bucket; convert to a pseudo delay index (higher -> more delay)
    hour_buckets = (
        db.query(
            func.strftime('%Y-%m-%d %H:00', TrainPosition.timestamp).label('bucket'),
            func.avg(TrainPosition.speed_kmph).label('avg_speed'),
            func.count().label('cnt'),
        )
        .filter(TrainPosition.timestamp >= start)
        .group_by('bucket')
        .order_by('bucket')
        .all()
    )
    # Build continuous buckets across the window
    labels: list[str] = []
    series: list[float] = []
    bucket_to_speed = {b.bucket: (b.avg_speed or 0.0) for b in hour_buckets}
    # Normalize to a delay index: slower speed -> higher delay; scale 0-10
    speeds = [v for v in bucket_to_speed.values() if v is not None]
    max_speed = max(speeds) if speeds else 1.0
    t = start.replace(minute=0, second=0, microsecond=0)
    while t <= now:
        key = t.strftime('%Y-%m-%d %H:00')
        avg_speed = bucket_to_speed.get(key, 0.0)
        delay_index = round(10.0 * (1.0 - (avg_speed / max_speed if max_speed else 1.0)), 2)
        labels.append(t.strftime('%H:%M'))
        series.append(delay_index)
        t += timedelta(hours=1)
    return {"labels": labels, "series": series}


@router.get("/throughput")
def throughput(hours: int = Query(24, ge=1, le=168), db: Session = Depends(get_db)) -> dict:
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    # Throughput by train class based on position events in window
    rows = (
        db.query(Train.class_type, func.count(TrainPosition.id))
        .join(Train, Train.id == TrainPosition.train_id, isouter=True)
        .filter(TrainPosition.timestamp >= start)
        .group_by(Train.class_type)
        .all()
    )
    data = []
    for class_type, cnt in rows:
        label = class_type or 'Unknown'
        data.append({"label": label, "value": int(cnt)})
    # Fallback if no data
    if not data:
        data = [
            {"label": "Express", "value": 100},
            {"label": "Freight", "value": 80},
            {"label": "Local", "value": 90},
        ]
    return {"data": data}


@router.get("/hotspots")
def hotspots(hours: int = Query(24, ge=1, le=168), top_sections: int = Query(4, ge=1, le=12), buckets: int = Query(5, ge=2, le=24), db: Session = Depends(get_db)) -> dict:
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    # Determine top sections by activity in window
    section_counts = (
        db.query(TrainPosition.section_id, func.count(TrainPosition.id).label('cnt'))
        .filter(TrainPosition.timestamp >= start)
        .group_by(TrainPosition.section_id)
        .order_by(func.count(TrainPosition.id).desc())
        .limit(top_sections)
        .all()
    )
    y_labels = [row.section_id for row in section_counts] or ["S1", "S2", "S3", "S4"]
    # Time buckets within window
    bucket_duration = hours / buckets
    x_labels: list[str] = []
    bucket_starts: list[datetime] = []
    t = start
    for i in range(buckets):
        bucket_starts.append(t)
        x_labels.append(t.strftime('%H:%M'))
        t += timedelta(hours=bucket_duration)
    x_labels[-1] = now.strftime('%H:%M')

    # Initialize matrix
    data_matrix: list[list[int]] = [[0 for _ in range(buckets)] for _ in range(len(y_labels))]

    # For each section and bucket, count events
    for s_idx, section in enumerate(y_labels):
        for b_idx in range(buckets):
            b_start = bucket_starts[b_idx]
            b_end = bucket_starts[b_idx + 1] if b_idx + 1 < buckets else now
            cnt = (
                db.query(func.count(TrainPosition.id))
                .filter(TrainPosition.section_id == section)
                .filter(TrainPosition.timestamp >= b_start)
                .filter(TrainPosition.timestamp < b_end)
                .scalar()
            )
            data_matrix[s_idx][b_idx] = int(cnt or 0)

    # Fallback demo grid if no data
    if all(all(v == 0 for v in row) for row in data_matrix):
        x_labels = ['A', 'B', 'C', 'D', 'E'][:buckets]
        y_labels = ['S1', 'S2', 'S3', 'S4'][:top_sections]
        data_matrix = [
            [1, 2, 3, 2, 4][:buckets],
            [2, 3, 5, 1, 2][:buckets],
            [0, 1, 2, 3, 1][:buckets],
            [3, 4, 2, 5, 4][:buckets],
        ][:top_sections]

    return {"xLabels": x_labels, "yLabels": y_labels, "data": data_matrix}

