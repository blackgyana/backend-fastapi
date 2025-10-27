from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Body, HTTPException, Query, APIRouter

from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException, UnknownException
from src.schemas.hotels import HotelDTO, HotelAddDTO, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep


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
    limit = pagination.per_page
    offset = pagination.per_page * (pagination.page - 1)

    if date_from >= date_to:
        raise HTTPException(status_code=400, detail='Дата въезда не может быть позже даты выезда')

    return await db.hotels.get_filtered_by_dates(
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        title=title,
        location=location,
    )


@router.get("/{hotel_id}", summary="Получить 1 отель")
@cache(expire=60)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await db.hotels.get(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Отель не найден')
    except UnknownException as e:
        raise HTTPException(status_code=400, detail=e.detail)

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
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail='Отель уже существует')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK", "data": new_hotel}


@router.put("/{hotel_id}", summary="Обновить информацию об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAddDTO):
    try:
        await db.hotels.update(hotel_data, id=hotel_id)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Отель не найден')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить информацию об отеле",
    description="Можно менять каждое поле в отдельности или все поля разом",
)
async def update_hotel_part(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    try:
        await db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Отель не найден')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Отель не найден')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK"}
