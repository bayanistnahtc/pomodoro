from fastapi import Depends

from cache import get_redis_connection
from database import get_db_session
from repository import TaskCache, TaskRepository
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_tasks_service(
        task_cache: TaskCache = Depends(get_tasks_cache_repository),
        task_repository: TaskRepository = Depends(get_tasks_repository)
) -> TaskService:
    return TaskService(
        task_cache=task_cache,
        task_repository=task_repository
    )
