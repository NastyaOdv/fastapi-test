from datetime import datetime

import whisper
from fastapi import UploadFile, APIRouter, HTTPException
from pymongo.errors import PyMongoError

from src.controllers import files
from src.db import db_whisper
from src.models.logger import logger
from src.models.whisper import Whisper

router = APIRouter(
    prefix="/audio",
    tags=["Audio"],
    responses={404: {"description": "Not found"}},
)
crud_whisper = db_whisper.CRUDWhisper()


@router.post("/text")
async def create_text_from_audio(file: UploadFile):
    try:
        if file.size == 0:
            raise HTTPException(status_code=400, detail="invalid body")
        start_time = datetime.now()
        file_location = await files.create_file(file)
        model = whisper.load_model("base")

        try:
            result = model.transcribe(file_location, fp16=False)
            eng_result = model.transcribe(file_location, task="translate")
        except Exception as e:
            logger.error(f"Error with Whisper model: {e}")
            raise HTTPException(status_code=500, detail="An error occurred during the transcription process.")

        processing_time = datetime.now() - start_time
        logger.debug(f"time - {processing_time}")

        item = Whisper(
            id=None,
            name=file_location,
            text=result["text"],
            language=result.get("language", ""),
            english=eng_result["text"],
            processing_time=processing_time
        )

        try:
            id = await crud_whisper.create(item)
            item.id = str(id.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting document into MongoDB: {e}")
            raise HTTPException(status_code=500,
                                detail="An error occurred while inserting the document into the database.")

        return item.to_dict()

    except HTTPException as e:
        raise e  # Re-raise the HTTPException to be handled by FastAPI

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
