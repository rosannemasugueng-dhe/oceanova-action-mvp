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
    country = Column(String, nullable=False)
    ecosystem = Column(String, default="River")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    global_risk = Column(Integer, nullable=False)
    maternal_risk = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(RiverHotspot).count() == 0:
        seed_rivers = [
            RiverHotspot(name="Donga River", country="Cameroon", ecosystem="River", latitude=6.8833, longitude=10.5500, global_risk=12, maternal_risk=11),
            RiverHotspot(name="Nyabugogo River", country="Rwanda", ecosystem="River", latitude=-1.9397, longitude=30.0444, global_risk=64, maternal_risk=68),
            RiverHotspot(name="Niger River (Onitsha)", country="Nigeria", ecosystem="River", latitude=6.1498, longitude=6.7857, global_risk=81, maternal_risk=86),
            RiverHotspot(name="Nairobi River", country="Kenya", ecosystem="River", latitude=-1.2833, longitude=36.8333, global_risk=84, maternal_risk=89),
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
            "ecosystem": r.ecosystem,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "global_risk": r.global_risk,
            "maternal_risk": r.maternal_risk,
        }
        for r in records
    ]

def save_new_hotspot(name: str, country: str, ecosystem: str, latitude: float, longitude: float, global_risk: int, maternal_risk: int):
    init_db()
    db = SessionLocal()
    record = RiverHotspot(
        name=name,
        country=country,
        ecosystem=ecosystem,
        latitude=latitude,
        longitude=longitude,
        global_risk=global_risk,
        maternal_risk=maternal_risk,
    )
    db.add(record)
    db.commit()
    db.close()
