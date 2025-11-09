

import shutil
from fastapi import UploadFile

from src.tasks.tasks import resize_image


class ImagesService:
    def upload_image(self, img_file: UploadFile):
        img_path = f'src/static/images/{img_file.filename}'
        with open(img_path, 'wb+') as new_file:
            shutil.copyfileobj(img_file.file, new_file)
        resize_image.delay(img_path)