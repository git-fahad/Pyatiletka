-- Seed Data for Heavy Industry Domain
-- Reference data to get started

-- ============================================================================
-- REGIONS (Geographic Hierarchy)
-- ============================================================================

-- Level 1: USSR
INSERT INTO regions (region_code, region_name, region_type, parent_region_id) VALUES
('USSR', 'Union of Soviet Socialist Republics', 'USSR', NULL);

-- Level 2: Republics
INSERT INTO regions (region_code, region_name, region_type, parent_region_id) VALUES
('RSFSR', 'Russian Soviet Federative Socialist Republic', 'REPUBLIC', 1),
('UKR-SSR', 'Ukrainian Soviet Socialist Republic', 'REPUBLIC', 1),
('KAZ-SSR', 'Kazakh Soviet Socialist Republic', 'REPUBLIC', 1),
('BLR-SSR', 'Byelorussian Soviet Socialist Republic', 'REPUBLIC', 1);

-- Level 3: Major Industrial Oblasts/Regions
INSERT INTO regions (region_code, region_name, region_type, parent_region_id) VALUES
-- Russian SFSR regions
('URALS', 'Urals Industrial Region', 'OBLAST', 2),
('SIBERIA', 'Siberian Federal District', 'OBLAST', 2),
('MOSCOW-OBL', 'Moscow Oblast', 'OBLAST', 2),
('LENINGRAD', 'Leningrad Oblast', 'OBLAST', 2),
-- Ukrainian SSR regions
('DONBASS', 'Donbass Region', 'OBLAST', 3),
('DNIPRO', 'Dnipropetrovsk Oblast', 'OBLAST', 3),
-- Kazakh SSR regions
('KARAGANDA', 'Karaganda Oblast', 'OBLAST', 4),
('PAVLODAR', 'Pavlodar Oblast', 'OBLAST', 4);

-- ============================================================================
-- PRODUCTS
-- ============================================================================

-- Steel Products
INSERT INTO products (product_code, product_name, product_category, unit_of_measure, description) VALUES
('STEEL-001', 'Hot Rolled Steel Sheets', 'STEEL', 'TONS', 'Standard hot rolled steel for construction'),
('STEEL-002', 'Cold Rolled Steel Coils', 'STEEL', 'TONS', 'Cold rolled steel for automotive industry'),
('STEEL-003', 'Steel Pipes', 'STEEL', 'TONS', 'Steel pipes for oil and gas infrastructure'),
('STEEL-004', 'Steel Beams (I-Beams)', 'STEEL', 'TONS', 'Structural steel beams for construction'),
('STEEL-005', 'Stainless Steel', 'STEEL', 'TONS', 'High-grade stainless steel');

-- Machinery Products
INSERT INTO products (product_code, product_name, product_category, unit_of_measure, description) VALUES
('MACH-001', 'Industrial Tractors', 'MACHINERY', 'UNITS', 'Heavy-duty tractors for agriculture and construction'),
('MACH-002', 'Metal Lathes', 'MACHINERY', 'UNITS', 'Precision metal working lathes'),
('MACH-003', 'Mining Excavators', 'MACHINERY', 'UNITS', 'Large excavators for mining operations'),
('MACH-004', 'Transport Trucks', 'MACHINERY', 'UNITS', 'Heavy transport trucks (ZIL, KAMAZ)'),
('MACH-005', 'Railway Locomotives', 'MACHINERY', 'UNITS', 'Electric and diesel locomotives');

-- Armaments Products
INSERT INTO products (product_code, product_name, product_category, unit_of_measure, description) VALUES
('ARM-001', 'T-72 Main Battle Tanks', 'ARMAMENTS', 'UNITS', 'Standard main battle tank'),
('ARM-002', 'BMP Infantry Fighting Vehicles', 'ARMAMENTS', 'UNITS', 'Armored personnel carriers'),
('ARM-003', 'Artillery Pieces', 'ARMAMENTS', 'UNITS', 'Various caliber artillery'),
('ARM-004', 'Military Aircraft Components', 'ARMAMENTS', 'TONS', 'Components for MiG and Sukhoi aircraft');

-- ============================================================================
-- FACILITIES
-- ============================================================================

