import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///oceanova_rivers.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RiverRecord(Base):
    __tablename__ = "river_records"
    id = Column(Integer, primary_key=True, index=True)
    river_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    global_risk_index = Column(Float, nullable=False)
    maternal_vulnerability_index = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(RiverRecord).count() == 0:
        initial_data = [
            RiverRecord(river_name="Donga River", country="Cameroon", latitude=6.8833, longitude=10.5500, global_risk_index=12.0, maternal_vulnerability_index=11.5),
            RiverRecord(river_name="Nyabugogo River", country="Rwanda", latitude=-1.9397, longitude=30.0444, global_risk_index=64.0, maternal_vulnerability_index=68.5),
            RiverRecord(river_name="Niger River (Onitsha)", country="Nigeria", latitude=6.1498, longitude=6.7857, global_risk_index=81.0, maternal_vulnerability_index=86.0),
            RiverRecord(river_name="Nairobi River", country="Kenya", latitude=-1.2833, longitude=36.8333, global_risk_index=84.0, maternal_vulnerability_index=89.0),
        ]
        db.add_all(initial_data)
        db.commit()
    db.close()

def load_rivers_df() -> pd.DataFrame:
    init_db()
    return pd.read_sql("SELECT * FROM river_records ORDER BY id DESC", engine)

def add_river_record(river_name: str, country: str, lat: float, lon: float, global_idx: float, maternal_idx: float):
    db = SessionLocal()
    new_record = RiverRecord(
        river_name=river_name,
        country=country,
        latitude=lat,
        longitude=lon,
        global_risk_index=global_idx,
        maternal_vulnerability_index=maternal_idx
    )
    db.add(new_record)
    db.commit()
    db.close()
