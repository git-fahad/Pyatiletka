"""
SQLAlchemy ORM Models for Heavy Industry Domain
Pyatiletka Project
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Region(Base):
    __tablename__ = "regions"

    region_id = Column(Integer, primary_key=True, index=True)
    region_code = Column(String(10), unique=True, nullable=False)
    region_name = Column(String(255), nullable=False)
    region_type = Column(String(50), nullable=False)
    parent_region_id = Column(Integer, ForeignKey('regions.region_id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    facilities = relationship("Facility", back_populates="region")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(20), unique=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    product_category = Column(String(100), nullable=False, index=True)
    unit_of_measure = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    production_records = relationship("ActualProduction", back_populates="product")
    targets = relationship("ProductionTarget", back_populates="product")


class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(Integer, primary_key=True, index=True)
    facility_code = Column(String(20), unique=True, nullable=False)
    facility_name = Column(String(255), nullable=False)
    facility_type = Column(String(100), nullable=False, index=True)
    region_id = Column(Integer, ForeignKey('regions.region_id'), nullable=False)
    capacity_per_day = Column(Numeric(15, 2))
    workforce_size = Column(Integer)
    commissioned_date = Column(Date)
    status = Column(String(50), default='ACTIVE', index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    region = relationship("Region", back_populates="facilities")
    production_records = relationship("ActualProduction", back_populates="facility")
    targets = relationship("ProductionTarget", back_populates="facility")
    equipment = relationship("Equipment", back_populates="facility")


class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey('facilities.facility_id'), nullable=False)
    equipment_type = Column(String(100), nullable=False)
    equipment_name = Column(String(255), nullable=False)
    model = Column(String(100))
    install_date = Column(Date)
    last_maintenance_date = Column(Date)
    operational_status = Column(String(50), default='OPERATIONAL', index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    facility = relationship("Facility", back_populates="equipment")


class ProductionTarget(Base):
    __tablename__ = "production_targets"

    target_id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey('facilities.facility_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    plan_year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer)
    target_quantity = Column(Numeric(15, 2), nullable=False)
    target_set_date = Column(Date, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    facility = relationship("Facility", back_populates="targets")
    product = relationship("Product", back_populates="targets")


class ActualProduction(Base):
    __tablename__ = "actual_production"

    production_id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey('facilities.facility_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    production_date = Column(Date, nullable=False, index=True)
    quantity_produced = Column(Numeric(15, 2), nullable=False)
    quality_grade = Column(String(10), nullable=False, index=True)
    shift_number = Column(Integer)
    workers_on_shift = Column(Integer)
    equipment_downtime_hours = Column(Numeric(5, 2))
    defect_count = Column(Integer)
    notes = Column(Text)
    reported_by = Column(String(255))
    reported_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    facility = relationship("Facility", back_populates="production_records")
    product = relationship("Product", back_populates="production_records")