from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Literal


from .users import require_role

router = APIRouter(dependencies=[Depends(require_role("controller", "admin"))])


class Disruption(BaseModel):
	type: Literal["delay", "track_block", "platform_issue", "rolling_stock", "signal_failure"]
	description: Optional[str] = None
	start_ts: float
	duration_seconds: int
	section_id: Optional[str] = None
	station_id: Optional[str] = None
	severity: Literal["low", "medium", "high"] = "medium"


class Scenario(BaseModel):
	name: str
	disruptions: List[Disruption]


class TimelineEvent(BaseModel):
	timestamp: float
	event: str
	impact: str


class TrainImpact(BaseModel):
	train_id: str
	delay_minutes: int
	status: Literal["on_time", "delayed", "cancelled"]


class Predictions(BaseModel):
	timeline: List[TimelineEvent]
	train_impacts: List[TrainImpact]


class Metrics(BaseModel):
	total_delay_minutes: float
	missed_connections: int
	platform_conflicts: int
	throughput_impact_percent: float
	passenger_delay_hours: float


class SimulationResult(BaseModel):
	id: str
	impacted_trains: List[str]
	metrics: Metrics
	predictions: Predictions


class ApplyRequest(BaseModel):
	simulation_id: str


class ApplyResponse(BaseModel):
	success: bool
	message: str


@router.post("/run", response_model=SimulationResult)
def run_simulation(scenario: Scenario) -> SimulationResult:
	from app.services.simulator import simulator_service

	res = simulator_service.run(scenario.model_dump())
	return SimulationResult(**res)


@router.post("/apply", response_model=ApplyResponse)
def apply_simulation_to_real(request: ApplyRequest) -> ApplyResponse:
	from app.services.simulator import simulator_service

	res = simulator_service.apply_to_real(request.simulation_id)
	return ApplyResponse(**res)


