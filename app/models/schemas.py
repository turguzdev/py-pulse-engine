from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NodeCreate(BaseModel):
    name: str = Field(..., description="Node hostname or identifier", min_length=2, max_length=50)
    region: str = Field(default="eu-central-1", description="Deployment region")
    role: str = Field(default="worker", description="Cluster role: worker, master, gateway")
    tags: Optional[List[str]] = Field(default_factory=list, description="Categorization tags")

class NodeResponse(BaseModel):
    id: str
    name: str
    region: str
    role: str
    status: str
    cpu_cores: int
    memory_gb: float
    tags: List[str]
    uptime_hours: float
    created_at: str

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str
    uptime_seconds: float

class SystemDiagnostics(BaseModel):
    platform: str
    python_version: str
    cpu_percent: float
    cpu_count: int
    memory_total_mb: float
    memory_available_mb: float
    memory_percent: float
    disk_usage_percent: float
