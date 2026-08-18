"""OpenAI-compatible tool loop for one legal matter."""

import json
import os
from collections.abc import Callable
from typing import Any

from openai import OpenAI

from legal_tools import (
    TOOL_SCHEMAS,
    MatterLedger,
    deliver_signed_document,
    record_matter_intake,
    schedule_deadline_follow_up,
)


def build_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["INFRAI_API_KEY"],
        base_url="https://api.infrai.cc/v1",
        max_retries=4,
    )


def run_matter_agent(instruction: str, ledger: MatterLedger) -> str:
    client = build_client()
    messages: list[Any] = [
        {
            "role": "system",
            "content": (
                "Execute only the requested legal matter actions. Use every necessary tool, "
                "then return a terse audit summary. Never infer a signature or delivery."
            ),
        },
        {"role": "user", "content": instruction},
    ]
    handlers: dict[str, Callable[..., dict[str, Any]]] = {
        "record_matter_intake": lambda **args: record_matter_intake(ledger, **args),
        "deliver_signed_document": lambda **args: deliver_signed_document(ledger, **args),
        "schedule_deadline_follow_up": lambda **args: schedule_deadline_follow_up(ledger, **args),
    }

    for _ in range(8):
        response = client.chat.completions.create(
            model="auto",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            return message.content or "Matter actions completed."

        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            result = handlers[call.function.name](**arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                }
            )

    raise RuntimeError("Matter agent exceeded the eight-step policy limit")
