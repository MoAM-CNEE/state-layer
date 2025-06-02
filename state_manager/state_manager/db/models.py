from sqlalchemy import Column, BigInteger, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

Base = declarative_base()


class Entity(Base):
    __tablename__ = "entity"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    api_version = Column(String(255), nullable=False)
    kind = Column(String(255), nullable=False)
    name = Column(String(253), nullable=False)
    namespace = Column(String(63), nullable=False)
    definition = Column(JSON, nullable=True)

    __table_args__ = (
        UniqueConstraint('api_version', 'kind', 'name', 'namespace', name='unique_entity_name'),
    )

    labels = relationship("EntityLabel", back_populates="entity", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<Entity(id={self.id}, api_version='{self.api_version}', "
                f"kind='{self.kind}', name='{self.name}', namespace='{self.namespace}', definition={self.definition})>")


class EntityLabel(Base):
    __tablename__ = "entity_label"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    entity_id = Column(BigInteger, ForeignKey("entity.id"), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('entity_id', 'name', name='unique_entity_label_name'),
    )

    entity = relationship("Entity", back_populates="labels")

    def __repr__(self):
        return f"<EntityLabel(id={self.id}, name={self.name}, value={self.value})>"
