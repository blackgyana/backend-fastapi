from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    facilities: Mapped[list['FacilitiesOrm']] = relationship(
        back_populates='rooms',
        secondary='rooms_facilities'
    )