# rpi_counter_fastapi-dev_new/app/schemas/reports.py

from pydantic import BaseModel
from typing import List, Optional
from .run_log import RunLogOut

class ReportKPIs(BaseModel):
    """Key Performance Indicators for the summary report."""
    total_runs: int
    completed_runs: int
    aborted_runs: int
    failed_runs: int
    success_rate: float # as a percentage
    
class ProductionSummaryReport(BaseModel):
    """The complete payload for the production summary report."""
    kpis: ReportKPIs
    runs: List[RunLogOut]