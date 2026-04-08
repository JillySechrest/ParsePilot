import json
import boto3
from app.config import settings

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=settings.aws_region,
)

async def generate_query_embedding(text: str) -> list[float]:
    """
    Convert text string into embedding vector using Bedrock Titan

    An embedding is a list of 1536 floats that represent the "meaning" of the text
    Similar texts produce similar vectors
    """
    request_body = {
        "inputText": text,
    }

    response = bedrock_runtime.invoke_model(
        # amazon.titan-embed-text-v1
        modelId=settings.bedrock_embed_model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body),
    )

    response_body = json.loads(response["body"].read())
    # returns list of 1536 floats
    return response_body["embedding"]

async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts.
    Used during document processing to embed every chunk

    *Titan doesn't support batch embedding in a single call, so loop*
    TODO: Integrate asyncio.gather() to enable parallelization of call in prod env
    """
    embeddings = []
    for text in texts:
        embedding = await generate_query_embedding(text)
        embeddings.append(embedding)
    return embeddings
