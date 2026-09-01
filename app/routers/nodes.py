import uuid
import random
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import NodeCreate, NodeResponse

router = APIRouter(prefix="/nodes", tags=["Cluster Nodes"])

# Initial in-memory cluster nodes
_nodes_db = [
    {
        "id": "node-alpha-01",
        "name": "pulse-edge-frankfurt",
        "region": "eu-central-1",
        "role": "master",
        "status": "online",
        "cpu_cores": 16,
        "memory_gb": 64.0,
        "tags": ["primary", "control-plane", "k8s"],
        "uptime_hours": 142.5,
        "created_at": "2026-08-25T10:00:00Z"
    },
    {
        "id": "node-beta-02",
        "name": "pulse-worker-virginia",
        "region": "us-east-1",
        "role": "worker",
        "status": "online",
        "cpu_cores": 32,
        "memory_gb": 128.0,
        "tags": ["compute", "gpu-accelerated", "inference"],
        "uptime_hours": 88.2,
        "created_at": "2026-08-28T14:30:00Z"
    },
    {
        "id": "node-gamma-03",
        "name": "pulse-gateway-tokyo",
        "region": "ap-northeast-1",
        "role": "gateway",
        "status": "online",
        "cpu_cores": 8,
        "memory_gb": 32.0,
        "tags": ["edge", "cdn", "traffic"],
        "uptime_hours": 210.1,
        "created_at": "2026-08-20T08:15:00Z"
    }
]

@router.get("", response_model=List[NodeResponse])
async def list_nodes(region: Optional[str] = None, role: Optional[str] = None):
    """List all connected cluster nodes with optional filtering."""
    results = _nodes_db
    if region:
        results = [n for n in results if n["region"].lower() == region.lower()]
    if role:
        results = [n for n in results if n["role"].lower() == role.lower()]
    return results

@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str):
    """Retrieve details for a specific node."""
    for node in _nodes_db:
        if node["id"] == node_id:
            return node
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node '{node_id}' not found.")

@router.post("", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
async def register_node(payload: NodeCreate):
    """Register and provision a new node into the cluster."""
    node_id = f"node-{uuid.uuid4().hex[:8]}"
    new_node = {
        "id": node_id,
        "name": payload.name,
        "region": payload.region,
        "role": payload.role,
        "status": "online",
        "cpu_cores": random.choice([8, 16, 32, 64]),
        "memory_gb": float(random.choice([16, 32, 64, 128])),
        "tags": payload.tags or ["auto-provisioned"],
        "uptime_hours": 0.1,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    _nodes_db.append(new_node)
    return new_node

@router.delete("/{node_id}", status_code=status.HTTP_200_OK)
async def decommission_node(node_id: str):
    """Decommission and remove a node from the cluster."""
    global _nodes_db
    initial_len = len(_nodes_db)
    _nodes_db = [n for n in _nodes_db if n["id"] != node_id]
    if len(_nodes_db) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node '{node_id}' not found.")
    return {"success": True, "message": f"Node '{node_id}' decommissioned successfully."}
