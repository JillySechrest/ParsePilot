from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth.cognito import get_current_user
from app.services.s3 import upload_to_s3
from app.models.database import Document
from app.db import get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".csv", ".md"}
MAX_FILE_SIZE = 10 * 2024 * 2024 # 10MB Maximum file size

@router.post("/upload")
async def upload_document(
	file: UploadFile = File(...),
	current_user: dict = Depends(get_current_user),
	# Auth required
	db: Session = Depends(get_db),
):
	"""
	Upload document flow
	1. Validate file type & size
	2. Upload to S3
	3. Create db record w/ status='processing'
	4. Trigger async chunking/embedding pipeline (via SQS)
	5. Return document ID to frontend
	"""
	# --- VALIDATION --- 
	# Extract file extension & check if allowed
	extension = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
	if extension not in ALLOWED_EXTENSIONS:
		raise HTTPException(status_code=400, detail="Unsupported file type")

	# Read contents + check size
	contents = await file.read()
	if len(contents) > MAX_FILE_SIZE:
		raise HTTPException(status_code=400, detail="File too large (max 10MB)")

	# --- UPLOAD TO S3 ---
	doc_id = str(uuid.uuid4())
	user_id = current_user["sub"] # User ID from JWT
	s3_key = f"{user_id}/{doc_id}{extension}"

	await upload_to_s3(contents, s3_key)

	# --- CREATE DB RECORD ---
	document = Document(
		id=doc_id,
		user_id=user_id,
		filename=file.filename,
		s3_key=s3_key,
		# status changes to "ready" after embedding pipeline
		status="processing",
	)
	db.add(document)
	db.commit()

	# --- TRIGGER PROCESSING PIPELINE
	# In prod, send message to SQS to trigger lambda
	# In local dev, call processing function directly
	return {"docuemntId": doc_id, "status": "processing"}

@router.get("/health")
async def documents_health() -> dict[str, str]:
	return {"status": "documents route ready"}
