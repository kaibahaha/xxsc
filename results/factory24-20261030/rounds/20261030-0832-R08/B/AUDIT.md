# R08-B independent audit

- Source job_id: `701606d2cbc14621`; latest observed: QUEUED.
- Code/test/manifest: not delivered or independently read yet; GIT_CODE_PENDING.
- Independent score: N/A; status PENDING; audit_job_id: NONE.
- Once real source exists, verify SHA256, independently run `python3 -m unittest discover -s tests -v`, add >=10 new adversarial cases, review request replay, idempotency and retry/circuit correctness, give file:line P0–P3 and score /100. WorkBuddy self-tests are not independent evidence.
