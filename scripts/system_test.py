#!/usr/bin/env python
"""
An end-to-end test script for the Box Counter System.
This script simulates a full workflow by interacting with the running
application's API and WebSocket endpoints.

Requires:
- pip install httpx websockets
- The main application must be running.
- APP_ENV must be set to 'development' for the debug endpoint to be active.
"""
import asyncio
import httpx
import websockets
import json

BASE_URL = "http://localhost:8000"
WEBSOCKET_URL = "ws://localhost:8000/ws"

API_HEADERS = {"Content-Type": "application/json"}
# This should match the API_KEY in your .env file
PROTECTED_API_HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": "your_secret_api_key_here" 
}

async def trigger_sensor(sensor_id: int, state: str):
    """Calls the debug API to simulate a sensor event."""
    async with httpx.AsyncClient() as client:
        print(f"TEST: Triggering Sensor {sensor_id} -> {state}")
        payload = {"sensor_id": sensor_id, "new_state": state}
        try:
            res = await client.post(f"{BASE_URL}/api/v1/debug/sensor-event", json=payload, headers=API_HEADERS)
            res.raise_for_status()
            print(f"  -> API Response: {res.json()}")
        except httpx.RequestError as e:
            print(f"FATAL: Could not trigger sensor. Is the app running in 'development' mode?")
            print(f"  -> {e}")
            exit(1)

async def run_test_sequence():
    """Executes the full end-to-end test sequence."""
    print("--- Starting End-to-End System Test ---")

    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✓ WebSocket connection established.")

            # 1. Simulate a full box detection cycle
            print("\n--- Simulating Box Detection ---")
            await trigger_sensor(1, "triggered") # Box enters
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "triggered") # Box reaches end
            await asyncio.sleep(0.1)
            await trigger_sensor(1, "cleared")   # Box leaves first sensor (COUNT!)
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "cleared")   # Box fully exits
            
            # 2. Listen on WebSocket for count update
            print("\n--- Waiting for WebSocket update... ---")
            count_updated = False
            try:
                async for message in websocket:
                    data = json.loads(message)
                    if data.get("type") == "detection_status" and data["data"]["count"] >= 1:
                        print(f"✓ SUCCESS: WebSocket reported new count: {data['data']['count']}")
                        count_updated = True
                        break # Exit the listener loop
                    # Timeout to prevent infinite loop
                    # This is a simplified listener for the test
                    await asyncio.sleep(0.1) # Yield control
            except asyncio.TimeoutError:
                print("✗ FAILURE: Timed out waiting for WebSocket count update.")

            if not count_updated:
                # If the specific message wasn't received after a short while
                print("✗ FAILURE: Did not receive expected WebSocket message.")

            # 3. Reset the counter via API
            print("\n--- Testing Counter Reset API ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/detection/reset", headers=API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Reset API returned OK.")
                else:
                    print(f"✗ FAILURE: Reset API failed with status {res.status_code}")

            # 4. Test a protected endpoint (Emergency Stop)
            print("\n--- Testing Protected API Endpoint (Emergency Stop) ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/system/emergency-stop", headers=PROTECTED_API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Protected endpoint returned OK.")
                else:
                    print(f"✗ FAILURE: Protected endpoint failed with status {res.status_code}. Check your API Key.")

    except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError) as e:
        print("\n✗ FATAL: Could not connect to the application.")
        print("Please ensure the FastAPI server is running before executing this test.")
        return

    print("\n--- End-to-End System Test Finished ---")

if __name__ == "__main__":
    asyncio.run(run_test_sequence())
