from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #TODO --> CREATE POSTGRES SERVICE
    # DB
    database_url: str = "postgresql://user:pass@localhost:3002/parsepilot"

    #TODO --> CREATE S3 BUCKET
    # AWS
    aws_region: str = "use-east-1"
    s3_bucket_name: str = "parse-pilot-ingest"

    #TODO --> VERIFY COGNITO REGION
    # Cognito
    cognito_user_pool_id: str
    cognito_app_client_id: str
    cognito_region: str = "us-east-1"

    #TODO --> CREATE BEDROCK SERVICE IN AWS
    bedrock_model_id: str = "anthropic.claude-4-sonnet-20240229-v1:0"
    bedrock_embed_model_id: str = "amazon.tital-embed-text-v1"

    class Config:
            # Read from .env file
            env_file = ".env"
    
settings = Settings()


