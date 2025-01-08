from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime

from src.database import Base

class BookingsOrm(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days