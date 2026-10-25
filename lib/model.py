import os
from pathlib import Path
from dotenv import load_dotenv
from strands.models.bedrock import BedrockModel

# Load environment variables from .env at project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")
REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
os.environ.setdefault("AWS_REGION", REGION)
os.environ.setdefault("AWS_DEFAULT_REGION", REGION)

model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
print(f"Using {MODEL_ID} in {REGION}")

__all__ = ["model", "MODEL_ID", "REGION"]
