from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService


router = APIRouter(prefix='/images')

@router.post("")
def upload_image(img_file: UploadFile):
    ImagesService().upload_image(img_file)