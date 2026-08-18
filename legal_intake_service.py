"""Typed HTTP boundary for legal matter automation."""

from fastapi import FastAPI, HTTPException
from openai import APIConnectionError, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

from legal_tools import MatterLedger
from matter_agent import run_matter_agent

service = FastAPI(title="Legal matter tool runner")


class MatterAutomationRequest(BaseModel):
    matter_id: str = Field(min_length=1)
    client_name: str = Field(min_length=1)
    instruction: str = Field(min_length=1)


class MatterAutomationResponse(BaseModel):
    summary: str
    matter: MatterLedger


@service.post("/matters/run", response_model=MatterAutomationResponse)
def run_matter(request: MatterAutomationRequest) -> MatterAutomationResponse:
    ledger = MatterLedger(
        matter_id=request.matter_id,
        client_name=request.client_name,
        status="intake_pending",
    )
    try:
        summary = run_matter_agent(request.instruction, ledger)
    except RateLimitError as exc:
        raise HTTPException(status_code=429, detail="Upstream capacity reached; retry later") from exc
    except APIStatusError as exc:
        status = exc.status_code if 400 <= exc.status_code < 500 else 502
        raise HTTPException(status_code=status, detail="AI request was rejected") from exc
    except APIConnectionError as exc:
        raise HTTPException(status_code=503, detail="AI service connection failed") from exc
    return MatterAutomationResponse(summary=summary, matter=ledger)
