from datetime import date

from legal_tools import MatterLedger, schedule_deadline_follow_up


def test_deadline_follow_up_changes_matter_state_and_leaves_audit_record() -> None:
    ledger = MatterLedger(
        matter_id="MAT-2026-0042",
        client_name="Avery Chen",
        status="documents_delivered",
        signed_document_id="DOC-8841",
        delivery_recipient="legal@client.example",
    )

    result = schedule_deadline_follow_up(ledger, "2026-08-20")

    assert result == {
        "matter_id": "MAT-2026-0042",
        "status": "follow_up_scheduled",
        "follow_up_date": "2026-08-20",
    }
    assert ledger.follow_up_date == date(2026, 8, 20)
    assert ledger.audit_log == ["deadline follow-up scheduled for 2026-08-20"]
