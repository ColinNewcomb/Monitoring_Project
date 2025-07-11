from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float, nullable=False)
    memory_info = Column(Float, nullable=False)
    disk_info = Column(Float, nullable=False)
    anomaly = Column(Boolean, default=False)
    anomaly_cause = Column(String, nullable=True)
    anomaly_deviation = Column(Float, nullable=True)

    # network_sent = Column(Float, nullable=True)
    # network_recv = Column(Float, nullable=True)
    # boot_time = Column(DateTime, nullable=True)
    # user_info = Column(String, nullable=True)
    
    
engine = create_engine('sqlite:///system_metrics.db')  # Use SQLite for simplicity
SessionLocal = sessionmaker(bind=engine)

def init_database():
    Base.metadata.create_all(engine)

