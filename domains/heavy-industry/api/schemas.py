from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


# ============================================================================
# FACILITY SCHEMAS
# ============================================================================

class FacilityBase(BaseModel):
    facility_code: str
    facility_name: str
    facility_type: str
    capacity_per_day: Optional[float] = None
    workforce_size: Optional[int] = None
    status: str = "ACTIVE"


class FacilityResponse(FacilityBase):
    facility_id: int
    region_name: str
    commissioned_date: Optional[date] = None

    class Config:
        from_attributes = True  # Allows ORM model conversion


# ============================================================================
# PRODUCT SCHEMAS
# ============================================================================

class ProductBase(BaseModel):
    product_code: str
    product_name: str
    product_category: str
    unit_of_measure: str
    description: Optional[str] = None


class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True


# ============================================================================
# PRODUCTION SCHEMAS
# ============================================================================

class ProductionRecordResponse(BaseModel):
    production_id: int
    facility_name: str
    product_name: str
    production_date: date
    quantity_produced: float
    quality_grade: str
    shift_number: Optional[int] = None
    workers_on_shift: Optional[int] = None
    equipment_downtime_hours: Optional[float] = None
    defect_count: Optional[int] = None

    class Config:
        from_attributes = True


class DailyProductionSummary(BaseModel):
    production_date: date
    facility_name: str
    product_name: str
    product_category: str
    total_quantity: float
    avg_downtime: Optional[float] = None
    total_defects: int
    shift_count: int


# ============================================================================
# METRICS SCHEMAS
# ============================================================================

class PlanVsActualResponse(BaseModel):
    plan_year: int
    month: int
    facility_name: str
    product_name: str
    planned: float
    actual: float
    completion_percentage: float

    class Config:
        from_attributes = True


class FacilityPerformance(BaseModel):
    facility_name: str
    avg_completion_rate: float
    total_production: float
    avg_quality_score: float


# ============================================================================
# REGION SCHEMAS
# ============================================================================

class RegionResponse(BaseModel):
    region_id: int
    region_code: str
    region_name: str
    region_type: str

    class Config:
        from_attributes = True