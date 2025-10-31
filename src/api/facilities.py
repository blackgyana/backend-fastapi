from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions.base import ObjectAlreadyExistsException, UnknownException
from src.schemas.facilities import FacilityDTO, FacilityAddDTO
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities")


@router.get("", summary="Получить все удобства")
@cache(expire=300)
async def get_facilities(db: DBDep) -> list[FacilityDTO]:
    result = await db.facilities.get_all()
    return result


@router.post("", summary="Добавить удобство")
async def add_facility(db: DBDep, facility_data: FacilityAddDTO):
    try:
        facility = await db.facilities.add(facility_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail='Удобство уже существует')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK", "data": facility}
