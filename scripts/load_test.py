#!/usr/bin/env python
"""
A simple asynchronous load testing script.
This script bombards an endpoint with concurrent requests to measure performance.
Requires httpx: pip install httpx
"""
import asyncio
import time
import httpx

# --- Configuration ---
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/system/status" # A lightweight endpoint is good for this
NUM_REQUESTS = 500
CONCURRENCY = 50

async def fetch(client: httpx.AsyncClient):
    """Sends a single GET request."""
    try:
        response = await client.get(f"{BASE_URL}{ENDPOINT}")
        response.raise_for_status()
        return response.status_code
    except httpx.RequestError as e:
        return e

async def run_load_test():
    """Runs the load test with the specified concurrency."""
    print(f"--- Starting Load Test ---")
    print(f"URL: {BASE_URL}{ENDPOINT}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    print("--------------------------")

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        
        async def concurrent_fetch():
            async with semaphore:
                return await fetch(client)

        start_time = time.monotonic()
        tasks = [concurrent_fetch() for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_time = time.monotonic()

    total_time = end_time - start_time
    successful_requests = sum(1 for r in results if isinstance(r, int) and r == 200)
    failed_requests = NUM_REQUESTS - successful_requests
    requests_per_second = successful_requests / total_time if total_time > 0 else 0

    print("\n--- Load Test Results ---")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second (RPS): {requests_per_second:.2f}")
    print("-------------------------")

if __name__ == "__main__":
    asyncio.run(run_load_test())
