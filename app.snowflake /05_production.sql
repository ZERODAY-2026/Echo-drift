USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE DATAMIND_MANUFACTURING_DB;
USE SCHEMA MANUFACTURING;

-- Create the Production table
CREATE OR REPLACE TABLE PRODUCTION (
    RECORD_ID NUMBER,
    PRODUCTION_DATE DATE,
    PRODUCTION_LINE TEXT,
    MACHINE_ID TEXT,
    PRODUCT_NAME TEXT,
    TARGET_UNITS NUMBER,
    ACTUAL_UNITS NUMBER,
    SHORTFALL_UNITS NUMBER,
    DEFECTIVE_UNITS NUMBER,
    DOWNTIME_MINUTES NUMBER
);

-- Insert sample records
INSERT INTO PRODUCTION VALUES
    (1, '2026-10-10', 'Line-A', 'MCH-101', 'Hydraulic Pump', 200, 185, 15, 3, 20),
    (2, '2026-10-11', 'Line-B', 'MCH-204', 'Steel Gear Shaft', 350, 300, 50, 12, 45),
    (3, '2026-10-12', 'Line-C', 'MCH-302', 'Precision Bearing', 500, 490, 10, 2, 10),
    (4, '2026-10-13', 'Line-B', 'MCH-205', 'Turbine Housing', 100, 65, 35, 4, 60),
    (5, '2026-10-14', 'Line-A', 'MCH-102', 'Control Valve', 250, 245, 5, 0, 5),
    (6, '2026-10-15', 'Line-B', 'MCH-204', 'Steel Gear Shaft', 350, 290, 60, 15, 55),
    (7, '2026-10-16', 'Line-C', 'MCH-301', 'Precision Bearing', 500, 480, 20, 5, 15),
    (8, '2026-10-17', 'Line-A', 'MCH-101', 'Hydraulic Pump', 200, 192, 8, 2, 12);
