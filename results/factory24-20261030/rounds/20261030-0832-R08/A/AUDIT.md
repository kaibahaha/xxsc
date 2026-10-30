# R08-A independent audit

- Source job_id: `a13b941e4ea349be`; latest observed: QUEUED.
- Code/test/manifest: not delivered or independently read yet; GIT_CODE_PENDING.
- Independent score: N/A; status PENDING; audit_job_id: NONE.
- Once real source exists, verify SHA256, independently run `python3 -m unittest discover -s tests -v`, add >=10 new adversarial cases, review transaction durability, recovery idempotence and checkpoint crashes, give file:line P0–P3 and score /100. WorkBuddy self-tests are not independent evidence.
