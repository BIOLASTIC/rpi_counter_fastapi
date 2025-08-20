# rpi_counter_fastapi-apintrigation/app/api/v1/analytics.py

import asyncio
from fastapi import APIRouter, Depends, Query, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timedelta, time
import json
import io
import csv
import httpx
from pathlib import Path

from app.models import get_async_session, RunLog, DetectionEventLog, Product, Operator, RunStatus
from config import settings

router = APIRouter()

@router.post("/qc-test/upload")
async def handle_qc_test_upload(
    image: UploadFile = File(...),
    models: List[str] = Form(...)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_bytes = await image.read()
    
    async with httpx.AsyncClient(base_url=settings.AI_API.BASE_URL, timeout=20.0) as client:
        tasks = []
        for model_id in models:
            files = {"image": (image.filename, image_bytes, image.content_type)}
            data = {"model_id": model_id, "serial_no": "MANUAL_TEST"}
            task = client.post("/predict", files=files, data=data)
            tasks.append(task)
        
        try:
            responses = await asyncio.gather(*tasks)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Could not connect to the AI service: {e}")

    results = {}
    for response in responses:
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI service returned an error: {response.text}"
            )
        data = response.json()
        model_id = data.get("model_id")
        results[model_id] = data

    return results

@router.get("/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
    run_query = (
        select(RunLog)
        .options(
            selectinload(RunLog.detection_events), 
            selectinload(RunLog.product),
            selectinload(RunLog.operator)
        )
        .order_by(RunLog.start_timestamp.asc())
    )
    
    if start_date: run_query = run_query.where(RunLog.start_timestamp >= start_date)
    if end_date: run_query = run_query.where(RunLog.start_timestamp <= end_date)
    if operator_id: run_query = run_query.where(RunLog.operator_id == operator_id)
    if product_id: run_query = run_query.where(RunLog.product_id == product_id)
    
    run_results = await db.execute(run_query)
    runs_in_period = run_results.scalars().unique().all()
    run_ids_in_period = {r.id for r in runs_in_period}

    detections_in_period = []
    if run_ids_in_period:
        detection_query = (
            select(DetectionEventLog)
            .where(DetectionEventLog.run_log_id.in_(run_ids_in_period))
            .options(selectinload(DetectionEventLog.run).selectinload(RunLog.product))
        )
        detection_results = await db.execute(detection_query)
        detections_in_period = detection_results.scalars().all()

    total_runs = len(runs_in_period)
    completed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for r in runs_in_period if r.status == RunStatus.FAILED)
    aborted_runs = sum(1 for r in runs_in_period if r.status == RunStatus.ABORTED)
    total_items = len(detections_in_period)

    total_run_time_seconds = sum(
        (r.end_timestamp - r.start_timestamp).total_seconds() 
        for r in runs_in_period if r.end_timestamp and r.start_timestamp
    )
    
    # --- THIS IS THE FIX ---
    # Initialize date-dependent values to 0 and only calculate if dates are provided.
    availability = 0
    planned_downtime_sec = 0
    unplanned_downtime_sec = 0
    daily_trends = {}
    
    if start_date and end_date:
        total_period_seconds = (end_date - start_date).total_seconds()
        availability = (total_run_time_seconds / total_period_seconds) * 100 if total_period_seconds > 0 else 0
        
        # Downtime Analysis
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
        
        # Daily Trend Analysis
        delta = end_date.date() - start_date.date()
        for i in range(delta.days + 1):
            day = start_date.date() + timedelta(days=i)
            daily_trends[day.isoformat()] = {"items": 0, "pass": 0, "fail": 0}
    # --- END OF FIX ---
    
    performance = (total_items / (total_run_time_seconds / 3600)) if total_run_time_seconds > 0 else 0

    for det in detections_in_period:
        day_str = det.timestamp.date().isoformat()
        if day_str in daily_trends:
            daily_trends[day_str]["items"] += 1
            if det.details:
                qc_summary = det.details.get("qc_summary", {})
                if qc_summary.get("overall_status") == "ACCEPT":
                    daily_trends[day_str]["pass"] += 1
                elif qc_summary.get("overall_status") == "REJECT":
                    daily_trends[day_str]["fail"] += 1

    for day, data in daily_trends.items():
        total_qc = data["pass"] + data["fail"]
        daily_trends[day]["pass_rate"] = (data["pass"] / total_qc * 100) if total_qc > 0 else 0

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
            qc_summary = detection.details.get("qc_summary", {})
            if qc_summary.get("overall_status") == "ACCEPT":
                qc_pass += 1
            elif qc_summary.get("overall_status") == "REJECT":
                qc_fail += 1
            
            defects_summary = detection.details.get("defects_summary", {})
            for defect_type, count in defects_summary.get("defect_counts", {}).items():
                defect_counts[defect_type] = defect_counts.get(defect_type, 0) + count

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

# (The /export-csv endpoint is unchanged and remains here)
@router.get("/export-csv")
async def export_analytics_csv(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
):
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
    
    writer.writerow([
        "DetectionTimestamp", "SerialNumber", "RunID", "BatchCode", "Operator", "Product",
        "QC_Status", "DetectedCategory", "DetectedSize", "DefectCount", "ImagePath"
    ])
    
    for det in detections:
        qc_summary = det.details.get("qc_summary", {}) if det.details else {}
        category_summary = det.details.get("category_summary", {}) if det.details else {}
        size_summary = det.details.get("size_summary", {}) if det.details else {}
        defects_summary = det.details.get("defects_summary", {}) if det.details else {}

        writer.writerow([
            det.timestamp.isoformat(), det.serial_number, det.run.id, det.run.batch_code,
            det.run.operator.name if det.run.operator else "N/A",
            det.run.product.name if det.run.product else "N/A",
            qc_summary.get("overall_status", "N/A"),
            category_summary.get("detected_type", "N/A"),
            size_summary.get("detected_size", "N/A"),
            defects_summary.get("total_defects", 0),
            det.image_path
        ])

    output.seek(0)
    
    filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )