import redis
import psycopg2
import time


from prometheus_client import start_http_server, Counter, Summary

# Prometheus metrics
message_counter = Counter('redis_messages_consumed_total', 'Total Redis messages consumed')
insert_latency = Summary('db_insert_latency_seconds', 'Time to insert into TimescaleDB')

# Start Prometheus metrics server (use a different port than listener)
start_http_server(8001)

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# PostgreSQL / TimescaleDB connection
conn = psycopg2.connect(
    dbname='ticks',
    user='ts_user',
    password='ts_pass',
    host='timescaledb',
    port='5432'
)
cur = conn.cursor()

# Ensure the table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS tick_data (
    symbol TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);
""")
conn.commit()

print("Listening to Redis stream 'ticks'...")

last_id = '0'  # Start from the beginning

while True:
    try:
        messages = redis_client.xread({'ticks': last_id}, block=2000, count=10)

        for stream_name, entries in messages:
            for msg_id, data in entries:
                last_id = msg_id
                symbol = data.get('symbol')
                price = float(data.get('price'))
                ts = data.get('timestamp')

                with insert_latency.time():
                    cur.execute(
                        "INSERT INTO tick_data (symbol, price, timestamp) VALUES (%s, %s, %s)",
                        (symbol, price, ts)
                    )
                    conn.commit()

                message_counter.inc()
                print(f"Inserted: {symbol} {price} @ {ts}")

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
