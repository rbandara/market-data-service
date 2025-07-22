import nest_asyncio
nest_asyncio.apply()

import asyncio
import redis
import os
from alpaca.data.live import StockDataStream

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
stream = StockDataStream(API_KEY, API_SECRET)
print("started redus steaming")


from prometheus_client import start_http_server, Counter

tick_counter = Counter('alpaca_ticks_received', 'Number of Alpaca ticks received')


async def handle_trade(trade):
    tick_counter.inc()
    msg = {
        "symbol": trade.symbol,
        "price": str(trade.price),
        "timestamp": trade.timestamp.isoformat()
    }
    redis_client.xadd("ticks", msg)
    print(f"[{trade.symbol}] {trade.price} @ {trade.timestamp}")

async def main():
    print("Subscribing to trades...")

    start_http_server(9102)  # For listener or 9102 for consumer
    asyncio.run(main())
 
    stream.subscribe_trades(handle_trade, "SPY", "QQQ")
    await stream.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
