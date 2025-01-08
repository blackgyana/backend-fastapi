from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKey, Integer

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Integer, CheckConstraint("price >= 1", name="check_price"), default=1000)
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity >= 0", name="check_quantity"), default=1)


# class BedChoices(str, Enum):
#     SINGLE = "two_single_beds"
#     DOUBLE = "one_double_bed"

    
# class RoomFacilities(Base):
#     __tablename__ = 'room_facilities'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
#     bed: Mapped[BedChoices] = mapped_column(Enum(BedChoices), default=BedChoices.DOUBLE)
#     places: Mapped[int] = mapped_column(SmallInteger, CheckConstraint("places >= 1", name="check_places"), default=1)
#     bath: Mapped[bool] = mapped_column(Boolean, default=False)
#     fridge: Mapped[bool] = mapped_column(Boolean, default=False)
#     conditioner: Mapped[bool] = mapped_column(Boolean, default=False)
#     furniture: Mapped[bool] = mapped_column(Boolean, default=False)
#     wifi: Mapped[bool] = mapped_column(Boolean, default=False)
#     breakfast: Mapped[bool] = mapped_column(Boolean, default=False)