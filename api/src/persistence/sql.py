from sqlalchemy import create_engine, Column, Integer, String, Date, delete, insert, select, update
from sqlalchemy.ext.declarative import declarative_base

from ..models.seashell import SeashellUpdate, SeashellCreate

from typing import Optional, List

class DbAccess():
    def __init__(self, uri: str):
        self.uri = uri
        self.engine = create_engine(uri, echo=True)

    def close(self):
        self.engine.dispose()

    async def new_seashell(self, seashell: SeashellCreate) -> Optional[dict]:
        with self.engine.begin() as conn:
            cmd = (
                insert(SeashellTable).values(
                name=seashell.name,
                species=seashell.species,
                description=seashell.description,
                personal_notes=seashell.personal_notes,
                date_found=seashell.date_found
            ).returning(SeashellTable)
            )

            res = conn.execute(cmd)

            row = res.mappings().first()
            return dict(row) if row else None

    async def get_seashell(self, seashell_id: int) -> Optional[dict]:
        with self.engine.begin() as conn:
            cmd = select(SeashellTable).where(SeashellTable.id == seashell_id)
            res = conn.execute(cmd)
            row = res.mappings().first()
            return dict(row) if row else None

    async def list_seashells(self) -> List[dict]:
        with self.engine.begin() as conn:
            cmd = select(SeashellTable)
            res = conn.execute(cmd)
            return [dict(row) for row in res.mappings().all()]

    async def delete_seashell(self, seashell_id: int) -> bool:
        with self.engine.begin() as conn:
            cmd = delete(SeashellTable).where(SeashellTable.id == seashell_id)
            res = conn.execute(cmd)
            return res.rowcount > 0

    async def delete_seashells(self, sheashell_ids: List[int]) -> int:
        with self.engine.begin() as conn:
            cmd = delete(SeashellTable).where(SeashellTable.id.in_(sheashell_ids))
            res = conn.execute(cmd)
            return res.rowcount

    async def update_seashell(self,seashell_id: int, seashell: SeashellUpdate) -> Optional[dict]:
        with self.engine.begin() as conn:
            cmd = (
                update(SeashellTable)
                .where(SeashellTable.id == seashell_id)
                .values(
                    name=seashell.name,
                    species=seashell.species,
                    description=seashell.description,
                    personal_notes=seashell.personal_notes,
                    date_found=seashell.date_found
                ).returning(SeashellTable)
            )

            res = conn.execute(cmd)
            if res.rowcount > 0:
                row = res.mappings().first()
                return dict(row) if row else None
            else:
                return None




Base = declarative_base()

class SeashellTable(Base):
    __tablename__ = "seashells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    description = Column(String)
    personal_notes = Column(String)
    date_found = Column(Date)