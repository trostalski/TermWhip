from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.db.base import Base


class LoincCode(Base):
    __tablename__ = "loinc_codes"

    code = Column("code", String, primary_key=True, index=True)
    component = Column("component", String)
    property = Column("property", String)
    time_aspct = Column("time_aspct", String)
    system = Column("system", String)
    scale_type = Column("scale_type", String)
    method_type = Column("method_type", String)
    _class = Column("class", String)
    class_type = Column("class_type", String)
    long_name = Column("long_name", String)
    short_name = Column("short_name", String)
    external_copy_right_notice = Column("external_copy_right_notice", String)
    status = Column("status", String)
    version_first_released = Column("version_first_released", String)
    version_last_changes = Column("version_last_changes", String)
    fts_ts_vector = Column("fts_ts_vector", TSVECTOR)

    __table__args__ = (
        Index(
            "idx_loinc_fts_tsvector",
            fts_ts_vector,
            postgresql_using="gin",
        ),
    )
