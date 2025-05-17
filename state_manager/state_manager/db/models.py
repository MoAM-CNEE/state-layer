from sqlalchemy import Column, BigInteger, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import UniqueConstraint

Base = declarative_base()


class Rule(Base):
    __tablename__ = 'rule'

    id = Column(BigInteger, primary_key=True)
    _condition = Column(String(8192), unique=True, nullable=False)
    _action = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Rule(id={self.id}, _condition={self._condition})>"


class Metric(Base):
    __tablename__ = "metric"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(1024), unique=True, nullable=False)
    query = Column(String(8192), nullable=False)

    def __repr__(self):
        return f"<Metric(id={self.id}, name={self.name})>"


class EnvironmentEntity(Base):
    __tablename__ = "environment_entity"

    id = Column(BigInteger, primary_key=True)
    api_version = Column(String(255), nullable=False)
    kind = Column(String(255), nullable=False)
    name = Column(String(253), nullable=False)
    namespace = Column(String(63), nullable=False)
    definition = Column(JSON, nullable=True)

    __table_args__ = (
        UniqueConstraint('api_version', 'kind', 'name', 'namespace', name='unique_environment_entity_name'),
    )

    labels = relationship("EnvironmentEntityLabel", back_populates="entity", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<EnvironmentEntity(id={self.id}, api_version='{self.api_version}', "
                f"kind='{self.kind}', name='{self.name}', namespace='{self.namespace}')>")


class EnvironmentEntityLabel(Base):
    __tablename__ = "environment_entity_label"

    id = Column(BigInteger, primary_key=True)
    environment_entity_id = Column(BigInteger, ForeignKey("environment_entity.id"), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('environment_entity_id', 'name', name='unique_entity_label_name'),
    )

    entity = relationship("EnvironmentEntity", back_populates="labels")

    def __repr__(self):
        return f"<EnvironmentEntityLabel(id={self.id}, name={self.name}, value={self.value})>"
