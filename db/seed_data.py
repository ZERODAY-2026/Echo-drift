import random
from datetime import date, datetime, timedelta

from db.snowflake_client import get_connection

random.seed(42)
TODAY = date.today()
DAYS = 30

DDL = [
	"CREATE OR REPLACE TABLE MACHINES (MACHINE_ID STRING, MACHINE_NAME STRING, LINE STRING, STATUS STRING)",
	"CREATE OR REPLACE TABLE PRODUCTS (PRODUCT_ID STRING, PRODUCT_NAME STRING, MATERIAL_ID STRING)",
	"CREATE OR REPLACE TABLE SUPPLIERS (SUPPLIER_ID STRING, SUPPLIER_NAME STRING, MATERIAL_ID STRING, LEAD_TIME_DAYS INT, AVG_DELAY_DAYS FLOAT)",
	"CREATE OR REPLACE TABLE INVENTORY (MATERIAL_ID STRING, MATERIAL_NAME STRING, STOCK_LEVEL INT, REORDER_POINT INT, WAREHOUSE_ID STRING, SUPPLIER_ID STRING)",
	"CREATE OR REPLACE TABLE DOWNTIME (DOWNTIME_ID INT, MACHINE_ID STRING, START_TIME TIMESTAMP_NTZ, END_TIME TIMESTAMP_NTZ, DURATION_MIN INT, REASON STRING)",
	"CREATE OR REPLACE TABLE PRODUCTION (PROD_ID INT, PROD_DATE DATE, MACHINE_ID STRING, PRODUCT_ID STRING, PLANNED_QTY INT, ACTUAL_QTY INT)",
	"CREATE OR REPLACE TABLE ORDERS (ORDER_ID STRING, CUSTOMER STRING, PRODUCT_ID STRING, QUANTITY INT, ORDER_DATE DATE, DUE_DATE DATE, DELIVERED_DATE DATE, STATUS STRING)",
	"CREATE OR REPLACE TABLE DEFECTS (DEFECT_ID INT, DEFECT_DATE DATE, MACHINE_ID STRING, PRODUCT_ID STRING, DEFECT_TYPE STRING, DEFECT_COUNT INT)",
]

MACHINES = [
	("M-01", "CNC Lathe", "Line A", "Running"),
	("M-02", "Gear Hobber", "Line A", "Running"),
	("M-03", "Panel Assembler", "Line A", "Running"),
	("M-04", "Packing Unit A", "Line A", "Running"),
	("M-05", "Injection Moulder", "Line B", "Running"),
	("M-06", "Laser Cutter", "Line B", "Running"),
	("M-07", "Hydraulic Press", "Line B", "Maintenance"),
	("M-08", "Packing Unit B", "Line B", "Running"),
]
PRODUCTS = [
	("P-100", "Steel Bracket", "MAT-1"),
	("P-200", "Gear Assembly", "MAT-3"),
	("P-300", "Motor Housing", "MAT-2"),
	("P-400", "Control Panel", "MAT-4"),
]
PRODUCT_MACHINE = {"P-100": "M-07", "P-200": "M-02", "P-300": "M-05", "P-400": "M-03"}
SUPPLIERS = [
	("SUP-1", "SteelCo India", "MAT-1", 10, 4.5),
	("SUP-2", "CopperWorks", "MAT-2", 7, 0.8),
	("SUP-3", "AlumaTech", "MAT-3", 8, 1.2),
	("SUP-4", "CircuitPro", "MAT-4", 14, 2.0),
]
INVENTORY = [
	("MAT-1", "Steel Sheet", 180, 500, "WH-1", "SUP-1"),
	("MAT-2", "Copper Wire", 1200, 600, "WH-1", "SUP-2"),
	("MAT-3", "Aluminium Ingot", 900, 400, "WH-2", "SUP-3"),
	("MAT-4", "Circuit Board", 260, 300, "WH-2", "SUP-4"),
]
CUSTOMERS = ["Tata Motors", "Bosch India", "Mahindra", "L&T", "Bajaj Auto", "Ashok Leyland"]
NORMAL_REASONS = ["Scheduled maintenance", "Tool change", "Sensor fault", "Power fluctuation"]
DEFECT_TYPES = ["Surface scratch", "Dimensional error", "Misalignment", "Weld crack", "Paint flaw"]


