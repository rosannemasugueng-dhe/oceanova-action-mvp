import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# SQLite compatible locally AND PostGIS/PostgreSQL in production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///oceanova_rivers.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RiverHotspot(Base):
    __tablename__ = "river_hotspots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, default="Africa")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    global_risk = Column(Float, nullable=False)
    maternal_risk = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Load reference data only if the database is empty
    if db.query(RiverHotspot).count() == 0:
        seed_rivers = [
            RiverHotspot(name="Donga River", country="Cameroon", latitude=6.8833, longitude=10.5500, global_risk=12.0, maternal_risk=11.5),
            RiverHotspot(name="Nyabugogo River", country="Rwanda", latitude=-1.9397, longitude=30.0444, global_risk=64.0, maternal_risk=68.5),
            RiverHotspot(name="Niger River (Onitsha)", country="Nigeria", latitude=6.1498, longitude=6.7857, global_risk=81.0, maternal_risk=86.0),
            RiverHotspot(name="Nairobi River", country="Kenya", latitude=-1.2833, longitude=36.8333, global_risk=84.0, maternal_risk=89.0),
        ]
        db.add_all(seed_rivers)
        db.commit()
    db.close()

def get_all_hotspots() -> list[dict]:
    init_db()
    db = SessionLocal()
    records = db.query(RiverHotspot).order_by(RiverHotspot.id.desc()).all()
    db.close()
    return [
        {
            "id": r.id,
            "name": r.name,
            "country": r.country,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "global_risk": r.global_risk,
            "maternal_risk": r.maternal_risk,
        }
        for r in records
    ]

def save_new_hotspot(name: str, country: str, latitude: float, longitude: float, global_risk: float, maternal_risk: float):
    init_db()
    db = SessionLocal()
    record = RiverHotspot(
        name=name,
        country=country,
        latitude=latitude,
        longitude=longitude,
        global_risk=global_risk,
        maternal_risk=maternal_risk,
    )
    db.add(record)
    db.commit()
    db.close()
