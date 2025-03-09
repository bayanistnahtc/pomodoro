from dataclasses import dataclass
from repository import TaskCache, TaskRepository
from schema.task import TaskSchema


@dataclass
class TaskService:
    task_cache: TaskCache
    task_repository: TaskRepository

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
