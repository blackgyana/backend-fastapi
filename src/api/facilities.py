from fastapi import APIRouter
from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix='/facilities')


@router.get('', summary='Получить все удобства')
async def get_facilities(db: DBDep) -> list[Facility]:
    result = await db.facilities.get_all()
    return result


@router.post('', summary='Добавить удобство')
async def add_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {'status': 'OK', 'data': facility}
