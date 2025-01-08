from datetime import date

from sqlalchemy import func, select
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm


def filtered_free_rooms_ids(date_from: date, date_to: date, hotel_id: int | None = None):
        '''
        RAW SQL:
        
        with rooms_booked as (
            SELECT room_id, count(*) as booked_count FROM bookings
            WHERE date_from < '2025-03-10' and date_to > '2025-03-01'
            GROUP BY room_id
        ),
        rooms_left_count as (
            select rooms.id, (quantity - coalesce(booked_count, 0)) as rooms_left 
            from rooms 
            left outer join rooms_booked on rooms.id = rooms_booked.room_id
        )
        select * from rooms_left_count where rooms_left > 0;
        '''
        rooms_booked = (
            select(BookingsOrm.room_id, func.count('*').label('booked_count'))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from < date_to, 
                    BookingsOrm.date_to > date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name='rooms_booked')
        )
        rooms_left_stmt = (
            select(RoomsOrm.id.label('room_id'), 
                (RoomsOrm.quantity - func.coalesce(rooms_booked.c.booked_count, 0))
                .label('rooms_left'))
            .select_from(RoomsOrm)
            .outerjoin(rooms_booked, RoomsOrm.id == rooms_booked.c.room_id)
            .cte(name='rooms_left_stmt')
        )

        hotel_rooms_ids = (
            select(RoomsOrm.id.label('room_id'))
            .select_from(RoomsOrm)
        )
        if hotel_id is not None:    
            hotel_rooms_ids = hotel_rooms_ids.filter_by(hotel_id = hotel_id)

        hotel_rooms_ids = hotel_rooms_ids.subquery(name='hotel_rooms_ids')
        
        filtered_free_rooms_ids = (
            select(rooms_left_stmt.c.room_id)
            .select_from(rooms_left_stmt)
            .filter(rooms_left_stmt.c.rooms_left > 0,
                    rooms_left_stmt.c.room_id.in_(hotel_rooms_ids))
        )
        
        return filtered_free_rooms_ids
        


