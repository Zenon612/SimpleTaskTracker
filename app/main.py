from fastapi import FastAPI
from app.api.v1.routers import router as task_router
from app.core.db import engine
from app.models.task import Base

app = FastAPI(title="Task Tracker API",
              description="Небольшой трекер задач в качестве учебного проекта.",
              version="1.0.0")

app.include_router(task_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)