-- Steel Mills
INSERT INTO facilities (facility_code, facility_name, facility_type, region_id, capacity_per_day, workforce_size, commissioned_date, status) VALUES
('MILL-001', 'Magnitogorsk Iron and Steel Works', 'STEEL_MILL', 6, 35000, 58000, '1932-02-01', 'ACTIVE'),
('MILL-002', 'Cherepovets Steel Mill', 'STEEL_MILL', 6, 28000, 42000, '1955-08-24', 'ACTIVE'),
('MILL-003', 'Azovstal Iron and Steel Works', 'STEEL_MILL', 10, 22000, 35000, '1933-02-04', 'ACTIVE'),
('MILL-004', 'Karaganda Metallurgical Plant', 'STEEL_MILL', 12, 18000, 28000, '1960-01-15', 'ACTIVE'),
('MILL-005', 'Nizhny Tagil Iron and Steel Works', 'STEEL_MILL', 6, 25000, 38000, '1940-06-25', 'ACTIVE');

-- Machinery Factories
INSERT INTO facilities (facility_code, facility_name, facility_type, region_id, capacity_per_day, workforce_size, commissioned_date, status) VALUES
('FACT-001', 'Chelyabinsk Tractor Plant', 'MACHINERY_FACTORY', 6, 85, 22000, '1933-06-01', 'ACTIVE'),
('FACT-002', 'Kirov Plant (Leningrad)', 'MACHINERY_FACTORY', 9, 65, 28000, '1801-01-01', 'ACTIVE'),
('FACT-003', 'Uralmash (Ural Heavy Machinery Plant)', 'MACHINERY_FACTORY', 6, 120, 32000, '1933-07-15', 'ACTIVE'),
('FACT-004', 'ZIL Automobile Plant', 'MACHINERY_FACTORY', 8, 200, 45000, '1916-08-02', 'ACTIVE');

-- Tank Plants
INSERT INTO facilities (facility_code, facility_name, facility_type, region_id, capacity_per_day, workforce_size, commissioned_date, status) VALUES
('TANK-001', 'Uralvagonzavod (Nizhny Tagil)', 'TANK_PLANT', 6, 12, 28000, '1936-10-11', 'ACTIVE'),
('TANK-002', 'Malyshev Factory (Kharkiv)', 'TANK_PLANT', 10, 8, 18000, '1895-01-01', 'ACTIVE'),
('TANK-003', 'Omsk Transport Machine Plant', 'TANK_PLANT', 7, 6, 15000, '1942-01-01', 'ACTIVE');

-- ============================================================================
-- EQUIPMENT (Sample for a few facilities)
-- ============================================================================

-- Equipment at Magnitogorsk Steel Mill
INSERT INTO equipment (facility_id, equipment_type, equipment_name, model, install_date, operational_status) VALUES
(1, 'BLAST_FURNACE', 'Blast Furnace #10', 'BF-5000', '1980-03-15', 'OPERATIONAL'),
(1, 'BLAST_FURNACE', 'Blast Furnace #11', 'BF-5000', '1982-07-20', 'OPERATIONAL'),
(1, 'ROLLING_MILL', 'Hot Rolling Mill Line 1', 'HRM-2500', '1978-11-05', 'OPERATIONAL'),
(1, 'ROLLING_MILL', 'Hot Rolling Mill Line 2', 'HRM-2500', '1981-04-12', 'OPERATIONAL'),
(1, 'OXYGEN_CONVERTER', 'BOF Converter #3', 'BOF-350', '1983-09-30', 'OPERATIONAL');

-- Equipment at Uralvagonzavod Tank Plant
INSERT INTO equipment (facility_id, equipment_type, equipment_name, model, install_date, operational_status) VALUES
(9, 'ASSEMBLY_LINE', 'Tank Assembly Line A', 'TAL-T72', '1975-06-01', 'OPERATIONAL'),
(9, 'ASSEMBLY_LINE', 'Tank Assembly Line B', 'TAL-T72', '1979-08-15', 'OPERATIONAL'),
(9, 'WELDING_ROBOT', 'Automated Hull Welder', 'AWR-500', '1984-02-20', 'OPERATIONAL'),
(9, 'TESTING_FACILITY', 'Engine Test Bay', 'ETB-1000', '1976-10-10', 'OPERATIONAL');

