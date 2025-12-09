import logging

import uvicorn
from fastapi import FastAPI
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Phone-Address Service",
)
app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        loop='uvloop',  # потому что uvloop быстрее asyncio
    )
