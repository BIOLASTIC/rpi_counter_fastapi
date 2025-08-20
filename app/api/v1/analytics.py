from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timedelta, time
import json
import io
import csv

from app.models import get_async_session, RunLog, DetectionEventLog, Product, Operator, RunStatus

router = APIRouter()

@router.get("/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
    """
    Generates a comprehensive analytics report for a given date range with optional filters.
    """
    # 1. Base Query for Runs in the selected period
    run_query = (
        select(RunLog)
        .options(
            selectinload(RunLog.detection_events), 
            selectinload(RunLog.product),
            selectinload(RunLog.operator)
        )
        .order_by(RunLog.start_timestamp.asc()) # Order chronologically for downtime calculation
    )
    
    # Apply filters
    if start_date: run_query = run_query.where(RunLog.start_timestamp >= start_date)
    if end_date: run_query = run_query.where(RunLog.start_timestamp <= end_date)
    if operator_id: run_query = run_query.where(RunLog.operator_id == operator_id)
    if product_id: run_query = run_query.where(RunLog.product_id == product_id)
    
    run_results = await db.execute(run_query)
    runs_in_period = run_results.scalars().unique().all()

    # Create a set of run IDs for efficient filtering of detections
    run_ids_in_period = {r.id for r in runs_in_period}

    # 2. Base Query for Detections based on the filtered runs
    detections_in_period = []
    if run_ids_in_period:
        detection_query = (
            select(DetectionEventLog)
            .where(DetectionEventLog.run_log_id.in_(run_ids_in_period))
            .options(selectinload(DetectionEventLog.run).selectinload(RunLog.product))
        )
        detection_results = await db.execute(detection_query)
        detections_in_period = detection_results.scalars().all()

    # --- KPI & OEE-Lite Calculations ---
    total_runs = len(runs_in_period)
    completed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.FAILED)
    aborted_runs = sum(1 for r in runs_in_period if r.status == RunStatus.ABORTED)
    total_items = len(detections_in_period)

    total_run_time_seconds = sum(
        (r.end_timestamp - r.start_timestamp).total_seconds() 
        for r in runs_in_period if r.end_timestamp and r.start_timestamp
    )
    
    total_period_seconds = (end_date - start_date).total_seconds() if start_date and end_date else 0
    availability = (total_run_time_seconds / total_period_seconds) * 100 if total_period_seconds > 0 else 0
    performance = (total_items / (total_run_time_seconds / 3600)) if total_run_time_seconds > 0 else 0

    # --- Downtime Analysis ---
    planned_downtime_sec = 0
    unplanned_downtime_sec = 0
    for i in range(len(runs_in_period) - 1):
        current_run = runs_in_period[i]
        next_run = runs_in_period[i+1]
        if current_run.end_timestamp and next_run.start_timestamp:
            gap = (next_run.start_timestamp - current_run.end_timestamp).total_seconds()
            if gap > 0:
                if current_run.status == RunStatus.COMPLETED:
                    planned_downtime_sec += gap
                else: # FAILED or ABORTED
                    unplanned_downtime_sec += gap

    # --- Daily Trend Analysis ---
    daily_trends = {}
    if start_date and end_date:
        delta = end_date.date() - start_date.date()
        for i in range(delta.days + 1):
            day = start_date.date() + timedelta(days=i)
            daily_trends[day.isoformat()] = {"items": 0, "pass": 0, "fail": 0}

    for det in detections_in_period:
        day_str = det.timestamp.date().isoformat()
        if day_str in daily_trends:
            daily_trends[day_str]["items"] += 1
            if det.details:
                qc_status = det.details.get("identification_results", {}).get("qc", {}).get("overall_status")
                if qc_status == "ACCEPT": daily_trends[day_str]["pass"] += 1
                elif qc_status == "REJECT": daily_trends[day_str]["fail"] += 1

    for day, data in daily_trends.items():
        total_qc = data["pass"] + data["fail"]
        daily_trends[day]["pass_rate"] = (data["pass"] / total_qc * 100) if total_qc > 0 else 0


    # --- Chart and Table Data ---
    hourly_counts = {f"{h:02d}": 0 for h in range(24)}
    for detection in detections_in_period:
        hour = detection.timestamp.strftime('%H')
        hourly_counts[hour] += 1

    product_counts = {}
    for detection in detections_in_period:
        if detection.run and detection.run.product:
            product_name = detection.run.product.name
            product_counts[product_name] = product_counts.get(product_name, 0) + 1
    
    top_products = sorted(product_counts.items(), key=lambda item: item[1], reverse=True)[:5]

    qc_pass, qc_fail, defect_counts = 0, 0, {}
    for detection in detections_in_period:
        if detection.details:
            qc_status = detection.details.get("identification_results", {}).get("qc", {}).get("overall_status")
            if qc_status == "ACCEPT": qc_pass += 1
            elif qc_status == "REJECT": qc_fail += 1
            
            defects = detection.details.get("identification_results", {}).get("defects", {}).get("defects", [])
            for defect in defects:
                defect_type = defect.get("defect_type", "Unknown")
                defect_counts[defect_type] = defect_counts.get(defect_type, 0) + 1
    
    top_defects = sorted(defect_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    
    return {
        "kpis": {
            "total_runs": total_runs, "completed_runs": completed_runs, "failed_runs": failed_runs,
            "aborted_runs": aborted_runs, "total_items_detected": total_items,
            "quality_pass_rate": (qc_pass / (qc_pass + qc_fail)) * 100 if (qc_pass + qc_fail) > 0 else 0,
        },
        "oee_lite": {
            "availability": availability,
            "performance_items_per_hour": performance,
        },
        "downtime": {
            "planned_changeover_hours": planned_downtime_sec / 3600,
            "unplanned_downtime_hours": unplanned_downtime_sec / 3600,
        },
        "daily_trends": daily_trends,
        "hourly_throughput": hourly_counts,
        "product_counts": product_counts,
        "top_5_products": top_products,
        "quality_control": { "pass_count": qc_pass, "fail_count": qc_fail, "top_5_defects": top_defects }
    }


@router.get("/export-csv")
async def export_analytics_csv(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
    """
    Exports detailed run and detection logs to a CSV file based on filters.
    """
    query = (
        select(DetectionEventLog)
        .join(RunLog)
        .options(
            selectinload(DetectionEventLog.run).selectinload(RunLog.product),
            selectinload(DetectionEventLog.run).selectinload(RunLog.operator)
        )
        .order_by(DetectionEventLog.timestamp.desc())
    )
    if start_date: query = query.where(RunLog.start_timestamp >= start_date)
    if end_date: query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id: query = query.where(RunLog.operator_id == operator_id)
    if product_id: query = query.where(RunLog.product_id == product_id)
    
    results = await db.execute(query)
    detections = results.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write Header
    writer.writerow([
        "DetectionTimestamp", "SerialNumber", "RunID", "BatchCode", "Operator", "Product",
        "QC_Status", "DetectedCategory", "DetectedSize", "DefectCount", "ImagePath"
    ])
    
    # Write Data
    for det in detections:
        qc_details = det.details.get("identification_results", {}) if det.details else {}
        qc_status = qc_details.get("qc", {}).get("overall_status", "N/A")
        category = qc_details.get("category", {}).get("detected_product_type", "N/A")
        size = qc_details.get("size", {}).get("detected_size", "N/A")
        defect_count = len(qc_details.get("defects", {}).get("defects", []))

        writer.writerow([
            det.timestamp.isoformat(), det.serial_number, det.run.id, det.run.batch_code,
            det.run.operator.name if det.run.operator else "N/A",
            det.run.product.name if det.run.product else "N/A",
            qc_status, category, size, defect_count, det.image_path
        ])

    output.seek(0)
    
    filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )