from sqlalchemy import Boolean, Column, DateTime, Float, Identity, Integer, String

from sqlalchemy.orm import declarative_base

Base = declarative_base()



class Trip(Base):
    __tablename__ = "trips"

    pk_id = Column(Integer, Identity(), primary_key=True)
    trip_id = Column(String)
    vendor_id = Column(Integer, nullable=True)
    pickup_datetime = Column(DateTime, nullable=True)
    dropoff_datetime = Column(DateTime, nullable=True)
    passenger_count = Column(Integer, nullable=True)
    pickup_longitude = Column(Float, nullable=True)
    pickup_latitude = Column(Float, nullable=True)
    dropoff_longitude = Column(Float, nullable=True)
    dropoff_latitude = Column(Float, nullable=True)
    store_and_fwd_flag = Column(Boolean, nullable=True)
    trip_duration = Column(Integer, nullable=True)

