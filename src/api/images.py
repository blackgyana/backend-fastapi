import shutil
from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix='/images')

@router.post("")
def upload_image(img_file: UploadFile):
    img_path = f'src/static/images/{img_file.filename}'
    with open(img_path, 'wb+') as new_file:
        shutil.copyfileobj(img_file.file, new_file)
    
    resize_image.delay(img_path)