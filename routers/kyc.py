from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated
import os
from deps import SessionDep, get_current_user
from crud import create_kyc_submission
from pathlib import Path
from datetime import datetime

kyc_router = APIRouter(tags=["kyc"])

UPLOAD_DIR = Path("private/uploads/kyc")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@kyc_router.post("/kyc/verify")
async def submit_kyc(
    db_session: SessionDep,
    current_user = Depends(get_current_user),
    document_type: str = Form(...),
    file: UploadFile = File(...)
):
    # Save uploaded file
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"user_{current_user.id}_{timestamp}_{file.filename}"
    safe_name = filename.replace(' ', '_')
    dest = UPLOAD_DIR / safe_name
    try:
        contents = await file.read()
        with open(dest, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # create KYC submission record
    submission = await create_kyc_submission(db_session, user_id=current_user.id, document_type=document_type, document_file_path=str(dest))
    return {"status": "submitted", "id": submission.id}
