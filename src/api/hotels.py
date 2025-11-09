from datetime import date
import logging
from fastapi_cache.decorator import cache
from fastapi import Body, HTTPException, Query, APIRouter

from src.exceptions.base import UnknownException
from src.exceptions.framework import HotelAlreadyExistsHTTPException, HotelNotFoundHTTPException, InvalidDatesHTTPException, UnknownHTTPException
from src.exceptions.repositories import ObjectAlreadyExistsException, ObjectNotFoundException
from src.exceptions.services import InvalidDatesException
from src.schemas.hotels import HotelDTO, HotelAddDTO, HotelUpdateDTO
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelsService


router = APIRouter(prefix="/hotels")


@router.get("", summary="Получить все отели")
@cache(expire=60)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(examples=["2025-03-01"]),
    date_to: date = Query(examples=["2025-03-10"]),
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
) -> list[HotelDTO]:
    
    try:
        return await HotelsService(db).get_hotels(pagination, date_from, date_to, title, location)
    except InvalidDatesException as ex:
        raise InvalidDatesHTTPException from ex


@router.get("/{hotel_id}", summary="Получить 1 отель")
@cache(expire=60)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex


@router.post("", summary="Добавить отель")
async def add_hotel(
    db: DBDep,
    hotel_data: HotelAddDTO = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Русь 5 звезд", "location": "Сочи, ул. Морская, 3"},
            },
            "2": {
                "summary": "Калининград",
                "value": {
                    "title": "Estate премиум люкс",
                    "location": "Калининград, ул. Набережная, 5",
                },
            },
        }
    ),
):
    try:
        new_hotel = await HotelsService(db).add_hotel(hotel_data)
    except ObjectAlreadyExistsException as ex:
        raise HotelAlreadyExistsHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK", "data": new_hotel}


@router.put("/{hotel_id}", summary="Обновить информацию об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelUpdateDTO):
    try:
        upd_hotel = await HotelsService(db).update_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK", "data": upd_hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить информацию об отеле",
    description="Можно менять каждое поле в отдельности или все поля разом",
)
async def update_hotel_part(db: DBDep, hotel_id: int, hotel_data: HotelUpdateDTO):
    try:
        upd_hotel = await HotelsService(db).update_hotel_part(hotel_id, hotel_data)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except UnknownException as ex:
        logging.exception(ex)
        raise UnknownHTTPException from ex
    return {"status": "OK", "data": upd_hotel}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except UnknownException as ex:
        logging.exception(ex)
        raise UnknownHTTPException from ex
    return {"status": "OK"}
