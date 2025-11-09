from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions.base import UnknownException
from src.exceptions.framework import FacilityAlreadyExistsHTTPException, UnknownHTTPException
from src.exceptions.repositories import ObjectAlreadyExistsException
from src.schemas.facilities import FacilityDTO, FacilityAddDTO
from src.api.dependencies import DBDep
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities")


@router.get("", summary="Получить все удобства")
@cache(expire=300)
async def get_facilities(db: DBDep) -> list[FacilityDTO]:
    return await FacilitiesService(db).get_facilities()


@router.post("", summary="Добавить удобство")
async def add_facility(db: DBDep, facility_data: FacilityAddDTO):
    try:
        facility = await FacilitiesService(db).add_facility(facility_data)
    except ObjectAlreadyExistsException as ex:
        raise FacilityAlreadyExistsHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK", "data": facility}
