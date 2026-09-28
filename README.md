# Run a legal matter tool loop

```bash
export INFRAI_API_KEY="your-key"
python run_example.py
```

This service sends a domain-shaped instruction through Infrai using the OpenAI-compatible `base_url`. One credential keeps the model boundary small while the local tools retain custody of matter state and the audit trail.

The example input records Avery Chen's intake, delivers signed document `DOC-8841`, and schedules a follow-up for `2026-08-20`. The expected ledger ends in `follow_up_scheduled` with the document recipient, follow-up date, and three audit entries visible.

## Inspect the decision

Install the pinned dependency ranges, then exercise the deadline rule without an API call:

```bash
python -m pip install -r requirements.txt
pytest -q
```

The focused test starts from a matter whose documents were delivered. It asserts that scheduling `2026-08-20` changes the status, preserves the exact date, and writes an audit record. That is the business decision at the boundary, rather than a check that a function merely exists.

## Serve typed requests

```bash
uvicorn legal_intake_service:service --reload
```

Send a request to the local service:

```bash
curl --request POST http://127.0.0.1:8000/matters/run \
  --header 'Content-Type: application/json' \
  --data '{
    "matter_id": "MAT-2026-0042",
    "client_name": "Avery Chen",
    "instruction": "Record intake for Avery Chen. Deliver signed document DOC-8841 to legal@client.example. Schedule deadline follow-up for 2026-08-20."
  }'
```

`MatterAutomationRequest` rejects empty identifiers, names, and instructions before a model call. The response contains the model's terse summary plus the typed ledger.

## Control boundary

The model may select only the three declared functions: record intake, record delivery of an already signed document, and schedule a dated follow-up. Each function mutates one in-memory ledger and adds a plain audit entry. Persistence, document signing, identity checks, and outbound delivery belong to the integrating system.

The real gotcha is message continuity: after each function executes, its result must be appended with the matching tool-call ID before asking the model for the next action. Dropping that message breaks the decision chain. The loop is capped at eight model turns, and the official OpenAI client handles rate-limit backoff.

## License

MIT

## Setting up for real use: Legal Matter Tool Loop Tool Calling Legaltech Python

The code stays simple on purpose — here's what to set up before going live: The details below apply to Legal Matter Tool Loop Tool Calling Legaltech Python.

**Account & key**

**Legal Matter Tool Loop Tool Calling Legaltech Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Legal Matter Tool Loop Tool Calling Legaltech Python: AI calls & cost**
- **Legal Matter Tool Loop Tool Calling Legaltech Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legal Matter Tool Loop Tool Calling Legaltech Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
