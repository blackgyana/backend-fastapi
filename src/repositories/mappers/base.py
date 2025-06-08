from pydantic import BaseModel
from src.database import Base


class DataMapper:
    db_model: type[Base]
    schema: type[BaseModel]

    @classmethod
    def to_domain_entity(cls, data: Base):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def to_persistence_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
