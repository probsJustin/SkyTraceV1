"""
Scheduler Service for Data Collection Jobs
Manages cron-like scheduling for data collection clients
"""
import asyncio
import importlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from uuid import uuid4, UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.tenant import Tenant as TenantModel

logger = structlog.get_logger()


class ScheduledJob:
    """Represents a scheduled data collection job"""
    
    def __init__(
        self,
        job_id: str,
        name: str,
        client_class: str,
        config: Dict[str, Any],
        interval_minutes: int,
        tenant_id: str,
        enabled: bool = True
    ):
        self.job_id = job_id
        self.name = name
        self.client_class = client_class
        self.config = config
        self.interval_minutes = interval_minutes
        self.tenant_id = tenant_id
        self.enabled = enabled
        
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0
        self.error_count = 0
        self.last_error: Optional[str] = None
        
        self._calculate_next_run()
    
    def _calculate_next_run(self):
        """Calculate when this job should run next"""
        if self.last_run:
            self.next_run = self.last_run + timedelta(minutes=self.interval_minutes)
        else:
            # First run - schedule for now
            self.next_run = datetime.utcnow()
    
    def is_due(self) -> bool:
        """Check if this job is due to run"""
        if not self.enabled:
            return False
        return self.next_run and datetime.utcnow() >= self.next_run
    
    def mark_completed(self, success: bool = True, error: Optional[str] = None):
        """Mark job as completed"""
        self.last_run = datetime.utcnow()
        self.run_count += 1
        
        if success:
            self.last_error = None
        else:
            self.error_count += 1
            self.last_error = error
        
        self._calculate_next_run()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary"""
        return {
            "job_id": self.job_id,
            "name": self.name,
            "client_class": self.client_class,
            "config": self.config,
            "interval_minutes": self.interval_minutes,
            "tenant_id": self.tenant_id,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "error_count": self.error_count,
            "last_error": self.last_error
        }


class SchedulerService:
    """Service for managing scheduled data collection jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, ScheduledJob] = {}
        self.running = False
        self.logger = logger.bind(service="SchedulerService")
        
        # Register default jobs
        self._register_default_jobs()
    
    def _register_default_jobs(self):
        """Register default data collection jobs"""
        # ADSBExchange military aircraft job with archive-and-refresh
        adsbexchange_job = ScheduledJob(
            job_id="adsbexchange-military",
            name="ADSBExchange Military Aircraft",
            client_class="app.clients.data_collectors.adsbexchange_client.ADSBExchangeClient",
            config={
                "rapidapi_key": settings.ADSBEXCHANGE_RAPIDAPI_KEY,
                "endpoint": "/v2/mil/",
                "timeout": 30,
                "use_archive_refresh": True  # Enable archive-and-refresh mode
            },
            interval_minutes=30,  # Every 30 minutes
            tenant_id="default"
        )
        
        self.jobs[adsbexchange_job.job_id] = adsbexchange_job
        
        self.logger.info("Registered default data collection jobs", count=len(self.jobs))
    
    async def _load_client_class(self, client_class_path: str):
        """Dynamically load a client class"""
        try:
            module_path, class_name = client_class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            client_class = getattr(module, class_name)
            return client_class
        except Exception as e:
            self.logger.error("Failed to load client class", 
                            client_class=client_class_path, error=str(e))
            raise
    
    async def _run_job(self, job: ScheduledJob):
        """Run a single data collection job"""
        self.logger.info("Starting data collection job", 
                        job_id=job.job_id, job_name=job.name)
        
        try:
            # Load the client class
            client_class = await self._load_client_class(job.client_class)
            
            # Create client instance
            client = client_class(job.config)
            
            # Execute the complete workflow if database is available
            if AsyncSessionLocal:
                try:
                    async with AsyncSessionLocal() as session:
                        # Get tenant UUID from tenant_id string
                        if isinstance(job.tenant_id, str):
                            # Look up tenant by slug/name or use default
                            tenant_result = await session.execute(
                                select(TenantModel).where(TenantModel.slug == job.tenant_id)
                            )
                            tenant = tenant_result.scalar_one_or_none()
                            if tenant:
                                tenant_uuid = tenant.id
                            else:
                                # Create default tenant if it doesn't exist
                                default_tenant = TenantModel(
                                    name="Default Organization",
                                    slug="default",
                                    description="Default tenant for data collection"
                                )
                                session.add(default_tenant)
                                await session.commit()
                                await session.refresh(default_tenant)
                                tenant_uuid = default_tenant.id
                        else:
                            tenant_uuid = job.tenant_id
                        
                        # Check if we should use archive-and-refresh mode
                        use_archive_refresh = job.config.get("use_archive_refresh", False)
                        
                        # Let the client handle the entire fetch and store workflow
                        result = await client.fetch_and_store_data(session, tenant_uuid, use_archive_refresh)
                        
                        if result["success"]:
                            self.logger.info(
                                "Data collection job completed successfully",
                                job_id=job.job_id,
                                **{k: v for k, v in result.items() if k != "success"}
                            )
                        else:
                            self.logger.error(
                                "Data collection job failed",
                                job_id=job.job_id,
                                error=result.get("error", "Unknown error")
                            )
                            raise Exception(result.get("error", "Job failed"))
                            
                except Exception as e:
                    self.logger.error("Failed to execute data collection job",
                                    job_id=job.job_id, error=str(e))
                    raise
            else:
                self.logger.warning("Database not available - cannot run data collection job", 
                                  job_id=job.job_id)
                raise Exception("Database not available")
            
            job.mark_completed(success=True)
            
        except Exception as e:
            error_msg = f"Job failed: {str(e)}"
            self.logger.error("Data collection job failed", 
                            job_id=job.job_id, error=error_msg)
            job.mark_completed(success=False, error=error_msg)
    
    async def run_job_now(self, job_id: str) -> Dict[str, Any]:
        """Run a specific job immediately"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        await self._run_job(job)
        
        return {
            "job_id": job_id,
            "status": "completed",
            "last_run": job.last_run.isoformat() if job.last_run else None,
            "success": job.last_error is None
        }
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        self.logger.info("Scheduler loop started")
        
        while self.running:
            try:
                # Check all jobs
                for job in self.jobs.values():
                    if job.is_due():
                        try:
                            await self._run_job(job)
                        except Exception as e:
                            self.logger.error("Error running scheduled job", 
                                            job_id=job.job_id, error=str(e))
                
                # Sleep for 1 minute before checking again
                await asyncio.sleep(60)
                
            except Exception as e:
                self.logger.error("Error in scheduler loop", error=str(e))
                await asyncio.sleep(60)  # Wait before retrying
    
    async def start(self):
        """Start the scheduler"""
        if self.running:
            self.logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.logger.info("Starting data collection scheduler")
        
        # Start the scheduler loop in background
        asyncio.create_task(self._scheduler_loop())
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        self.logger.info("Stopped data collection scheduler")
    
    def add_job(
        self,
        name: str,
        client_class: str,
        config: Dict[str, Any],
        interval_minutes: int,
        tenant_id: str,
        enabled: bool = True
    ) -> str:
        """Add a new scheduled job"""
        job_id = str(uuid4())
        
        job = ScheduledJob(
            job_id=job_id,
            name=name,
            client_class=client_class,
            config=config,
            interval_minutes=interval_minutes,
            tenant_id=tenant_id,
            enabled=enabled
        )
        
        self.jobs[job_id] = job
        
        self.logger.info("Added new scheduled job", 
                        job_id=job_id, name=name, interval=interval_minutes)
        
        return job_id
    
    def remove_job(self, job_id: str) -> bool:
        """Remove a scheduled job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            self.logger.info("Removed scheduled job", job_id=job_id)
            return True
        return False
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job information"""
        job = self.jobs.get(job_id)
        return job.to_dict() if job else None
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all scheduled jobs"""
        return [job.to_dict() for job in self.jobs.values()]
    
    def enable_job(self, job_id: str) -> bool:
        """Enable a job"""
        if job_id in self.jobs:
            self.jobs[job_id].enabled = True
            return True
        return False
    
    def disable_job(self, job_id: str) -> bool:
        """Disable a job"""
        if job_id in self.jobs:
            self.jobs[job_id].enabled = False
            return True
        return False


# Global scheduler instance
scheduler = SchedulerService()