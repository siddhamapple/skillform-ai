from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.services.upload import handle_upload

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    resume: UploadFile = File(...),
    static_name: str = Form(...),
    static_email: str = Form(...),
    # ...add any additional static form fields here...
):
    static_info = {
        "name": static_name,
        "email": static_email,
        # ...other static fields...
    }
    try:
        result = handle_upload(resume, static_info)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
