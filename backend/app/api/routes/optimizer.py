from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


from .users import require_role

router = APIRouter(dependencies=[Depends(require_role("controller", "admin"))])


class OptimizeRequest(BaseModel):
	section_id: str
	lookahead_minutes: int = 30
	objectives: List[str] = ["throughput", "delay_min"]
	constraints: Dict[str, Any] = {}


class Recommendation(BaseModel):
	train_id: str
	action: str
	reason: str
	eta_change_seconds: Optional[int] = None
	platform: Optional[str] = None
	priority_score: Optional[float] = None


class OptimizeResponse(BaseModel):
	recommendations: List[Recommendation]
	explanations: List[str] = []
	latency_ms: int


@router.post("/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest) -> OptimizeResponse:
	from app.services.optimizer import optimizer_service

	result = optimizer_service.optimize(req.model_dump())
	recs = [
		Recommendation(
			train_id=r.get("train_id", ""),
			action=r.get("action", ""),
			reason=r.get("reason", ""),
			eta_change_seconds=r.get("eta_change_seconds"),
			platform=r.get("platform"),
			priority_score=r.get("priority_score"),
		)
		for r in result.get("recommendations", [])
	]
	return OptimizeResponse(
		recommendations=recs,
		explanations=result.get("explanations", []),
		latency_ms=5,
	)


