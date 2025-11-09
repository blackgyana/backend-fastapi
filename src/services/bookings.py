

from src.schemas.bookings import BookingAddDTO, BookingAddRequest, BookingDTO
from src.schemas.hotels import HotelDTO
from src.schemas.rooms import RoomDTO
from src.services.base import BaseService


class BookingsService(BaseService):

    async def get_bookings(self):
        return await self.db.bookings.get_filtered()
    
    async def get_my_bookings(self, uid:int):
        return await self.db.bookings.get_filtered(user_id=uid)
    
    async def add_booking(self, uid: int, booking_data: BookingAddRequest):
        room: RoomDTO = await self.db.rooms.get(id=booking_data.room_id)
        hotel: HotelDTO = await self.db.hotels.get(id=room.hotel_id)
        _booking_data = BookingAddDTO(**booking_data.model_dump(), user_id=uid, price=room.price)
        booking: BookingDTO = await self.db.bookings.add_booking(
            _booking_data, hotel_id=hotel.id
        )
        await self.db.commit()
        return booking

    async def delete_booking(self, uid:int, booking_id:int):
        await self.db.bookings.delete(id=booking_id, user_id=uid)
        await self.db.commit()