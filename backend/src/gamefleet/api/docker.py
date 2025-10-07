from fastapi import APIRouter
import docker

router = APIRouter()
client = docker.from_env()

@router.get("/containers")
def list_containers():
    containers = client.containers.list(all=True)
    return [
        {"id": c.id, "name": c.name, "status": c.status, "image": c.image.tags}
        for c in containers
    ]

@router.post("/start/{container_id}")
def start_container(container_id: str):
    container = client.containers.get(container_id)
    container.start()
    return {"status": "started", "id": container_id}
