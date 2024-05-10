import json
import asyncio
import websockets
from utils import print_log
from data_manager import save_trade_data


async def binance_websocket_connection():
    print_log("Starting Binance WebSocket connection")
    retry_delay = min(2, 60)

    while True:
        try:
            async with websockets.connect("wss://stream.binance.com:9443/ws") as websocket:
                await subscribe_to_trades(websocket)

                while True:
                    data = await websocket.recv()
                    await asyncio.sleep(1 / 5)
                    await get_trade_data(data)
        except websockets.exceptions.ConnectionClosed:
            print_log("Connection to Binance closed. Retrying...", level='ERROR', delay=retry_delay)
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 1.5, 60)
            continue
        except Exception as e:
            print_log(f"Error occurred: {e}", level='ERROR')
            continue

    print_log("Binance WebSocket connection ended")


async def subscribe_to_trades(websocket):
    subscription_msg = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@trade", "ethusdt@trade", "xrpusdt@trade",
            "ltcusdt@trade", "adabusdt@trade", "linkusdt@trade",
            "bnbusdt@trade", "dogeusdt@trade", "eosusdt@trade",
            "atomusdt@trade", "solusdt@trade", "dotusdt@trade",
            "maticusdt@trade", "vetusdt@trade", "fttusdt@trade",
            "xtzusdt@trade", "chzusdt@trade", "thetusdt@trade",
            "bchusdt@trade", "filusdt@trade", "unieth@trade"
        ],
        "id": 1
    }
    await websocket.send(json.dumps(subscription_msg))


async def get_trade_data(data):
    try:
        trade_data = json.loads(data)
        symbol = trade_data['s']
        price = trade_data['p']
        print_log(f"Symbol: {symbol}, Price: {price}")
        save_trade_data(symbol, price)
    except KeyError as e:
        print_log(f"Error getting trade data: {e}", level='ERROR')
    except Exception as e:
        print_log(f"Error occurred: {e}", level='ERROR')


if __name__ == "__main__":
    asyncio.run(binance_websocket_connection())
