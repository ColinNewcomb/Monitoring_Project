from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os

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

Dev_DP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'system_metrics.db')
DB_PATH_DOCKER = os.environ.get('DATABASE_URL', Dev_DP_PATH)

engine = create_engine(f"sqlite:///{DB_PATH_DOCKER}")  # Use SQLite for simplicity
SessionLocal = sessionmaker(bind=engine)

def init_database():
    os.makedirs(os.path.dirname(DB_PATH_DOCKER), exist_ok=True)  # Create directory if it doesn't exist
    Base.metadata.create_all(engine)  # Create tables if they don't exist

def cleanup_database(days_to_keep=14):
    
    session = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)  # Keep last 14 days of data
        delete_count = session.query(SystemMetrics).filter(SystemMetrics.time_stamp < cutoff_date).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error during cleanup: {e}")
    finally:
        session.close()
        
        
def get_database_size():
    
    try:
        size_bytes = os.path.getsize(DB_PATH_DOCKER)
        return size_bytes / (1024 * 1024)  # Convert to MB
    except FileNotFoundError:
        return 0
