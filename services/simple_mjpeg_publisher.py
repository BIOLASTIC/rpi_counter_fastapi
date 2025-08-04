#!/usr/bin/env python3
"""
Simple MJPEG Publisher for Raspberry Pi AI System
Reads an MJPEG stream from STDIN (rpicam-vid) and publishes each JPEG
frame to two Redis Pub/Sub channels:

    • camera:frames:rpi   – raw camera feed
    • ai_stream:frames:rpi – identical feed for your AI overlay service
"""

import sys
import time
import signal
from pathlib import Path

import redis


class SimpleMJPEGPublisher:
    # --------------------------------------------------------------------- #
    def __init__(self) -> None:
        self.running: bool = True
        self.frame_count: int = 0
        self.error_count: int = 0
        self._redis = None
        self._start = time.time()
        self._last_status = 0.0

        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    # ------------------------------------------------------------------ #
    # Graceful-shutdown handler
    def _stop(self, *_args) -> None:
        print("[MJPEG-Publisher] Stopping …")
        self.running = False

    # ------------------------------------------------------------------ #
    # Connect to local Redis (retry up to 5×)
    def _connect_redis(self, retries: int = 5) -> bool:
        attempt = 0
        while attempt < retries and self.running:
            try:
                self._redis = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=False,
                    socket_timeout=3,
                    socket_connect_timeout=3,
                )
                self._redis.ping()
                print("[MJPEG-Publisher] Connected to Redis ✔")
                return True
            except Exception as exc:  # pragma: no cover
                attempt += 1
                print(
                    f"[MJPEG-Publisher] Redis connect {attempt}/{retries} failed: {exc}"
                )
                time.sleep(2)
        return False

    # ------------------------------------------------------------------ #
    # Read **one** complete JPEG from STDIN (detect SOI/EOI markers)
    def _read_frame(self) -> bytes | None:
        data = b""
        soi_seen = False
        while self.running:
            byte = sys.stdin.buffer.read(1)
            if not byte:
                # End-of-stream
                return data if data else None

            data += byte

            if not soi_seen and data[-2:] == b"\xff\xd8":  # SOI
                soi_seen = True
                data = b"\xff\xd8"
                continue

            if soi_seen and data[-2:] == b"\xff\xd9":  # EOI
                return data

            if len(data) > 1_048_576:  # 1 MiB safety-limit
                print("[MJPEG-Publisher] Frame >1 MiB – discarded")
                return None

    # ------------------------------------------------------------------ #
    # Main loop
    def run(self) -> int:
        if not self._connect_redis():
            print("[MJPEG-Publisher] Exiting – no Redis")
            return 1

        print("[MJPEG-Publisher] Started – waiting for MJPEG bytes …")

        while self.running:
            frame = self._read_frame()
            if frame is None:  # EOF or oversized frame
                continue

            self.frame_count += 1
            try:
                self._redis.publish("camera:frames:rpi", frame)
                self._redis.publish("ai_stream:frames:rpi", frame)
            except Exception as exc:
                self.error_count += 1
                print(f"[MJPEG-Publisher] Redis publish error ({exc})")
                if not self._connect_redis(1):  # quick retry
                    break

            # Status every 30 s
            now = time.time()
            if now - self._last_status >= 30:
                fps = self.frame_count / max(now - self._start, 1e-3)
                print(
                    f"[MJPEG-Publisher] {self.frame_count} frames  "
                    f"{fps:.1f} FPS  errors {self.error_count}"
                )
                self._last_status = now

        print(
            f"[MJPEG-Publisher] Done – sent {self.frame_count} frames "
            f"with {self.error_count} errors"
        )
        return 0


# ------------------------------------------------------------------------- #
if __name__ == "__main__":
    sys.exit(SimpleMJPEGPublisher().run())
