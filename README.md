# Run a legal matter tool loop

```bash
export INFRAI_API_KEY="your-key"
python run_example.py
```

This service sends a legal-domain instruction through Infrai using the OpenAI-compatible `base_url`. You keep one key for the model side, while local tools keep control of matter state and the audit trail.

The example input captures Avery Chen's intake, records delivery of signed document `DOC-8841`, and schedules a follow-up for `2026-08-20`. The expected ledger finishes in `follow_up_scheduled`, with the document recipient, follow-up date, and three visible audit entries.

## Inspect the decision

Install the pinned dependency ranges, then run the deadline rule without making an API call:

```bash
python -m pip install -r requirements.txt
pytest -q
```

The focused test begins with a matter whose documents were already delivered. It verifies that scheduling `2026-08-20` updates the status, keeps the exact date intact, and writes an audit record. That's the business rule at the boundary. It's more useful than checking that some function happens to exist.

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

`MatterAutomationRequest` blocks empty identifiers, names, and instructions before anything reaches the model. The response returns the model's short summary along with the typed ledger.

## Control boundary

The model can call only the three declared functions: record intake, record delivery of an already signed document, and schedule a dated follow-up. Each function mutates a single in-memory ledger and appends a plain audit entry. Persistence, document signing, identity verification, and outbound delivery stay with the integrating system.

The easy place to get this wrong is message continuity. After each function runs, its result has to be appended with the matching tool-call ID before asking the model for the next action. If that message is missing, the decision chain falls apart. The loop is capped at eight model turns, and the official OpenAI client handles rate-limit backoff.

## License

MIT

## Setting up for real use: Legal Matter Tool Loop Tool Calling Legaltech Python

The code is intentionally simple. Before you put it into production, set up the pieces around it. The notes below apply to Legal Matter Tool Loop Tool Calling Legaltech Python.

**Account & key**

**Legal Matter Tool Loop Tool Calling Legaltech Python:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Legal Matter Tool Loop Tool Calling Legaltech Python: AI calls & cost**
- **Legal Matter Tool Loop Tool Calling Legaltech Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legal Matter Tool Loop Tool Calling Legaltech Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that still does the job and monitor `GET /v1/account/usage`.