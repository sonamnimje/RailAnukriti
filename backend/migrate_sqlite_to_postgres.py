#!/usr/bin/env python3
"""
Copy data from a local SQLite file (rail.db) into a PostgreSQL database.

Usage examples:
  PYTHONPATH=backend python backend/migrate_sqlite_to_postgres.py \
    --sqlite backend/app/rail.db \
    --postgres postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME

Notes:
  - Tables are auto-created on the destination if they don't exist.
  - Existing rows are not updated; this performs naive inserts.
"""

from __future__ import annotations

import argparse
from typing import Any, Dict, List, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Import models and Base
from app.db.models import (
    Base,
    User,
    Train,
    Station,
    TrainSchedule,
    TrainPosition,
    Override,
    OptimizerDecision,
    TrainLog,
)


def _rows_to_dicts(session: Session, model_cls: Type[Base]) -> List[Dict[str, Any]]:
    column_names = [c.name for c in model_cls.__table__.columns]
    rows: List[Dict[str, Any]] = []
    for instance in session.query(model_cls).all():
        row = {name: getattr(instance, name) for name in column_names}
        rows.append(row)
    return rows


def migrate(sqlite_url: str, postgres_url: str) -> None:
    src_engine = create_engine(sqlite_url, future=True)
    dst_engine = create_engine(postgres_url, future=True)

    # Ensure destination tables exist
    Base.metadata.create_all(bind=dst_engine)

    with Session(src_engine) as src_sess, Session(dst_engine) as dst_sess:
        # Order matters due to FKs
        copy_order: List[Type[Base]] = [
            User,
            Train,
            Station,
            TrainSchedule,
            TrainPosition,
            Override,
            OptimizerDecision,
            TrainLog,
        ]

        total_inserted: Dict[str, int] = {}

        for model_cls in copy_order:
            data = _rows_to_dicts(src_sess, model_cls)
            if not data:
                total_inserted[model_cls.__tablename__] = 0
                continue

            # Insert in batches for safety
            batch_size = 500
            inserted = 0
            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                dst_sess.execute(model_cls.__table__.insert(), batch)
                inserted += len(batch)

            total_inserted[model_cls.__tablename__] = inserted

        dst_sess.commit()

    for table, count in total_inserted.items():
        print(f"Inserted {count} rows into '{table}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate data from SQLite to PostgreSQL")
    parser.add_argument("--sqlite", required=False, default="sqlite:///backend/app/rail.db", help="Path/URL to source SQLite (default: sqlite:///backend/app/rail.db)")
    parser.add_argument("--postgres", required=True, help="Destination PostgreSQL SQLAlchemy URL (postgresql+psycopg://...)")
    args = parser.parse_args()

    sqlite_url = args.sqlite
    if sqlite_url.endswith(".db") and not sqlite_url.startswith("sqlite:///"):
        sqlite_url = f"sqlite:///{sqlite_url}"

    migrate(sqlite_url, args.postgres)


if __name__ == "__main__":
    main()


