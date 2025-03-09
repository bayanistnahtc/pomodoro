from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from models import Categories, Tasks
from schema.task import TaskSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> list[Tasks]:
        query = select(Tasks)
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query).scalars().all()
        return tasks

    def get_task(self, task_id) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            task: Tasks = session.execute(query).scalar_one_or_none()
            return task

    def create_task(self, task: TaskSchema) -> int:
        task_model = Tasks(
            id=task.id,
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id
        )
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def delete_task(self, task_id: int):
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, name: str) -> list[Tasks]:
        query = select(Tasks).\
            join(Categories, Tasks.category_id == Categories.id).\
            where(Categories.name == name)
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query).scalars().all()
            return tasks

    def update_task_name(self, task_id: int, name: str) -> int:
        query = update(Tasks).\
            where(Tasks.id == task_id).\
            values(name=name).\
            returning(Tasks.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
