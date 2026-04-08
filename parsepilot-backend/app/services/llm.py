import json
import boto3
from app.config import settings

# --- CREATE BEDROCK CLIENT ---
# boto3 reads creds from
# 1. Env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# 2. ~/.aws/credentials
# 3. IAM role (IF running on EC2/Lambda)
# For local dev --> setup AWS CLI via `aws configure`
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=settings.aws_region,
)

SYSTEM_PROMPT = """You are a helpful document assistant who is extremely detail oriented and thorough. Answer the user's question based ONLY on the provided document context.

Rules:
- If the answer is in the context, provide a clear and concise response
- If the answer is NOT in the context, say "I couldn't find information about that
    in the document.
- When possible, reference which part of the document your answer comes from.
"""

def build_user_prompt(question: str, context_chunks: list[dict]) -> str:
    """
    Builds user message that includes retrieved chunks + question
    Each chunk is numbered for LLM references (ie: 'According to chunk 3...')
    """
    context_text = "\n\n.join(" \
                    f"[Chunk {i+1}]: {chunk['text']}" 
    for i, chunk in enumerate(context_chunks)

    return f"""Relevant document excerpts:
    
    {context_text}

    ---
    User's question: {question}

    Please answer based upon excepts above."""

async def ask_llm(question: str, context_chunks: list[dict]) -> str:
    """
    Send question + context to Claude via AWS Bedrock

    Args:
        question: User's question text
        context_chunks: List of dicts, each with a 'text' key containing a chunk
    
    Returns:
        The LLM's answer as a string
    """

    # Build prompt using template
    user_message = build_user_prompt(question, context_chunks)

    # --- CONSTRUCT API REQUEST ---
    # "Message API" format used by Bedrock for Claude models
    # Expects list of message objects w/ 'role' & 'content
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.2,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": user_message,
            }
        ],
    }

    # --- CALL BEDROCK ---
    # Send requests and waits for full response
    # FOR STREAMING --> use invoke_model_with_response_stream
    response = bedrock_runtime.invoke_model(
        modelId=settings.bedrock_model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body),
    )

    # --- PARSE RESPONSE ---
    # Streamed response is read & parsed
    response_body = json.loads(response["body"].read())

    # Claude's response in context[0].text
    return response_body["content"][0]["text"]