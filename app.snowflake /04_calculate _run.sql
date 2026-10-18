USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE DATAMIND_MANUFACTURING_DB;
USE SCHEMA MANUFACTURING;

-- =====================================================================
-- CALCULATION 1: Quality Yield & Defect Rates by Product
-- Evaluates production quality: net passed units, defect %, and yield %
-- =====================================================================
SELECT 
    INSPECTION_ID,
    PRODUCT_NAME,
    INSPECTED_QUANTITY,
    DEFECTIVE_QUANTITY,
    (INSPECTED_QUANTITY - DEFECTIVE_QUANTITY) AS PASSED_QUANTITY,
    ROUND((DEFECTIVE_QUANTITY / INSPECTED_QUANTITY) * 100, 2) AS DEFECT_RATE_PCT,
    ROUND(((INSPECTED_QUANTITY - DEFECTIVE_QUANTITY) / INSPECTED_QUANTITY) * 100, 2) AS YIELD_RATE_PCT
FROM QUALITY_INSPECTIONS
ORDER BY DEFECT_RATE_PCT DESC;

-- =====================================================================
-- CALCULATION 2: Lead Time (Days) & Production Schedule
-- Calculates the turnaround time from order creation to delivery
-- =====================================================================
SELECT 
    ORDER_ID,
    CUSTOMER_NAME,
    PRODUCT_NAME,
    ORDER_QUANTITY,
    ORDER_DATE,
    DELIVERY_DATE,
    DATEDIFF('day', ORDER_DATE, DELIVERY_DATE) AS LEAD_TIME_DAYS,
    ORDER_STATUS
FROM CUSTOMER_ORDERS
ORDER BY LEAD_TIME_DAYS DESC;

-- =====================================================================
-- CALCULATION 3: Manufacturing Production vs. Quality JOIN Analysis
-- Joins Customer Orders with Quality Inspections to track net yield vs ordered targets
-- =====================================================================
SELECT 
    o.ORDER_ID,
    o.CUSTOMER_NAME,
    o.PRODUCT_NAME,
    o.ORDER_STATUS,
    o.ORDER_QUANTITY,
    q.INSPECTED_QUANTITY,
    q.DEFECTIVE_QUANTITY,
    (q.INSPECTED_QUANTITY - q.DEFECTIVE_QUANTITY) AS USABLE_UNITS,
    o.ORDER_QUANTITY - (q.INSPECTED_QUANTITY - q.DEFECTIVE_QUANTITY) AS REMAINING_UNITS_NEEDED,
    ROUND((q.DEFECTIVE_QUANTITY / q.INSPECTED_QUANTITY) * 100, 2) AS DEFECT_RATE_PCT
FROM CUSTOMER_ORDERS o
JOIN QUALITY_INSPECTIONS q
    ON o.PRODUCT_NAME = q.PRODUCT_NAME
ORDER BY o.ORDER_ID;

-- =====================================================================
-- CALCULATION 4: Executive Status Summary
-- Aggregates orders, volume, and average turnaround per pipeline status
-- =====================================================================
SELECT 
    ORDER_STATUS,
    COUNT(ORDER_ID) AS TOTAL_ORDERS,
    SUM(ORDER_QUANTITY) AS TOTAL_VOLUME_ORDERED,
    ROUND(AVG(DATEDIFF('day', ORDER_DATE, DELIVERY_DATE)), 1) AS AVG_LEAD_TIME_DAYS
FROM CUSTOMER_ORDERS
GROUP BY ORDER_STATUS
ORDER BY TOTAL_VOLUME_ORDERED DESC;
