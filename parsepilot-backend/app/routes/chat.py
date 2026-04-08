from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.cognito import get_current_user
from app.services.embeddings import generate_query_embedding
from app.service.llm import ask_llm
from app.models.database import Document, ChatMessage
from app.db import get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter()

router.post("/{document_id}/ask")
async def ask_question(
		document_id: str,
		body: AskRequest,
		current_user: dict = Depends(get_current_user),
		db: Session = Depends(get_db),
):
	"""
	Full RAG flow in single endpoint
	1. Verify user owns docu
	2. Generate emebdding of user question
	3. Search pgvector for most relevant doc chunk
	4. Send chunks + question to Claude via Bedrock
	5. Save both messages to chat history
	6. Return answer
	"""
	user_id = current_user["sub"]

	# --- STEP 1: VERIFY OWNERSHIP ---
	document = db.query(Document).filter(
		Document.id == document_id,
		Document.user_id == user_id,
	).first()

	if not document:
		raise HTTPException(status_code=404, detail="Document not found")
	if document.status != "ready":
		raise HTTPException(status_code=400, detail="Document still processing")

	# --- STEP 2: EMBED THE QUESTION ---
	# Convert user text question into numeric vector
	query_embedding = await generate_query_embedding(body.question)

	# --- STEP 3: VECTOR SEARCH ---
	# Find top-5 most relevant chunks for document
	from app.services.vector_search import find_similar_chunks
	chunks = await find_similar_chunks(
		document_id=document_id,
		query_embedding=query_embedding,
		top_k=5,
	)

	# --- STEP 4: QUERY THE LLM ---
	# Combine relevant chunks into context & forward to Claude
	answer = await ask_llm(
		question=body.question,
		context_chunks=chunks,
	)

	# --- STEP 5: SAVE CHAT HISTORY ---
	user_msg = ChatMessage(
		id=str(uuid.uuid4()),
		document_id=document_id,
		user_id=user_id,
		role="user",
		content=body.question,
	)
	assistant_msg = ChatMessage(
		id=str(uuid.uuid4()),
		document_id=document_id,
		user_id=user_id,
		role="assistant",
		content=answer,
	)
	db.add_all([user_msg, assistant_msg])
	db.commit()

	# --- STEP 6: RETURN RESPONSE ---
	return {
		"messageId": assistant_msg.id,
		"answer": answer,
	}

@router.get("/{document_id}/history")
async def get_chat_history(
	document_id: str,
	current_user: dict = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	# Return all chat messages for doc, ordered by creation time
	user_id = current_user["sub"]

	# Query db for chat messages by document_id & user_id and then order by creation date
	messages = db.query(ChatMessage).filter(
		ChatMessage.document_id == document_id,
		ChatMessage = user_id == user_id,
	).order_by(ChatMessage.created_at.asc()).all()

	return {
		# return messages in history
		"messages": [
			{
				"id": m.id,
				"role": m.role,
				"content": m.content,
				"timestamp": m.created_at.isoformat(),
			}
			for m in messages
		]
	}

@router.get("/health")
async def chat_health() -> dict[str, str]:
	return {"status": "chat route ready"}
