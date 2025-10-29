-- Heavy Industry Domain Database Schema
-- Gosplan Data Mesh Project
-- Database: heavy_industry

-- ============================================================================
-- REFERENCE TABLES (Dimensions)
-- ============================================================================

-- Regional Hierarchy (3 levels: USSR → Republic → Oblast/Region)
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_code VARCHAR(10) UNIQUE NOT NULL,
    region_name VARCHAR(255) NOT NULL,
    region_type VARCHAR(50) NOT NULL, -- 'USSR', 'REPUBLIC', 'OBLAST'
    parent_region_id INTEGER REFERENCES regions(region_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for hierarchy queries
CREATE INDEX idx_regions_parent ON regions(parent_region_id);
CREATE INDEX idx_regions_type ON regions(region_type);

-- Products (what is being produced)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_category VARCHAR(100) NOT NULL, -- 'STEEL', 'MACHINERY', 'ARMAMENTS'
    unit_of_measure VARCHAR(50) NOT NULL, -- 'TONS', 'UNITS', 'PIECES'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(product_category);

-- Facilities (factories, mills, plants)
CREATE TABLE facilities (
    facility_id SERIAL PRIMARY KEY,
    facility_code VARCHAR(20) UNIQUE NOT NULL,
    facility_name VARCHAR(255) NOT NULL,
    facility_type VARCHAR(100) NOT NULL, -- 'STEEL_MILL', 'MACHINERY_FACTORY', 'TANK_PLANT'
    region_id INTEGER NOT NULL REFERENCES regions(region_id),
    capacity_per_day DECIMAL(15, 2), -- Daily production capacity
    workforce_size INTEGER,
    commissioned_date DATE,
    status VARCHAR(50) DEFAULT 'ACTIVE', -- 'ACTIVE', 'MAINTENANCE', 'INACTIVE'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_capacity_positive CHECK (capacity_per_day > 0),
    CONSTRAINT chk_workforce_positive CHECK (workforce_size >= 0)
);

CREATE INDEX idx_facilities_region ON facilities(region_id);
CREATE INDEX idx_facilities_type ON facilities(facility_type);
CREATE INDEX idx_facilities_status ON facilities(status);

-- Equipment at facilities
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    equipment_type VARCHAR(100) NOT NULL, -- 'BLAST_FURNACE', 'ROLLING_MILL', 'ASSEMBLY_LINE'
    equipment_name VARCHAR(255) NOT NULL,
    model VARCHAR(100),
    install_date DATE,
    last_maintenance_date DATE,
    operational_status VARCHAR(50) DEFAULT 'OPERATIONAL', -- 'OPERATIONAL', 'MAINTENANCE', 'BROKEN'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_equipment_facility ON equipment(facility_id);
CREATE INDEX idx_equipment_status ON equipment(operational_status);

-- ============================================================================
-- TRANSACTIONAL TABLES (Facts)
-- ============================================================================

-- Production Targets (5-year plan targets)
CREATE TABLE production_targets (
    target_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    plan_year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month INTEGER CHECK (month BETWEEN 1 AND 12),
    target_quantity DECIMAL(15, 2) NOT NULL,
    target_set_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_target_positive CHECK (target_quantity > 0),
    CONSTRAINT chk_plan_year CHECK (plan_year BETWEEN 1986 AND 1990),
    CONSTRAINT uk_target UNIQUE (facility_id, product_id, plan_year, month)
);

CREATE INDEX idx_targets_facility ON production_targets(facility_id);
CREATE INDEX idx_targets_product ON production_targets(product_id);
CREATE INDEX idx_targets_year ON production_targets(plan_year);

-- Actual Production (daily production records)
CREATE TABLE actual_production (
    production_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    production_date DATE NOT NULL,
    quantity_produced DECIMAL(15, 2) NOT NULL,
    quality_grade VARCHAR(10) NOT NULL, -- 'A', 'B', 'C'
    shift_number INTEGER CHECK (shift_number BETWEEN 1 AND 3), -- 3 shifts per day
    workers_on_shift INTEGER,
    equipment_downtime_hours DECIMAL(5, 2) DEFAULT 0,
    defect_count INTEGER DEFAULT 0,
    notes TEXT,
    reported_by VARCHAR(255), -- Who reported this data
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_quantity_positive CHECK (quantity_produced >= 0),
    CONSTRAINT chk_quality_valid CHECK (quality_grade IN ('A', 'B', 'C')),
    CONSTRAINT chk_workers_positive CHECK (workers_on_shift >= 0),
    CONSTRAINT chk_downtime_valid CHECK (equipment_downtime_hours >= 0 AND equipment_downtime_hours <= 24),
    CONSTRAINT chk_defects_positive CHECK (defect_count >= 0)
);

CREATE INDEX idx_production_facility ON actual_production(facility_id);
CREATE INDEX idx_production_product ON actual_production(product_id);
CREATE INDEX idx_production_date ON actual_production(production_date);
CREATE INDEX idx_production_quality ON actual_production(quality_grade);

-- Equipment Maintenance Log
CREATE TABLE maintenance_log (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment(equipment_id),
    maintenance_date DATE NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL, -- 'SCHEDULED', 'EMERGENCY', 'REPAIR'
    duration_hours DECIMAL(5, 2) NOT NULL,
    technician_name VARCHAR(255),
    description TEXT,
    cost_rubles DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_duration_positive CHECK (duration_hours > 0)
);

CREATE INDEX idx_maintenance_equipment ON maintenance_log(equipment_id);
CREATE INDEX idx_maintenance_date ON maintenance_log(maintenance_date);

-- Resource Consumption (raw materials, energy)
CREATE TABLE resource_consumption (
    consumption_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES facilities(facility_id),
    consumption_date DATE NOT NULL,
    resource_type VARCHAR(100) NOT NULL, -- 'IRON_ORE', 'COAL', 'ELECTRICITY', 'NATURAL_GAS'
    quantity DECIMAL(15, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL, -- 'TONS', 'KWH', 'CUBIC_METERS'
    cost_rubles DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_consumption_positive CHECK (quantity > 0)
);

CREATE INDEX idx_consumption_facility ON resource_consumption(facility_id);
CREATE INDEX idx_consumption_date ON resource_consumption(consumption_date);
CREATE INDEX idx_consumption_type ON resource_consumption(resource_type);

-- ============================================================================
-- AUDIT TABLE
-- ============================================================================

-- Audit log for all data modifications
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    operation VARCHAR(20) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_table ON audit_log(table_name);
CREATE INDEX idx_audit_date ON audit_log(changed_at);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Daily production summary
CREATE VIEW daily_production_summary AS
SELECT 
    ap.production_date,
    f.facility_name,
    r.region_name,
    p.product_name,
    p.product_category,
    SUM(ap.quantity_produced) as total_quantity,
    AVG(ap.equipment_downtime_hours) as avg_downtime,
    SUM(ap.defect_count) as total_defects,
    COUNT(*) as shift_count
FROM actual_production ap
JOIN facilities f ON ap.facility_id = f.facility_id
JOIN regions r ON f.region_id = r.region_id
JOIN products p ON ap.product_id = p.product_id
GROUP BY ap.production_date, f.facility_name, r.region_name, p.product_name, p.product_category;

-- Plan vs Actual (monthly comparison)
CREATE VIEW plan_vs_actual_monthly AS
SELECT 
    pt.plan_year,
    pt.month,
    f.facility_name,
    r.region_name,
    p.product_name,
    pt.target_quantity as planned,
    COALESCE(SUM(ap.quantity_produced), 0) as actual,
    CASE 
        WHEN pt.target_quantity > 0 THEN 
            ROUND((COALESCE(SUM(ap.quantity_produced), 0) / pt.target_quantity * 100), 2)
        ELSE 0
    END as completion_percentage
FROM production_targets pt
LEFT JOIN actual_production ap ON 
    pt.facility_id = ap.facility_id 
    AND pt.product_id = ap.product_id 
    AND EXTRACT(YEAR FROM ap.production_date) = pt.plan_year
    AND EXTRACT(MONTH FROM ap.production_date) = pt.month
JOIN facilities f ON pt.facility_id = f.facility_id
JOIN regions r ON f.region_id = r.region_id
JOIN products p ON pt.product_id = p.product_id
GROUP BY pt.plan_year, pt.month, f.facility_name, r.region_name, 
         p.product_name, pt.target_quantity;

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE regions IS 'Hierarchical geographic structure: USSR → Republics → Oblasts';
COMMENT ON TABLE products IS 'Types of products produced in heavy industry sector';
COMMENT ON TABLE facilities IS 'Production facilities (mills, factories, plants)';
COMMENT ON TABLE production_targets IS 'Five-year plan targets by facility and product';
COMMENT ON TABLE actual_production IS 'Daily production records with quality metrics';
COMMENT ON TABLE equipment IS 'Equipment inventory at each facility';
COMMENT ON TABLE maintenance_log IS 'Equipment maintenance history';
COMMENT ON TABLE resource_consumption IS 'Raw materials and energy consumption';

-- ============================================================================
-- GRANT PERMISSIONS (for application user)
-- ============================================================================

-- This will be executed when the database is initialized
-- Grant appropriate permissions to the application user

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO heavy_industry_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO heavy_industry_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO heavy_industry_user;