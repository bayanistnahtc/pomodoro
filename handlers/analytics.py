from fastapi import APIRouter


router = APIRouter(prefix="/analytics", tags=["task"])


@router.get("/task/{task_id}")
async def get_task(task_id):
    return {"task_id": task_id}


@router.post("/tasks")
async def get_tasks():
    return []
