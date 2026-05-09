from fastapi import FastAPI

from src.portfolio import api_router


app = FastAPI()


app.include_router(api_router)


@app.on_event("startup")
async def startup():
    from src.core.db import Base, engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)