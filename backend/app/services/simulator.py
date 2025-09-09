from dataclasses import dataclass
from typing import Dict, Any, List
import random
import time
from datetime import datetime, timedelta


@dataclass
class SimulatorConfig:
	max_horizon_minutes: int = 120


class SimulatorService:
	def __init__(self, config: SimulatorConfig | None = None) -> None:
		self.config = config or SimulatorConfig()
		self.simulation_counter = 0

	def run(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
		"""Run a digital twin simulation with realistic disruption modeling"""
		self.simulation_counter += 1
		simulation_id = f"sim-{self.simulation_counter:03d}"
		
		# Extract scenario data
		scenario_name = scenario.get("name", "Custom Scenario")
		disruptions = scenario.get("disruptions", [])
		
		# Simulate train impacts based on disruptions
		impacted_trains = self._simulate_train_impacts(disruptions)
		
		# Calculate comprehensive metrics
		metrics = self._calculate_metrics(disruptions, impacted_trains)
		
		# Generate prediction timeline
		predictions = self._generate_predictions(disruptions, impacted_trains)
		
		return {
			"id": simulation_id,
			"impacted_trains": impacted_trains,
			"metrics": metrics,
			"predictions": predictions
		}

	def _simulate_train_impacts(self, disruptions: List[Dict[str, Any]]) -> List[str]:
		"""Simulate which trains are impacted by disruptions"""
		impacted_trains = []
		
		# Mock train data - in real implementation, this would come from database
		all_trains = [
			"T001-Local", "T002-Express", "T003-Freight", "T004-Local", 
			"T005-Express", "T006-Freight", "T007-Local", "T008-Express"
		]
		
		for disruption in disruptions:
			disruption_type = disruption.get("type", "delay")
			severity = disruption.get("severity", "medium")
			section_id = disruption.get("section_id", "SEC-001")
			
			# Determine impact based on disruption type and severity
			if disruption_type == "track_block":
				# Track blocks affect all trains in the section
				impacted_trains.extend([t for t in all_trains if t not in impacted_trains])
			elif disruption_type == "delay":
				# Delays affect 2-4 trains depending on severity
				num_affected = {"low": 2, "medium": 3, "high": 4}[severity]
				affected = random.sample(all_trains, min(num_affected, len(all_trains)))
				impacted_trains.extend([t for t in affected if t not in impacted_trains])
			elif disruption_type == "platform_issue":
				# Platform issues affect 1-2 trains
				num_affected = {"low": 1, "medium": 1, "high": 2}[severity]
				affected = random.sample(all_trains, min(num_affected, len(all_trains)))
				impacted_trains.extend([t for t in affected if t not in impacted_trains])
			elif disruption_type == "rolling_stock":
				# Rolling stock issues affect specific trains
				affected = random.sample(all_trains, min(2, len(all_trains)))
				impacted_trains.extend([t for t in affected if t not in impacted_trains])
			elif disruption_type == "signal_failure":
				# Signal failures affect multiple trains in the area
				affected = random.sample(all_trains, min(3, len(all_trains)))
				impacted_trains.extend([t for t in affected if t not in impacted_trains])
		
		return list(set(impacted_trains))  # Remove duplicates

	def _calculate_metrics(self, disruptions: List[Dict[str, Any]], impacted_trains: List[str]) -> Dict[str, Any]:
		"""Calculate comprehensive simulation metrics"""
		total_delay = 0
		missed_connections = 0
		platform_conflicts = 0
		passenger_delay_hours = 0
		
		# Calculate delays based on disruption severity and type
		for disruption in disruptions:
			disruption_type = disruption.get("type", "delay")
			severity = disruption.get("severity", "medium")
			duration_minutes = disruption.get("duration_seconds", 0) // 60
			
			# Base delay multipliers by severity
			severity_multipliers = {"low": 0.5, "medium": 1.0, "high": 2.0}
			multiplier = severity_multipliers.get(severity, 1.0)
			
			# Type-specific impact calculations
			if disruption_type == "track_block":
				base_delay = duration_minutes * 0.8  # 80% of disruption duration
				total_delay += base_delay * multiplier * len(impacted_trains)
				missed_connections += int(len(impacted_trains) * 0.3 * multiplier)
			elif disruption_type == "delay":
				base_delay = duration_minutes * 0.6
				total_delay += base_delay * multiplier * len(impacted_trains)
			elif disruption_type == "platform_issue":
				base_delay = duration_minutes * 0.4
				total_delay += base_delay * multiplier * len(impacted_trains)
				platform_conflicts += int(len(impacted_trains) * 0.5 * multiplier)
			elif disruption_type == "rolling_stock":
				base_delay = duration_minutes * 0.7
				total_delay += base_delay * multiplier * len(impacted_trains)
			elif disruption_type == "signal_failure":
				base_delay = duration_minutes * 0.5
				total_delay += base_delay * multiplier * len(impacted_trains)
				missed_connections += int(len(impacted_trains) * 0.2 * multiplier)
		
		# Calculate passenger delay (assuming average 50 passengers per train)
		passenger_delay_hours = (total_delay * 50) / 60  # Convert to hours
		
		# Calculate throughput impact
		throughput_impact = min(100, (total_delay / 60) * 10)  # 10% impact per hour of delay
		
		return {
			"total_delay_minutes": round(total_delay, 1),
			"missed_connections": missed_connections,
			"platform_conflicts": platform_conflicts,
			"throughput_impact_percent": round(throughput_impact, 1),
			"passenger_delay_hours": round(passenger_delay_hours, 1)
		}

	def _generate_predictions(self, disruptions: List[Dict[str, Any]], impacted_trains: List[str]) -> Dict[str, Any]:
		"""Generate prediction timeline and train impact details"""
		timeline = []
		train_impacts = []
		
		current_time = datetime.now()
		
		# Generate timeline events
		for i, disruption in enumerate(disruptions):
			start_time = current_time + timedelta(minutes=i * 5)
			duration_minutes = disruption.get("duration_seconds", 0) // 60
			end_time = start_time + timedelta(minutes=duration_minutes)
			
			timeline.append({
				"timestamp": start_time.timestamp(),
				"event": f"{disruption.get('type', 'disruption').replace('_', ' ').title()} starts",
				"impact": f"Affects {len(impacted_trains)} trains"
			})
			
			if duration_minutes > 0:
				timeline.append({
					"timestamp": end_time.timestamp(),
					"event": f"{disruption.get('type', 'disruption').replace('_', ' ').title()} resolved",
					"impact": "Normal operations resume"
				})
		
		# Generate train impact details
		for train_id in impacted_trains:
			# Random delay between 5-45 minutes
			delay_minutes = random.randint(5, 45)
			
			# Determine status based on delay
			if delay_minutes < 15:
				status = "on_time"
			elif delay_minutes < 30:
				status = "delayed"
			else:
				status = "cancelled"
			
			train_impacts.append({
				"train_id": train_id,
				"delay_minutes": delay_minutes,
				"status": status
			})
		
		return {
			"timeline": timeline,
			"train_impacts": train_impacts
		}

	def apply_to_real(self, simulation_id: str) -> Dict[str, Any]:
		"""Apply simulation results to real system"""
		try:
			# In a real implementation, this would:
			
			# 1. Validate the simulation results
			print(f"Validating simulation {simulation_id}...")
			
			# 2. Apply recommended actions to the real system
			actions_applied = self._apply_simulation_actions(simulation_id)
			
			# 3. Update train schedules and platform assignments
			schedule_updates = self._update_train_schedules(simulation_id)
			
			# 4. Notify relevant stakeholders
			notifications_sent = self._notify_stakeholders(simulation_id)
			
			return {
				"success": True,
				"message": f"Simulation {simulation_id} applied to real system successfully",
				"details": {
					"actions_applied": actions_applied,
					"schedule_updates": schedule_updates,
					"notifications_sent": notifications_sent
				}
			}
		except Exception as e:
			return {
				"success": False,
				"message": f"Failed to apply simulation: {str(e)}"
			}

	def _apply_simulation_actions(self, simulation_id: str) -> List[str]:
		"""Apply the recommended actions from simulation to real system"""
		# In real implementation, this would:
		# - Update train speeds and routes
		# - Modify platform assignments
		# - Adjust signal timings
		# - Update crew schedules
		
		actions = [
			"Updated train T001-Local speed to 45 km/h",
			"Reassigned platform 2 to T002-Express", 
			"Adjusted signal timing at Station A",
			"Updated crew schedule for affected trains"
		]
		
		print(f"Applied {len(actions)} actions for simulation {simulation_id}")
		return actions

	def _update_train_schedules(self, simulation_id: str) -> Dict[str, Any]:
		"""Update train schedules based on simulation results"""
		# In real implementation, this would:
		# - Update database with new arrival/departure times
		# - Modify platform assignments
		# - Update passenger information systems
		
		updates = {
			"trains_updated": 4,
			"platform_changes": 2,
			"schedule_adjustments": 8,
			"passenger_notifications": True
		}
		
		print(f"Updated schedules for simulation {simulation_id}: {updates}")
		return updates

	def _notify_stakeholders(self, simulation_id: str) -> List[str]:
		"""Notify relevant stakeholders about the changes"""
		# In real implementation, this would:
		# - Send alerts to train operators
		# - Update passenger information displays
		# - Notify maintenance teams
		# - Alert station managers
		
		notifications = [
			"Alert sent to train operators",
			"Passenger information displays updated",
			"Maintenance team notified",
			"Station managers alerted"
		]
		
		print(f"Sent {len(notifications)} notifications for simulation {simulation_id}")
		return notifications


simulator_service = SimulatorService()