-- ============================================================================
-- PRODUCTION TARGETS (Sample for 1986)
-- ============================================================================

-- Steel Production Targets for Q1 1986
INSERT INTO production_targets (facility_id, product_id, plan_year, quarter, month, target_quantity, target_set_date) VALUES
-- Magnitogorsk Steel Mill targets
(1, 1, 1986, 1, 1, 980000, '1985-12-01'), -- Hot Rolled Steel
(1, 1, 1986, 1, 2, 950000, '1985-12-01'),
(1, 1, 1986, 1, 3, 1020000, '1985-12-01'),
(1, 3, 1986, 1, 1, 180000, '1985-12-01'), -- Steel Pipes
(1, 3, 1986, 1, 2, 175000, '1985-12-01'),
(1, 3, 1986, 1, 3, 185000, '1985-12-01');

-- Machinery targets for Q1 1986
INSERT INTO production_targets (facility_id, product_id, plan_year, quarter, month, target_quantity, target_set_date) VALUES
(5, 6, 1986, 1, 1, 2400, '1985-12-01'), -- Tractors
(5, 6, 1986, 1, 2, 2300, '1985-12-01'),
(5, 6, 1986, 1, 3, 2500, '1985-12-01'),
(8, 9, 1986, 1, 1, 5800, '1985-12-01'), -- Trucks
(8, 9, 1986, 1, 2, 5600, '1985-12-01'),
(8, 9, 1986, 1, 3, 6000, '1985-12-01');

-- Tank production targets for Q1 1986
INSERT INTO production_targets (facility_id, product_id, plan_year, quarter, month, target_quantity, target_set_date) VALUES
(9, 11, 1986, 1, 1, 340, '1985-12-01'), -- T-72 Tanks
(9, 11, 1986, 1, 2, 320, '1985-12-01'),
(9, 11, 1986, 1, 3, 360, '1985-12-01');

-- ============================================================================
-- SAMPLE ACTUAL PRODUCTION (Few days in January 1986)
-- ============================================================================

-- Some sample production records for the first week of January 1986
INSERT INTO actual_production (facility_id, product_id, production_date, quantity_produced, quality_grade, shift_number, workers_on_shift, equipment_downtime_hours, defect_count, reported_by) VALUES
-- Magnitogorsk Steel Mill - January 2-7, 1986
(1, 1, '1986-01-02', 31500, 'A', 1, 18200, 1.5, 12, 'V. Petrov'),
(1, 1, '1986-01-02', 32100, 'A', 2, 18500, 0.5, 8, 'V. Petrov'),
(1, 1, '1986-01-02', 30800, 'B', 3, 17800, 2.0, 15, 'V. Petrov'),
(1, 1, '1986-01-03', 32800, 'A', 1, 18400, 0.0, 5, 'V. Petrov'),
(1, 1, '1986-01-03', 31900, 'A', 2, 18300, 1.0, 10, 'V. Petrov'),
(1, 1, '1986-01-03', 31200, 'A', 3, 18000, 0.5, 7, 'V. Petrov'),

-- Uralvagonzavod - Tank production January 2-7, 1986
(9, 11, '1986-01-02', 11, 'A', 1, 8800, 0.0, 0, 'A. Ivanov'),
(9, 11, '1986-01-02', 10, 'A', 2, 8500, 2.5, 1, 'A. Ivanov'),
(9, 11, '1986-01-03', 12, 'A', 1, 9000, 0.0, 0, 'A. Ivanov'),
(9, 11, '1986-01-03', 11, 'B', 2, 8700, 1.0, 1, 'A. Ivanov'),
(9, 11, '1986-01-04', 11, 'A', 1, 8900, 0.5, 0, 'A. Ivanov'),
(9, 11, '1986-01-04', 10, 'A', 2, 8600, 1.5, 0, 'A. Ivanov');

-- ============================================================================
-- VERIFY DATA
-- ============================================================================

-- Show summary of what was inserted
SELECT 'Regions', COUNT(*) FROM regions
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Facilities', COUNT(*) FROM facilities
UNION ALL
SELECT 'Equipment', COUNT(*) FROM equipment
UNION ALL
SELECT 'Production Targets', COUNT(*) FROM production_targets
UNION ALL
SELECT 'Actual Production', COUNT(*) FROM actual_production;