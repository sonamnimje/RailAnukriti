from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import ingest, optimizer, simulator, overrides, ws, users, reports, train_logs
from .db.session import engine, SessionLocal
from .db.models import Base
from sqlalchemy import text
import os

from .core.config import settings

# When running from backend/ (Render rootDir), this import is available
try:
	from migrate_sqlite_to_postgres import migrate as migrate_sqlite_to_pg
except Exception:
	migrate_sqlite_to_pg = None  # type: ignore


def create_app() -> FastAPI:

	app = FastAPI(
		title="RailAnukriti Backend",
		description="AI-powered smart train traffic optimizer backend (FastAPI)",
		version="0.1.0",
	)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
	app.include_router(optimizer.router, prefix="/api/optimizer", tags=["optimizer"])
	app.include_router(simulator.router, prefix="/api/simulator", tags=["simulator"])
	app.include_router(overrides.router, prefix="/api/overrides", tags=["overrides"])
	app.include_router(users.router, prefix="/api/users", tags=["users"])
	app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
	app.include_router(train_logs.router, prefix="/api/train-logs", tags=["train-logs"])
	app.include_router(ws.router, tags=["ws"])  # exposes /ws/live

	# Ensure database tables exist on startup
	@app.on_event("startup")
	def on_startup() -> None:
		# If using Postgres on Render, attempt a one-time SQLite -> Postgres migration
		# This is safe to run repeatedly; the migration is idempotent and will skip if dest has data
		if settings.DB_TYPE == "postgresql" and migrate_sqlite_to_pg is not None:
			try:
				# Default location of local SQLite when running from backend/
				sqlite_path = os.getenv("SQLITE_SOURCE_PATH", "app/rail.db")
				postgres_url = os.getenv("DATABASE_URL")
				if postgres_url and os.path.exists(sqlite_path):
					migrate_sqlite_to_pg(f"sqlite:///{sqlite_path}", postgres_url)
			except Exception:
				# Never block startup on migration issues
				pass

		# Ensure tables exist on current engine
		Base.metadata.create_all(bind=engine)

		# Optional: seed demo data once if enabled and database appears empty
		if os.getenv("SEED_ON_STARTUP", "false").lower() == "true":
			try:
				from app.db.models import Train, TrainSchedule, TrainLog
				from seed_train_data import seed_data
				with SessionLocal() as db:
					trains_count = db.query(Train).count()
					schedules_count = db.query(TrainSchedule).count()
					logs_count = db.query(TrainLog).count()
					if trains_count == 0 and schedules_count == 0 and logs_count == 0:
						seed_data()
			except Exception:
				# Never block startup on seed issues
				pass
		# Lightweight migration: ensure overrides.ai_action exists (SQLite-safe)
		with engine.connect() as conn:
			try:
				conn.execute(text("ALTER TABLE overrides ADD COLUMN ai_action TEXT"))
			except Exception:
				# Column likely exists; ignore
				pass

	@app.get("/health")
	def health() -> dict:
		return {"status": "ok"}

	@app.get("/")
	def root() -> dict:
		return {"message": "RailAnukriti backend is running"}

	return app


app = create_app()


