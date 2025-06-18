# models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Donor(Base):
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    phone = Column(String(20))
    blood_type = Column(String(5))

class Recipient(Base):
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    hospital = Column(String(100))
    ward = Column(String(50))
    bed_number = Column(String(10))
    blood_type = Column(String(5))

# One-time DB creation
if __name__ == "__main__":
    engine = create_engine("sqlite:///blood.db", echo=True)
    Base.metadata.create_all(engine)
