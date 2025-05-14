from sqlalchemy import Column, BigInteger, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rule'

    id = Column(BigInteger, primary_key=True)
    _condition = Column(String(8192), unique=True, nullable=False)
    _action = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Rule(id={self.id}, _condition={self._condition})>"
