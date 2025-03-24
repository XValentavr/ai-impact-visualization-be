import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from api.routers import all_routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import logging  # noqa
from app.config.settings import settings

app = FastAPI(title="AI Impact Visualization", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.server.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server.HOST,
        port=settings.server.PORT,
        reload=settings.server.DEBUG,
        reload_dirs=["app"],
        reload_excludes=["logs/application.log"],
        log_config=None,
        log_level=None,
    )
