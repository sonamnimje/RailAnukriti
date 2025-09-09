from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import ingest, optimizer, simulator, overrides, ws, users, reports, train_logs
from .db.session import engine
from .db.models import Base
from sqlalchemy import text


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
		Base.metadata.create_all(bind=engine)
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


