"""
Heavy Industry Domain API
Pyatiletka Project - Five Year Plan Data Mesh

Main FastAPI application
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Import our modules
from database import get_db, engine
from models import Base, Facility, Product, Region, ActualProduction, ProductionTarget
from schemas import (
    FacilityResponse,
    ProductResponse,
    RegionResponse
)

# Create database tables (if they don't exist)
# This won't recreate existing tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Heavy Industry API",
    description="REST API for Heavy Industry domain data - Pyatiletka Project",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "service": "Heavy Industry API",
        "project": "Pyatiletka",
        "version": "1.0.0"
    }


# ============================================================================
# FACILITIES ENDPOINTS
# ============================================================================

@app.get("/facilities", response_model=List[FacilityResponse], tags=["Facilities"])
def get_facilities(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=500, description="Max records to return"),
        facility_type: Optional[str] = Query(None, description="Filter by facility type"),
        status: Optional[str] = Query(None, description="Filter by status"),
        db: Session = Depends(get_db)
):
    """
    Get list of all facilities with optional filters

    - **skip**: Pagination offset
    - **limit**: Max results per page
    - **facility_type**: Filter by STEEL_MILL, MACHINERY_FACTORY, TANK_PLANT
    - **status**: Filter by ACTIVE, MAINTENANCE, INACTIVE
    """
    query = db.query(
        Facility.facility_id,
        Facility.facility_code,
        Facility.facility_name,
        Facility.facility_type,
        Facility.capacity_per_day,
        Facility.workforce_size,
        Facility.commissioned_date,
        Facility.status,
        Region.region_name
    ).join(Region, Facility.region_id == Region.region_id)

    # Apply filters
    if facility_type:
        query = query.filter(Facility.facility_type == facility_type)
    if status:
        query = query.filter(Facility.status == status)

    # Get results
    facilities = query.offset(skip).limit(limit).all()

    # Convert to response model
    return [
        FacilityResponse(
            facility_id=f.facility_id,
            facility_code=f.facility_code,
            facility_name=f.facility_name,
            facility_type=f.facility_type,
            capacity_per_day=float(f.capacity_per_day) if f.capacity_per_day else None,
            workforce_size=f.workforce_size,
            commissioned_date=f.commissioned_date,
            status=f.status,
            region_name=f.region_name
        )
        for f in facilities
    ]


@app.get("/facilities/{facility_id}", response_model=FacilityResponse, tags=["Facilities"])
def get_facility_by_id(
        facility_id: int,
        db: Session = Depends(get_db)
):
    """
    Get a specific facility by ID
    """
    facility = db.query(
        Facility.facility_id,
        Facility.facility_code,
        Facility.facility_name,
        Facility.facility_type,
        Facility.capacity_per_day,
        Facility.workforce_size,
        Facility.commissioned_date,
        Facility.status,
        Region.region_name
    ).join(Region, Facility.region_id == Region.region_id) \
        .filter(Facility.facility_id == facility_id) \
        .first()

    if not facility:
        raise HTTPException(status_code=404, detail=f"Facility {facility_id} not found")

    return FacilityResponse(
        facility_id=facility.facility_id,
        facility_code=facility.facility_code,
        facility_name=facility.facility_name,
        facility_type=facility.facility_type,
        capacity_per_day=float(facility.capacity_per_day) if facility.capacity_per_day else None,
        workforce_size=facility.workforce_size,
        commissioned_date=facility.commissioned_date,
        status=facility.status,
        region_name=facility.region_name
    )


# ============================================================================
# PRODUCTS ENDPOINTS
# ============================================================================

@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(
        category: Optional[str] = Query(None, description="Filter by category (STEEL, MACHINERY, ARMAMENTS)"),
        db: Session = Depends(get_db)
):
    """
    Get list of all products with optional category filter
    """
    query = db.query(Product)

    if category:
        query = query.filter(Product.product_category == category)

    products = query.all()
    return products


@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product_by_id(
        product_id: int,
        db: Session = Depends(get_db)
):
    """
    Get a specific product by ID
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    return product


# ============================================================================
# REGIONS ENDPOINTS
# ============================================================================

@app.get("/regions", response_model=List[RegionResponse], tags=["Regions"])
def get_regions(
        region_type: Optional[str] = Query(None, description="Filter by type (USSR, REPUBLIC, OBLAST)"),
        db: Session = Depends(get_db)
):
    """
    Get list of all regions
    """
    query = db.query(Region)

    if region_type:
        query = query.filter(Region.region_type == region_type)

    regions = query.order_by(Region.region_id).all()
    return regions


# ============================================================================
# STATS ENDPOINT
# ============================================================================

@app.get("/stats", tags=["Statistics"])
def get_stats(db: Session = Depends(get_db)):
    """
    Get basic statistics about the database
    """
    return {
        "total_facilities": db.query(Facility).count(),
        "total_products": db.query(Product).count(),
        "total_regions": db.query(Region).count(),
        "total_production_records": db.query(ActualProduction).count(),
        "total_targets": db.query(ProductionTarget).count()
    }