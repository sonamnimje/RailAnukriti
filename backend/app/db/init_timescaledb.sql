CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Hypertable for train positions (time-series)
CREATE TABLE IF NOT EXISTS train_positions (
	id SERIAL PRIMARY KEY,
	train_id TEXT NOT NULL,
	section_id TEXT NOT NULL,
	planned_block_id TEXT NULL,
	actual_block_id TEXT NULL,
	location_km DOUBLE PRECISION NOT NULL,
	speed_kmph DOUBLE PRECISION NOT NULL,
	timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

SELECT create_hypertable('train_positions', 'timestamp', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_train_positions_train_time ON train_positions (train_id, timestamp DESC);

-- Reference tables and other logs (normal tables)
CREATE TABLE IF NOT EXISTS trains (
	id TEXT PRIMARY KEY,
	class_type TEXT NULL
);

CREATE TABLE IF NOT EXISTS stations (
	id TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	section_id TEXT NULL
);

CREATE TABLE IF NOT EXISTS train_schedules (
	id SERIAL PRIMARY KEY,
	train_id TEXT NOT NULL REFERENCES trains(id),
	station_id TEXT NOT NULL REFERENCES stations(id),
	planned_arrival TIMESTAMPTZ NULL,
	planned_departure TIMESTAMPTZ NULL,
	planned_platform TEXT NULL
);

CREATE TABLE IF NOT EXISTS overrides (
	id TEXT PRIMARY KEY,
	controller_id TEXT NOT NULL,
	train_id TEXT NOT NULL,
	action TEXT NOT NULL,
	ai_action TEXT NULL,
	reason TEXT NULL,
	timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS optimizer_decisions (
	id SERIAL PRIMARY KEY,
	section_id TEXT NOT NULL,
	request JSONB NOT NULL,
	response JSONB NOT NULL,
	latency_ms INTEGER NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


