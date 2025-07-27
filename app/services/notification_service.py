"""
REVISED: The notification service now also writes all alerts to the
EventLog table in the database for persistent logging.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.core.gpio_controller import AsyncGPIOController
from app.models.event_log import EventLog, EventType

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class Alert(BaseModel):
    level: AlertLevel
    message: str
    details: Optional[Dict[str, Any]] = None

class AsyncNotificationService:
    def __init__(self, gpio_controller: AsyncGPIOController, db_session_factory):
        self._gpio = gpio_controller
        self._get_db_session = db_session_factory
        self._queue = asyncio.Queue(maxsize=100)
        self._worker_task: Optional[asyncio.Task] = None

    def start(self):
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._notification_worker())

    def stop(self):
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()

    async def send_alert(self, level: str, message: str, details: Optional[dict] = None):
        try:
            alert_level = AlertLevel(level.lower())
            alert = Alert(level=alert_level, message=message, details=details)
            self._queue.put_nowait(alert)
        except asyncio.QueueFull:
            print("Notification Service Warning: Alert queue is full. Dropping oldest alert.")
            await self._queue.get()
            await self._queue.put(alert)

    async def _notification_worker(self):
        while True:
            try:
                alert: Alert = await self._queue.get()
                print(f"Notification: [{alert.level.name}] {alert.message}")

                # Persist the log to the database
                await self._log_event_to_db(alert)

                # Handle physical notifications (LEDs, buzzer)
                if alert.level == AlertLevel.INFO:
                    asyncio.create_task(self._gpio.blink_led("led_green", on_time=0.2, off_time=0.2))
                elif alert.level == AlertLevel.WARNING:
                    asyncio.create_task(self._gpio.blink_led("led_red", on_time=0.5, off_time=0.5))
                elif alert.level >= AlertLevel.ERROR:
                    asyncio.create_task(self._gpio.blink_led("led_red", on_time=0.1, off_time=0.1))

                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in notification worker: {e}")

    async def _log_event_to_db(self, alert: Alert):
        try:
            async with self._get_db_session() as session:
                log_entry = EventLog(
                    event_type=EventType(alert.level.value),
                    source="SYSTEM", # Could be enhanced to be more specific
                    message=alert.message,
                    details=alert.details
                )
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            print(f"Failed to log event to database: {e}")
