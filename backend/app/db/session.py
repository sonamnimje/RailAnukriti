from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.sync_database_uri, echo=settings.SQLALCHEMY_ECHO, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


