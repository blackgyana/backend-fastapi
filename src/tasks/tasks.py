import asyncio
from PIL import Image
import os
from src.tasks.celery_app import celery_app
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

@celery_app.task
def resize_image(image_path: str):
    sizes = [1024, 640, 360]
    output_folder = 'src/static/images'

   # Открываем изображение
    img = Image.open(image_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # Сохраняем изображение
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


async def get_bookings_with_today_checkin_helper():
    print('=== ЗАПУСК ПЕРИОДИЧЕСКОЙ ТАСКИ ===')
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f'{bookings=}')

async def periodic_loop_task():
    'Бесконечная задача в цикле'
    while True:
        await asyncio.sleep(10)
        await get_bookings_with_today_checkin_helper()


@celery_app.task(name='bookings_today_checkin')
def send_emails_for_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())