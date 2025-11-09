

from src.schemas.facilities import FacilityAddDTO
from src.services.base import BaseService


class FacilitiesService(BaseService):

    async def get_facilities(self):
        return await self.db.facilities.get_all()
        
    
    async def add_facility(self, facility_data: FacilityAddDTO):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return facility