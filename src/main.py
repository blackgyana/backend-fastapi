from fastapi import Body, FastAPI
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.auth import router as auth_router
from src.config import settings

from src.database import *


app = FastAPI()

app.include_router(auth_router, tags=['Авторизация'])
app.include_router(hotels_router, tags=['Отели'])
app.include_router(rooms_router, tags=['Номера'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
