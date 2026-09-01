import time
import platform
import psutil
from datetime import datetime
from fastapi import APIRouter
from app.config import settings
from app.models.schemas import HealthResponse, SystemDiagnostics

router = APIRouter(tags=["Health & System"])
start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def get_health():
    """Retrieve service health status and uptime metrics."""
    return HealthResponse(
        status="operational",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow().isoformat() + "Z",
        uptime_seconds=round(time.time() - start_time, 2)
    )

@router.get("/system", response_model=SystemDiagnostics)
async def get_system_diagnostics():
    """Retrieve host system hardware utilization and specs."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return SystemDiagnostics(
        platform=f"{platform.system()} {platform.release()} ({platform.machine()})",
        python_version=platform.python_version(),
        cpu_percent=psutil.cpu_percent(interval=None),
        cpu_count=psutil.cpu_count(logical=True) or 1,
        memory_total_mb=round(mem.total / (1024 * 1024), 2),
        memory_available_mb=round(mem.available / (1024 * 1024), 2),
        memory_percent=mem.percent,
        disk_usage_percent=disk.percent
    )
