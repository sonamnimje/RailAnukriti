from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone


from .users import require_role
from app.db.session import get_db
from app.db.models import TrainPosition as TrainPositionModel, TrainSchedule as TrainScheduleModel

router = APIRouter()


class TrainPosition(BaseModel):
	id: str
	section_id: str
	planned_block_id: Optional[str] = None
	actual_block_id: Optional[str] = None
	location_km: float = Field(..., ge=0)
	speed_kmph: float = Field(..., ge=0)
	timestamp: float


class TrainScheduleEvent(BaseModel):
	train_id: str
	station_id: str
	planned_arrival_ts: float
	planned_departure_ts: float
	platform: Optional[str] = None


class IngestBatch(BaseModel):
	positions: List[TrainPosition] = []
	schedules: List[TrainScheduleEvent] = []


@router.post("/positions")
def ingest_positions(batch: List[TrainPosition], db: Session = Depends(get_db)) -> dict:
	rows = []
	for p in batch:
		rows.append(
			TrainPositionModel(
				train_id=p.id,
				section_id=p.section_id,
				planned_block_id=p.planned_block_id,
				actual_block_id=p.actual_block_id,
				location_km=p.location_km,
				speed_kmph=p.speed_kmph,
			)
		)
	for r in rows:
		db.add(r)
	db.commit()
	return {"received": len(batch)}


@router.post("/schedules")
def ingest_schedules(batch: List[TrainScheduleEvent], db: Session = Depends(get_db)) -> dict:
	for e in batch:
		row = TrainScheduleModel(
			train_id=e.train_id,
			station_id=e.station_id,
			planned_arrival=datetime.fromtimestamp(e.planned_arrival_ts, tz=timezone.utc),
			planned_departure=datetime.fromtimestamp(e.planned_departure_ts, tz=timezone.utc),
			planned_platform=e.platform,
		)
		db.add(row)
	db.commit()
	return {"received": len(batch)}


@router.get("/positions")
def get_positions(db: Session = Depends(get_db), user = Depends(require_role("controller", "admin"))) -> List[dict]:
	rows = db.query(TrainPositionModel).order_by(TrainPositionModel.timestamp.desc()).limit(200).all()
	return [
		{
			"train_id": r.train_id,
			"section_id": r.section_id,
			"planned_block_id": r.planned_block_id,
			"actual_block_id": r.actual_block_id,
			"location_km": r.location_km,
			"speed_kmph": r.speed_kmph,
			"timestamp": r.timestamp.timestamp(),
		}
		for r in rows
	]


@router.get("/schedules")
def get_schedules(db: Session = Depends(get_db)) -> List[dict]:
	rows = db.query(TrainScheduleModel).order_by(TrainScheduleModel.id.desc()).limit(500).all()
	return [
		{
			"id": r.id,
			"train_id": r.train_id,
			"station_id": r.station_id,
			"planned_arrival_ts": r.planned_arrival.timestamp() if r.planned_arrival else None,
			"planned_departure_ts": r.planned_departure.timestamp() if r.planned_departure else None,
			"platform": r.planned_platform,
		}
		for r in rows
	]


@router.post("/batch")
def ingest_batch(batch: IngestBatch) -> dict:
	return {
		"positions_received": len(batch.positions),
		"schedules_received": len(batch.schedules),
	}


