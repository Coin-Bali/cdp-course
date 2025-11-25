import sys
import os
import json
import time
import threading
import websocket
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.cdp_auth import generate_jwt

load_dotenv(find_dotenv())

# --- WebSocket Client ---
def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Closed: {close_status_code} - {close_msg}")

def on_open(ws):
    def run(*args):
        # Subscribe to a public market data channel (e.g., ticker for BTC-USD)
        subscribe_message = {
            "type": "subscribe",
            "product_ids": ["BTC-USD"],
            "channel": "ticker"
        }
        
        # Example of Authenticated Subscription (User channel)
        # To use this, uncomment lines below and ensure CDP keys have permissions.
        # For Websockets, we pass method=None to generate_jwt to omit the 'uri' claim.
        
        # api_key_id = os.getenv("CDP_API_KEY_ID")
        # api_key_secret = os.getenv("CDP_API_KEY_SECRET")
        # if api_key_id and api_key_secret:
        #     try:
        #         jwt_token = generate_jwt(api_key_id, api_key_secret, request_method=None)
        #         subscribe_message["jwt"] = jwt_token
        #         subscribe_message["channel"] = "user" # Change to user channel
        #         print("Generated JWT for WebSocket auth.")
        #     except Exception as e:
        #         print(f"Auth Error: {e}")

        ws.send(json.dumps(subscribe_message))
        print(f"Sent subscribe message: {subscribe_message}")

        # Keep the connection alive for a while
        time.sleep(10) 
        
        # Unsubscribe (optional)
        unsubscribe_message = {
            "type": "unsubscribe",
            "product_ids": ["BTC-USD"],
            "channel": "ticker"
        }
        ws.send(json.dumps(unsubscribe_message))
        print(f"Sent unsubscribe message: {unsubscribe_message}")
        time.sleep(1)
        ws.close()

    threading.Thread(target=run).start()

if __name__ == "__main__":
    # WebSocket endpoint for public market data
    websocket_url = "wss://advanced-trade-ws.coinbase.com"
    print(f"Connecting to WebSocket: {websocket_url}")
    ws = websocket.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
