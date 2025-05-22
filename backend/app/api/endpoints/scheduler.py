"""
Scheduler endpoints for data collection jobs
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_async_session
from app.services.scheduler_service import scheduler

logger = structlog.get_logger()

router = APIRouter()


@router.get("/jobs/")
async def get_scheduled_jobs() -> List[Dict[str, Any]]:
    """Get all scheduled data collection jobs"""
    try:
        jobs = scheduler.list_jobs()
        logger.info("Retrieved scheduled jobs", count=len(jobs))
        return jobs
    except Exception as e:
        logger.error("Failed to get scheduled jobs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve scheduled jobs")


@router.get("/jobs/{job_id}")
async def get_scheduled_job(job_id: str) -> Dict[str, Any]:
    """Get specific scheduled job details"""
    try:
        job = scheduler.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Scheduled job not found")
        
        logger.info("Retrieved scheduled job", job_id=job_id)
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve scheduled job")


@router.post("/jobs/{job_id}/run")
async def run_job_now(job_id: str) -> Dict[str, Any]:
    """Run a scheduled job immediately"""
    try:
        logger.info("Running scheduled job on demand", job_id=job_id)
        result = await scheduler.run_job_now(job_id)
        logger.info("Scheduled job completed", job_id=job_id, result=result)
        return result
    except ValueError as e:
        logger.warning("Job not found", job_id=job_id)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to run scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to run job: {str(e)}")


@router.post("/jobs/")
async def create_scheduled_job(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new scheduled job"""
    try:
        required_fields = ["name", "client_class", "config", "interval_minutes", "tenant_id"]
        for field in required_fields:
            if field not in job_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        job_id = scheduler.add_job(
            name=job_data["name"],
            client_class=job_data["client_class"],
            config=job_data["config"],
            interval_minutes=job_data["interval_minutes"],
            tenant_id=job_data["tenant_id"],
            enabled=job_data.get("enabled", True)
        )
        
        logger.info("Created new scheduled job", job_id=job_id, name=job_data["name"])
        
        # Return the created job
        return scheduler.get_job(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create scheduled job", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.patch("/jobs/{job_id}")
async def update_scheduled_job(job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update scheduled job"""
    try:
        job = scheduler.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Scheduled job not found")
        
        # Update job enabled status if provided
        if "enabled" in job_data:
            if job_data["enabled"]:
                scheduler.enable_job(job_id)
            else:
                scheduler.disable_job(job_id)
        
        logger.info("Updated scheduled job", job_id=job_id)
        
        # Return updated job
        return scheduler.get_job(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to update job: {str(e)}")


@router.delete("/jobs/{job_id}")
async def delete_scheduled_job(job_id: str) -> Dict[str, str]:
    """Delete scheduled job"""
    try:
        success = scheduler.remove_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Scheduled job not found")
        
        logger.info("Deleted scheduled job", job_id=job_id)
        return {"message": f"Job {job_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")


@router.post("/jobs/{job_id}/enable")
async def enable_job(job_id: str) -> Dict[str, Any]:
    """Enable a scheduled job"""
    try:
        success = scheduler.enable_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Scheduled job not found")
        
        logger.info("Enabled scheduled job", job_id=job_id)
        return scheduler.get_job(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to enable scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to enable job: {str(e)}")


@router.post("/jobs/{job_id}/disable")
async def disable_job(job_id: str) -> Dict[str, Any]:
    """Disable a scheduled job"""
    try:
        success = scheduler.disable_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Scheduled job not found")
        
        logger.info("Disabled scheduled job", job_id=job_id)
        return scheduler.get_job(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to disable scheduled job", job_id=job_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to disable job: {str(e)}")


@router.get("/status")
async def get_scheduler_status() -> Dict[str, Any]:
    """Get scheduler service status"""
    try:
        jobs = scheduler.list_jobs()
        enabled_jobs = [job for job in jobs if job.get("enabled", False)]
        
        return {
            "status": "running" if scheduler.running else "stopped",
            "total_jobs": len(jobs),
            "enabled_jobs": len(enabled_jobs),
            "disabled_jobs": len(jobs) - len(enabled_jobs),
            "jobs": jobs
        }
    except Exception as e:
        logger.error("Failed to get scheduler status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get scheduler status")