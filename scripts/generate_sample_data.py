#!/usr/bin/env python3
\"\"\"generate_data.py
Populate the local Postgres instance with sample e-commerce and observability data.
Usage: python generate_data.py --customers 50 --products 40 --orders 200 --metrics 1000
\"\"\"
import time
import argparse
import random
from datetime import datetime, timedelta
import uuid
import json
import os
import sys

import psycopg2
from psycopg2.extras import execute_values

DEFAULT_CONN = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", 5432)),
    "dbname": os.getenv("PGDB", "agentic_db"),
    "user": os.getenv("PGUSER", "agentic"),
    "password": os.getenv("PGPASSWORD", "agentic_pass"),
}

def wait_for_db(conn_info, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            conn = psycopg2.connect(**conn_info)
            conn.close()
            print("DB reachable")
            return True
        except Exception as e:
            print("Waiting for DB... (%s)" % str(e))
            time.sleep(2)
    print("Timed out waiting for DB")
    return False

def random_name():
    first = ["Alex","Sam","Jordan","Taylor","Casey","Riley","Chris","Pat","Robin","Jamie","Drew","Morgan"]
    last = ["Smith","Johnson","Lee","Brown","Garcia","Martinez","Lopez","Wilson","Anderson","Thomas"]
    return f\"{random.choice(first)} {random.choice(last)}\"

def seed_commerce(conn, customers=50, products=40, orders=200):
    with conn.cursor() as cur:
        # Customers
        cust_vals = []
        for _ in range(customers):
            cust_vals.append((str(uuid.uuid4()), random_name(), f'user{random.randint(1000,9999)}@example.com', datetime.utcnow(), random.choice(["US","DE","FR","IN","BR"])))
        execute_values(cur, "INSERT INTO commerce.customers (id, name, email, created_at, country) VALUES %s ON CONFLICT DO NOTHING", cust_vals)
        print(f"Inserted {len(cust_vals)} customers")

        # Products
        prod_vals = []
        categories = ["books","electronics","apparel","home","sports"]
        for i in range(products):
            prod_vals.append((str(uuid.uuid4()), f"SKU{i:05d}", f"Product {i}", round(random.uniform(5.0, 500.0),2), random.choice(categories)))
        execute_values(cur, "INSERT INTO commerce.products (id, sku, name, price, category) VALUES %s ON CONFLICT DO NOTHING", prod_vals)
        print(f"Inserted {len(prod_vals)} products")

        # Orders & items
        # fetch product ids and prices
        cur.execute("SELECT id, price FROM commerce.products")
        product_rows = cur.fetchall()
        for _ in range(orders):
            cust_id = random.choice(cust_vals)[0]
            created_at = datetime.utcnow() - timedelta(days=random.randint(0,60), seconds=random.randint(0,86400))
            status = random.choice(["pending","shipped","delivered","cancelled"])
            # pick 1-5 items
            items = random.sample(product_rows, k=random.randint(1,5))
            total = sum([float(row[1]) * random.randint(1,3) for row in items])
            order_id = str(uuid.uuid4())
            cur.execute("INSERT INTO commerce.orders (id, customer_id, total, created_at, status) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", (order_id, cust_id, round(total,2), created_at, status))
            item_vals = []
            for item in items:
                pid = item[0]
                qty = random.randint(1,3)
                unit = float(item[1])
                item_vals.append((str(uuid.uuid4()), order_id, pid, qty, unit))
            execute_values(cur, "INSERT INTO commerce.order_items (id, order_id, product_id, quantity, unit_price) VALUES %s ON CONFLICT DO NOTHING", item_vals)
        print(f"Inserted {orders} orders and items")

def seed_observability(conn, metrics_count=1000, alerts_count=50, logs_count=500):
    with conn.cursor() as cur:
        # Metrics
        metric_vals = []
        now = datetime.utcnow()
        metric_names = ["cpu_usage","db_connections","query_latency_ms","error_rate"]
        for i in range(metrics_count):
            metric = random.choice(metric_names)
            ts = now - timedelta(seconds=random.randint(0,86400*30))
            value = round(random.uniform(0,1000),3)
            tags = {"env": random.choice(["staging","production"]), "host": f"host-{random.randint(1,20)}"}
            metric_vals.append((str(uuid.uuid4()), metric, value, ts, json.dumps(tags)))
        execute_values(cur, "INSERT INTO observability.metrics (id, metric_name, value, recorded_at, tags) VALUES %s ON CONFLICT DO NOTHING", metric_vals)
        print(f"Inserted {len(metric_vals)} metrics")

        # Alerts
        alert_vals = []
        severities = ["critical","warning","info"]
        for i in range(alerts_count):
            ts = now - timedelta(days=random.randint(0,30))
            alert_vals.append((str(uuid.uuid4()), random.choice(["High CPU","Replica Lag","Slow Query","Error Spike"]), random.choice(severities), ts, random.choice([True,False]), json.dumps({"node": f"node-{random.randint(1,5)}"})))
        execute_values(cur, "INSERT INTO observability.alerts (id, alert_name, severity, fired_at, resolved, metadata) VALUES %s ON CONFLICT DO NOTHING", alert_vals)
        print(f"Inserted {len(alert_vals)} alerts")

        # Logs
        log_vals = []
        levels = ["DEBUG","INFO","WARN","ERROR"]
        services = ["auth","api","worker","billing"]
        for i in range(logs_count):
            ts = now - timedelta(days=random.randint(0,30))
            log_vals.append((str(uuid.uuid4()), random.choice(services), random.choice(levels), f"Sample log message {random.randint(1,10000)}", ts, json.dumps({"request_id": str(uuid.uuid4())})))
        execute_values(cur, "INSERT INTO observability.logs (id, service, level, message, logged_at, context) VALUES %s ON CONFLICT DO NOTHING", log_vals)
        print(f"Inserted {len(log_vals)} logs")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", type=int, default=50)
    parser.add_argument("--products", type=int, default=40)
    parser.add_argument("--orders", type=int, default=200)
    parser.add_argument("--metrics", type=int, default=1000)
    parser.add_argument("--alerts", type=int, default=50)
    parser.add_argument("--logs", type=int, default=500)
    parser.add_argument("--wait", type=int, default=60)
    args = parser.parse_args()

    conn_info = {
        "host": os.getenv("PGHOST", DEFAULT_CONN["host"]),
        "port": int(os.getenv("PGPORT", DEFAULT_CONN["port"])),
        "dbname": os.getenv("PGDB", DEFAULT_CONN["dbname"]),
        "user": os.getenv("PGUSER", DEFAULT_CONN["user"]),
        "password": os.getenv("PGPASSWORD", DEFAULT_CONN["password"]),
    }

    print("Waiting for DB to be ready...")
    if not wait_for_db(conn_info, timeout=args.wait):
        sys.exit(1)

    conn = psycopg2.connect(**conn_info)
    try:
        seed_commerce(conn, customers=args.customers, products=args.products, orders=args.orders)
        seed_observability(conn, metrics_count=args.metrics, alerts_count=args.alerts, logs_count=args.logs)
        conn.commit()
    finally:
        conn.close()
    print("Data generation complete.")

if __name__ == '__main__':
    main()
