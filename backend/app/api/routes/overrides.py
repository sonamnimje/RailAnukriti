from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import uuid4


from .users import require_role
from app.db.session import get_db
from app.db.models import Override

router = APIRouter(dependencies=[Depends(require_role("controller", "admin"))])


class OverrideRequest(BaseModel):
	controller_id: str
	train_id: str
	action: str
	ai_action: Optional[str] = None
	reason: Optional[str] = None
	timestamp: float


class OverrideRecord(OverrideRequest):
	id: str


@router.post("/apply", response_model=OverrideRecord)
def apply_override(req: OverrideRequest, db: Session = Depends(get_db)) -> OverrideRecord:
	ovr_id = f"ovr-{uuid4().hex[:8]}"
	row = Override(
		id=ovr_id,
		controller_id=req.controller_id,
		train_id=req.train_id,
		action=req.action,
		ai_action=req.ai_action,
		reason=req.reason,
	)
	db.add(row)
	db.commit()
	return OverrideRecord(id=ovr_id, **req.dict())


@router.get("/logs", response_model=List[OverrideRecord])
def list_overrides(db: Session = Depends(get_db)) -> List[OverrideRecord]:
	rows = db.query(Override).order_by(Override.timestamp.desc()).limit(200).all()
	result: List[OverrideRecord] = []
	for r in rows:
		result.append(
			OverrideRecord(
				id=r.id,
				controller_id=r.controller_id,
				train_id=r.train_id,
				action=r.action,
				ai_action=r.ai_action,
				reason=r.reason,
				timestamp=r.timestamp.timestamp(),
			)
		)
	return result


