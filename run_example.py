"""Run one observable matter workflow without starting HTTP."""

from legal_tools import MatterLedger
from matter_agent import run_matter_agent


ledger = MatterLedger(
    matter_id="MAT-2026-0042",
    client_name="Avery Chen",
    status="intake_pending",
)
instruction = (
    "Record intake for Avery Chen. Deliver signed document DOC-8841 to "
    "legal@client.example. Schedule deadline follow-up for 2026-08-20."
)

print(run_matter_agent(instruction, ledger))
print(ledger.model_dump_json(indent=2))
