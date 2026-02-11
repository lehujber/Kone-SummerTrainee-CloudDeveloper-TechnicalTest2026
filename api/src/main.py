from fastapi import FastAPI
from .models.seashell import SeashellCreate

from .config import (
    getLogger
)
import json

app = FastAPI(title="James & Anna's seashell API")

logger = getLogger("seashell_api")

@app.post("/seashells/")
async def create_seashell(seashell: SeashellCreate):
    """Creates a new seashell entry"""

    logger.debug(f"Creating seashell: {json.dumps(seashell.model_dump(), indent=2, default=str)}" )
    return {"message": "Seashell created", "seashell": seashell.name}

@app.delete("/seashells/{seashell_id}")
async def delete_seashell(seashell_id: int):
    """Deletes a seashell entry by ID"""
    logger.debug(f"Deleting seashell with ID: {seashell_id}")
    return {"message": f"Seashell with ID {seashell_id} deleted"}

@app.put("/seashells/{seashell_id}")
async def update_seashell(seashell_id: int, seashell: SeashellCreate):
    """Updates a seashell entry by ID"""
    logger.debug(f"Updating seashell with ID: {seashell_id} to: {json.dumps(seashell.model_dump(), indent=2, default=str)}")
    return {"message": f"Seashell with ID {seashell_id} updated", "seashell": seashell.name}

@app.get("/seashells/")
async def list_seashells():
    """Lists all seashell entries"""
    logger.debug("Listing all seashells")
    return {"message": "List of seashells", "seashells": []}