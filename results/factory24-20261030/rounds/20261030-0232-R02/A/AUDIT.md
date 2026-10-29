# R02-A｜独立验收待执行

- Job: `15a3ffc753c64dcb`; parent interrupted: `9712edf966b54027`.
- Initial status: PENDING (RUNNING).
- Source/test availability: NOT YET VERIFIED. Self-test: NOT YET RETURNED. Independent audit score: N/A.
- On job completion: retrieve original result, inspect real Git source and tests, verify SHA256, rerun `python3 -m unittest discover -s tests -v` independently and add >=10 adversarial counterexamples covering edge cases, idempotency, concurrency, fault recovery, API boundaries. Grade P0–P3 with file:line evidence and score /100. A WorkBuddy self-test alone is NOT independent verification.
- Git code status: GIT_PENDING, not GIT_VERIFIED. Do not claim PASS before independent verification.
