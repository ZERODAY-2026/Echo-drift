SCHEMA_TEXT = """
Snowflake SQL. Tables (all in current schema):

MACHINES(MACHINE_ID, MACHINE_NAME, LINE, STATUS)
PRODUCTS(PRODUCT_ID, PRODUCT_NAME, MATERIAL_ID)
SUPPLIERS(SUPPLIER_ID, SUPPLIER_NAME, MATERIAL_ID, LEAD_TIME_DAYS, AVG_DELAY_DAYS)
INVENTORY(MATERIAL_ID, MATERIAL_NAME, STOCK_LEVEL, REORDER_POINT, WAREHOUSE_ID, SUPPLIER_ID)
DOWNTIME(DOWNTIME_ID, MACHINE_ID, START_TIME, END_TIME, DURATION_MIN, REASON)
PRODUCTION(PROD_ID, PROD_DATE, MACHINE_ID, PRODUCT_ID, PLANNED_QTY, ACTUAL_QTY)
ORDERS(ORDER_ID, CUSTOMER, PRODUCT_ID, QUANTITY, ORDER_DATE, DUE_DATE, DELIVERED_DATE, STATUS)
DEFECTS(DEFECT_ID, DEFECT_DATE, MACHINE_ID, PRODUCT_ID, DEFECT_TYPE, DEFECT_COUNT)

Notes:
- ORDERS.STATUS is one of: Delivered, Delayed, In Production.
- An order is late when DELIVERED_DATE > DUE_DATE (or DELIVERED_DATE is NULL and DUE_DATE < CURRENT_DATE()).
- Production shortfall = PLANNED_QTY - ACTUAL_QTY.
- Low stock means STOCK_LEVEL < REORDER_POINT.
- Joins: PRODUCTS.MATERIAL_ID = INVENTORY.MATERIAL_ID, ORDERS.PRODUCT_ID = PRODUCTS.PRODUCT_ID,
  DOWNTIME/PRODUCTION/DEFECTS.MACHINE_ID = MACHINES.MACHINE_ID.
- Always use CURRENT_DATE() for relative dates ("last week" = DATEADD(day,-7,CURRENT_DATE())), never hardcode dates.
"""

EXAMPLES = """
Q: Which machine had the most downtime in the last 7 days?
{"status":"ok","sql":"SELECT m.MACHINE_ID, m.MACHINE_NAME, SUM(d.DURATION_MIN)/60 AS DOWNTIME_HOURS FROM DOWNTIME d JOIN MACHINES m ON d.MACHINE_ID=m.MACHINE_ID WHERE d.START_TIME >= DATEADD(day,-7,CURRENT_DATE()) GROUP BY m.MACHINE_ID, m.MACHINE_NAME ORDER BY DOWNTIME_HOURS DESC","message":""}

Q: Which materials are below reorder point?
{"status":"ok","sql":"SELECT MATERIAL_NAME, STOCK_LEVEL, REORDER_POINT FROM INVENTORY WHERE STOCK_LEVEL < REORDER_POINT","message":""}

Q: How is production?
{"status":"ambiguous","sql":"","message":"Do you mean output vs plan, for which product or machine, and over what time period?"}

Q: Predict next year's profit
{"status":"unsupported","sql":"","message":"The data has no cost, revenue or forecasting information, so I cannot answer this reliably."}
"""
