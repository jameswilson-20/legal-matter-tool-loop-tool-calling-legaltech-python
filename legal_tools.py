"""Deterministic legal matter actions used by the model's tool calls."""

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field


class MatterLedger(BaseModel):
    matter_id: str
    client_name: str
    status: Literal["intake_pending", "documents_delivered", "follow_up_scheduled"]
    signed_document_id: str | None = None
    delivery_recipient: str | None = None
    follow_up_date: date | None = None
    audit_log: list[str] = Field(default_factory=list)


def record_matter_intake(ledger: MatterLedger, client_name: str) -> dict[str, Any]:
    ledger.client_name = client_name
    ledger.audit_log.append(f"intake recorded for {client_name}")
    return {"matter_id": ledger.matter_id, "status": ledger.status}


def deliver_signed_document(
    ledger: MatterLedger, document_id: str, recipient: str
) -> dict[str, Any]:
    ledger.signed_document_id = document_id
    ledger.delivery_recipient = recipient
    ledger.status = "documents_delivered"
    ledger.audit_log.append(f"signed document {document_id} delivered to {recipient}")
    return {"matter_id": ledger.matter_id, "status": ledger.status}


def schedule_deadline_follow_up(
    ledger: MatterLedger, follow_up_date: str
) -> dict[str, Any]:
    scheduled = date.fromisoformat(follow_up_date)
    ledger.follow_up_date = scheduled
    ledger.status = "follow_up_scheduled"
    ledger.audit_log.append(f"deadline follow-up scheduled for {scheduled.isoformat()}")
    return {
        "matter_id": ledger.matter_id,
        "status": ledger.status,
        "follow_up_date": scheduled.isoformat(),
    }


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "record_matter_intake",
            "description": "Record the client name for this matter.",
            "parameters": {
                "type": "object",
                "properties": {"client_name": {"type": "string"}},
                "required": ["client_name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deliver_signed_document",
            "description": "Record delivery of an already signed document.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "recipient": {"type": "string"},
                },
                "required": ["document_id", "recipient"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_deadline_follow_up",
            "description": "Schedule a follow-up on an ISO calendar date.",
            "parameters": {
                "type": "object",
                "properties": {"follow_up_date": {"type": "string"}},
                "required": ["follow_up_date"],
                "additionalProperties": False,
            },
        },
    },
]
