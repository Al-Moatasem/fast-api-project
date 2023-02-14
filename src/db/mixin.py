  
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql.expression import text


@declarative_mixin
class MixinTimestamp:
    created_at = Column(DateTime, server_default=text('now()'), nullable=False)
    updated_at = Column(DateTime, server_default=text('now()'), nullable=False, onupdate=text('now()'))
