from fastapi import Body, FastAPI
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.config import settings

from src.database import *


app = FastAPI()

app.include_router(hotels_router, tags=['Отели'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
