import os
import uuid
from datetime import datetime

from fastapi import UploadFile


async def create_file(file: UploadFile):
    file_ext = os.path.splitext(file.filename)[1]
    new_name = str(uuid.uuid5(uuid.NAMESPACE_OID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) + file_ext
    new_file_location = os.path.join("files", new_name)
    with open(new_file_location, "wb") as buffer:
        buffer.write(await file.read())
    return new_file_location
