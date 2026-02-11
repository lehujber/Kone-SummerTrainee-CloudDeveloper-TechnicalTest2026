from fastapi import FastAPI, HTTPException, Response, status

from typing import List

from .models.seashell import SeashellCreate, SeashellUpdate
from .persistence.sql import DbAccess

from .config import (
    getLogger,
    DATABASE_URI
)
import json

app = FastAPI(title="James & Anna's seashell API")
db = DbAccess(DATABASE_URI)


logger = getLogger("seashell_api")

@app.post("/seashells/")
async def create_seashell(seashell: SeashellCreate):
    """Creates a new seashell entry"""

    logger.debug(f"Creating seashell: {json.dumps(seashell.model_dump(), indent=2, default=str)}" )

    try:
        created = await db.new_seashell(seashell)
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create seashell")
        
        logger.debug(f"Seashell created with ID: {created['id']}")
        return  created

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating seashell: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating seashell")

@app.delete("/seashells/{seashell_id}")
async def delete_seashell(seashell_id: int):
    """Deletes a seashell entry by ID"""
    logger.debug(f"Deleting seashell with ID: {seashell_id}")
    try:
        deleted = await db.delete_seashell(seashell_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Seashell not found")
        
        logger.debug(f"Seashell with ID {seashell_id} deleted")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting seashell: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting seashell")

@app.delete("/seashells/")
async def delete_seashells(seashell_ids: List[int]):
    """Deletes multiple seashell entries by their IDs"""
    logger.debug(f"Deleting seashells with IDs: {seashell_ids}")
    try:
        deleted_count = await db.delete_seashells(seashell_ids)
        logger.debug(f"Deleted {deleted_count} seashells")
        return {"deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"Error deleting seashells: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting seashells")

@app.put("/seashells/{seashell_id}")
async def update_seashell(seashell_id: int, seashell: SeashellUpdate):
    """Updates a seashell entry by ID"""
    logger.debug(f"Updating seashell with ID: {seashell_id} to: {json.dumps(seashell.model_dump(), indent=2, default=str)}")

    try:
        updated = await db.update_seashell(seashell_id, seashell)
        if not updated:
            raise HTTPException(status_code=404, detail="Seashell not found")
        
        logger.debug(f"Seashell with ID {seashell_id} updated")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating seashell: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating seashell")

@app.get("/seashells/{seashell_id}")
async def get_seashell(seashell_id: int):
    """Retrieves a seashell entry by ID"""
    logger.debug(f"Retrieving seashell with ID: {seashell_id}")
    try:
        seashell = await db.get_seashell(seashell_id)
        if not seashell:
            raise HTTPException(status_code=404, detail="Seashell not found")
        
        logger.debug(f"Seashell retrieved: {json.dumps(seashell, indent=2, default=str)}")
        return seashell
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving seashell: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving seashell")

@app.get("/seashells/")
async def list_seashells():
    """Lists all seashell entries"""
    logger.debug("Listing all seashells")
    try:
        seashells = await db.list_seashells()
        logger.debug(f"Retrieved {len(seashells)} seashells")
        return  seashells
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing seashells: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing seashells")