def gen_downtime():
	rows, i = [], 1
	for d in range(DAYS, 0, -1):
		day = TODAY - timedelta(days=d)
		for mid, *_ in MACHINES:
			if mid == "M-07" and d <= 14:
				p, lo, hi, reason = 0.7, 120, 300, "Hydraulic pump failure"
			else:
				p, lo, hi, reason = 0.12, 15, 90, random.choice(NORMAL_REASONS)
			if random.random() < p:
				start = datetime.combine(day, datetime.min.time()) + timedelta(
					hours=random.randint(6, 18), minutes=random.randint(0, 59))
				dur = random.randint(lo, hi)
				rows.append((i, mid, start, start + timedelta(minutes=dur), dur, reason))
				i += 1
	return rows


def gen_production_and_defects():
	prod, defects, pid, did = [], [], 1, 1
	for d in range(DAYS, 0, -1):
		day = TODAY - timedelta(days=d)
		if day.weekday() == 6:
			continue
		for product, mid in PRODUCT_MACHINE.items():
			ratio = random.uniform(0.55, 0.75) if product == "P-100" and d <= 14 else random.uniform(0.93, 1.0)
			prod.append((pid, day, mid, product, 500, int(500 * ratio)))
			pid += 1
			cnt, dtype = random.randint(0, 6), random.choice(DEFECT_TYPES)
			if mid == "M-05" and d <= 7:
				cnt, dtype = random.randint(15, 30), "Misalignment"
			if cnt:
				defects.append((did, day, mid, product, dtype, cnt))
				did += 1
	return prod, defects


def gen_orders():
	rows = []
	for n in range(1, 46):
		product = random.choice([p[0] for p in PRODUCTS])
		order_date = TODAY - timedelta(days=random.randint(1, 45))
		due = order_date + timedelta(days=random.choice([10, 14, 21]))
		qty = random.choice([200, 500, 800, 1000])
		if due > TODAY:
			status, delivered = "In Production", None
		elif product == "P-100" and order_date >= TODAY - timedelta(days=35):
			status = "Delayed"
			delivered = due + timedelta(days=random.randint(3, 9))
			if delivered > TODAY:
				delivered = None
		elif random.random() < 0.9:
			status, delivered = "Delivered", due - timedelta(days=random.randint(0, 3))
		else:
			status, delivered = "Delayed", due + timedelta(days=random.randint(1, 2))
		rows.append((f"ORD-{1000 + n}", random.choice(CUSTOMERS), product, qty,
					 order_date, due, delivered, status))
	return rows


def insert(cur, table, rows):
	if not rows:
		print(f"  {table}: 0 rows")
		return
	placeholders = ",".join(["%s"] * len(rows[0]))
	cur.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
	print(f"  {table}: {len(rows)} rows")


if __name__ == "__main__":
	conn = get_connection()
	try:
		cur = conn.cursor()
		for stmt in DDL:
			cur.execute(stmt)
		prod, defects = gen_production_and_defects()
		insert(cur, "MACHINES", MACHINES)
		insert(cur, "PRODUCTS", PRODUCTS)
		insert(cur, "SUPPLIERS", SUPPLIERS)
		insert(cur, "INVENTORY", INVENTORY)
		insert(cur, "DOWNTIME", gen_downtime())
		insert(cur, "PRODUCTION", prod)
		insert(cur, "DEFECTS", defects)
		insert(cur, "ORDERS", gen_orders())
		print("Done. Manufacturing data loaded.")
	finally:
		conn.close()
